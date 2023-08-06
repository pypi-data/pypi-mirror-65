import dataclasses as dc
import os
import pprint
import time
import typing as t
import uuid
from contextlib import contextmanager
from copy import copy
from pathlib import Path
from urllib import parse as up
from urllib import request as ur

# TODO - import only during type checking and import future.annotations when dropping py 3.6
import pandas as pd
import requests
import validators as v
from munch import Munch, munchify
from requests import HTTPError, Response  # noqa: F401

from dp_common import ARROW_MIMETYPE, JSON, URL, JDict, NPath, SDict, log, setup_logging, temp_fname
from dp_common.df_processor import process_df, to_df

from . import config as c

# top level functions here
# check where running
# on_datapane: bool = "DATAPANE_ON_DATAPANE" in os.environ


def init(
    config_env: str = "default",
    config: t.Optional[c.Config] = None,
    debug: bool = False,
    logs_stream: t.Optional[t.TextIO] = None,
):
    """Init the API - this MUST handle being called multiple times"""
    if c.get_config() is not None:
        log.debug("Already init")

    if config:
        c.set_config(config)
    else:
        config_f = c.load_from_envfile(config_env)
        log.debug(f"Loaded environment from {config_f}")

    setup_logging(verbose_mode=debug, logs_stream=logs_stream)


def is_jupyter():
    """Checks if inside ipython shell inside browser"""
    return (
        "get_ipython" in __builtins__
        and get_ipython().__class__.__name__ == "ZMQInteractiveShell"  # noqa: F821
    )


# TODO - make generic and return a dataclass from server?
#  - we can just use Munch and proxying for now, and type later if/when needed
class Resource:
    # TODO - this should probably hold a requests session object
    endpoint: str
    headers: t.Dict
    url: str

    def __init__(self, endpoint: str, config: t.Optional[c.Config] = None):
        self.endpoint = endpoint.split("/api", maxsplit=1)[-1]
        self.config = config or c.config
        self.url = up.urljoin(self.config.server, f"api{self.endpoint}")
        self.headers = dict(Authorization=f"Token {self.config.token}")

    def _process_res(self, r: Response) -> JSON:
        if not r.ok:
            try:
                log.debug(pprint.pformat(r.json()))
            except ValueError:
                log.debug(pprint.pformat(r.text))
        r.raise_for_status()
        r_data = r.json()
        return munchify(r_data) if isinstance(r_data, dict) else r_data

    def post(self, params: t.Dict = None, **data: JSON) -> JSON:
        params = params or dict()
        r = requests.post(self.url, json=data, params=params, headers=self.headers)
        return self._process_res(r)

    def get(self) -> JSON:
        r = requests.get(self.url, headers=self.headers)
        return self._process_res(r)

    def patch(self, **data: JSON) -> JSON:
        r = requests.patch(data, headers=self.headers)
        return self._process_res(r)

    def delete(self) -> None:
        r: Response = requests.delete(self.url, headers=self.headers)
        r.raise_for_status()

    @contextmanager
    def nest_endpoint(self, endpoint: str) -> t.ContextManager["Resource"]:
        """Returns a context manager allowing recursive nesting in endpoints"""
        a = copy(self)
        a.url = up.urljoin(a.url, endpoint)
        log.debug(f"Nesting endpoint {endpoint}")
        yield a
        log.debug(f"Unnesting endpoint {endpoint}")


# @dc.dataclass(frozen=True)
# class UserObjectDTO:
#     url: URL
#     id: str
#     isPublic: bool
#     parent: t.Optional[URL]
#     ...
#

# TODO - wrap into a UserObject mixin?
def process_args(make_public: bool, kwargs: SDict) -> SDict:
    """Return new kwargs"""
    _kwargs = copy(kwargs)
    if "visibility" not in _kwargs:
        _kwargs["visibility"] = "PUBLIC" if make_public else "OWNER_ONLY"
    return _kwargs


class BEObjectRef:
    url: URL

    endpoint: str
    res: Resource
    # dto: UserObjectDTO
    dto: t.Optional[Munch] = None
    list_fields: t.List[str] = ["id", "title", "web_url"]

    @classmethod
    def _create_from_file(cls, file: Path, **kwargs) -> JSON:
        # get signed url
        upload_name = f"{int(time.time())}-{file.name}"
        upload_url = Resource("/generate-upload-url/").post(import_path=upload_name)
        # post text to blob store
        with file.expanduser().open("rb") as fp:
            log.info(f"Uploading {file}")
            requests.put(upload_url, data=fp).raise_for_status()
        # post dataset to api
        return Resource(cls.endpoint).post(import_path=upload_name, **kwargs)

    def set_url(self, id_or_url: str):
        # build a url to the resource on the api server
        _id: str
        if self.endpoint in id_or_url:
            url = id_or_url
            if not url.startswith("http"):
                url = f"https://{url}"
            if not v.url(url):
                raise AssertionError(f"{url} is not a valid object ref")
            x: up.SplitResult = up.urlsplit(url)
            _id = list(filter(None, x.path.split("/")))[-1]
        else:
            _id = id_or_url

        rel_obj_url = up.urljoin(self.endpoint, f"{_id}/")
        self.res = Resource(endpoint=rel_obj_url)
        self.url = self.res.url

    # obj storage
    def get_obj(self) -> None:
        self.dto = self.res.get()

    @property
    def has_obj(self) -> bool:
        return self.dto is not None

    def __init__(self, id_or_url: str = None, dto: t.Optional[Munch] = None):
        if id_or_url:
            self.set_url(id_or_url)
            self.get_obj()
        elif dto:
            self.set_url(dto.url)
            self.dto = dto

    def __getattr__(self, attr):
        if self.has_obj:
            log.debug(f"Proxying {attr} lookup to DTO")
            return getattr(self.dto, attr)
        # Default behaviour
        return self.__getattribute__(attr)

    def __str__(self) -> str:
        return self.url

    def __repr__(self) -> str:
        return pprint.pformat(self.dto.toDict())

    # helper functions
    def refresh(self):
        """Update the local representation of the object"""
        self.get_obj()
        log.debug(f"Refreshed {self.url}")

    def delete(self):
        self.res.delete()
        log.info(f"Deleted object {self.url}")

    @classmethod
    def list(cls) -> t.Iterable[SDict]:
        """Return a list of the resources """
        endpoint: t.Optional[str] = cls.endpoint

        while endpoint:
            r = Resource(endpoint=endpoint)
            items = r.get()
            # filter the items, ordering as needed
            for x in items.results:
                yield {k: x[k] for k in cls.list_fields if k in x}
            endpoint = items.next if items.next else None


class ExportableObjectMixin:
    def download_df(self) -> pd.DataFrame:
        export_format = ".json.gz"
        with self.res.nest_endpoint(endpoint=f"export/?export_format={export_format}") as nest_res:
            download_url: str = nest_res.get()

        with temp_fname(".json.gz") as fn:
            log.debug(f"Downloading {download_url} to {fn}")
            _ = ur.urlretrieve(download_url, fn)
            df = pd.read_json(fn, orient="table")
            df = to_df(df)
            process_df(df)

        return df

    def download_file(self, fn: NPath) -> URL:
        fn = Path(fn)

        # If file is of arrow type, export it. Otherwise use the gcs url directly.
        if self.content_type == ARROW_MIMETYPE:
            with self.res.nest_endpoint(
                endpoint=f"export/?export_format={self.get_export_format(fn)}"
            ) as nest_res:
                download_url = nest_res.get()
        else:
            download_url = self.gcs_signed_url
        log.info(f"Downloading {download_url} to {fn}")
        _ = ur.urlretrieve(download_url, fn)

    @staticmethod
    def save_df(df: pd.DataFrame) -> Path:
        df = to_df(df)
        process_df(df)
        with temp_fname(".json.gz", keep=True) as fn:
            fn = Path(fn)
            df.to_json(str(fn), orient="table")
            log.debug(f"Saved df to {fn} ({os.path.getsize(fn)} bytes)")
            return fn

    @staticmethod
    def get_export_format(fn: Path) -> str:
        # TODO: Use DatasetFormats Enum
        valid_formats = [".json.gz", ".csv", ".xlsx"]
        ext = "".join(fn.suffixes)
        if ext not in valid_formats:
            raise ValueError(
                f"Extension {ext} not valid for exporting table. Must be one of {', '.join(valid_formats)}"
            )
        return ext


class Blob(BEObjectRef, ExportableObjectMixin):
    endpoint: str = "/blobs/"

    @classmethod
    def upload_df(cls, df: pd.DataFrame, make_public: bool = False, **kwargs) -> "Blob":
        fn = cls.save_df(df)
        res = cls._create_from_file(fn, **process_args(make_public, kwargs))
        return cls(dto=res)

    @classmethod
    def upload_file(cls, fn: NPath, make_public: bool = False, **kwargs) -> "Blob":
        res = cls._create_from_file(Path(fn), **process_args(make_public, kwargs))
        return cls(dto=res)

    def download_file(self, fn: NPath) -> "Blob":
        super().download_file(fn)
        return self


class Script(BEObjectRef):
    endpoint: str = "/scripts/"

    @classmethod
    def upload_str(cls, script: str, public: bool = False, **kwargs) -> "Script":
        """Upload a function from the file (or current script?)"""
        with temp_fname(".py", keep=True) as fn:
            file = Path(fn)
            file.write_text(script)
        res = cls._create_from_file(file, **process_args(public, kwargs))
        return cls(dto=res)

    @classmethod
    def upload_file(cls, script: NPath, public: bool = False, **kwargs) -> "Script":
        res = cls._create_from_file(Path(script), **process_args(public, kwargs))
        return cls(dto=res)

    def download_str(self) -> str:
        return self.res.get().source_code

    def download_file(self, fn: NPath) -> "Script":
        """Download to fn given"""
        fn = Path(fn)
        if fn.suffix == ".py":
            fn.write_text(self.download_str())
        elif fn.suffix == ".ipynb":
            with self.res.nest_endpoint(endpoint="export/") as nest_res:
                download_url: str = nest_res.post()
            log.debug(f"Downloading {download_url} to {fn}")
            _ = ur.urlretrieve(download_url, fn)
        else:
            raise NotImplementedError(f"Can't export script to {fn}")
        return self

    def run(self, parameters=None, cache=True) -> "Run":
        """run the given app (cloning if needed?)"""
        parameters = parameters or dict()
        res = Resource("/runs/").post(script=self.url, parameter_vals=parameters, cache=cache)
        return Run(dto=res)


class Asset(BEObjectRef, ExportableObjectMixin):
    """We handle Asset's differently as effectively have to store the user request until
    it's been attached to a Datapane Asset block"""

    endpoint = "/assets/"

    file: Path = None
    kwargs: JDict = None

    @classmethod
    def upload_file(cls, file: NPath, **kwargs: JSON) -> "Asset":
        return cls(file=file, kwargs=kwargs)

    @classmethod
    def upload_df(cls, df: pd.DataFrame, **kwargs: JSON) -> "Asset":
        fn = cls.save_df(df)
        return cls(file=str(fn), kwargs=kwargs)

    @classmethod
    def upload_obj(cls, data: t.Any, **kwargs: JSON) -> "Asset":
        # import here as a very slow module due to nested imports
        from .files import show

        with temp_fname(".obj", keep=True) as fn:
            try:
                out_fn = show(data, filename=fn)
                return cls(file=out_fn, kwargs=kwargs)
            except NotImplementedError:
                # `show` doesn't support the file - just write and hope :)
                file = Path(fn)
                file.write_bytes(data)
                return cls(data=data, kwargs=kwargs)

    def _post_update(self, block_id: int):
        block_url = up.urljoin(c.config.server, f"api/blocks/{block_id}/")
        res = self._create_from_file(self.file, report_block=block_url, **self.kwargs)
        # reset the object internally
        self.set_url(res.url)
        self.get_obj()

    def __init__(
        self, id_or_url: str = None, file: NPath = None, data: t.Any = None, kwargs: JDict = None
    ):
        if id_or_url is not None:
            super().__init__(id_or_url)
        else:
            # building buffered version
            self.file = Path(file)
            self.kwargs = kwargs


@dc.dataclass(frozen=True)
class Markdown:
    content: str


# NOTE - hacks re API compatability
class Plot(Asset):
    @classmethod
    def create(cls, data: t.Any, **kwargs: JSON) -> "Asset":
        return Asset.upload_obj(data=data, **kwargs)


class Table(Asset):
    @classmethod
    def create(cls, df: pd.DataFrame, **kwargs: JSON) -> "Asset":
        return Asset.upload_df(df=df, **kwargs)


class Run(BEObjectRef):
    endpoint: str = "/runs/"

    def is_complete(self) -> bool:
        """Return true if the run has finished"""
        return self.status in ["SUCCESS", "ERROR", "CANCELLED"]


# @dc.dataclass()
# class Block:
#     # a subset of block types - we'll combine with munch for other dynamic attribs
#     refId: str
#     type: str
#     id: t.Optional[int] = None
#     dataset: t.Optional[URL] = None
#     function: t.Optional[URL] = None
#     content: t.Optional[str] = None


# Internal type to represent the blocks as exposed to the lib consumer
BlockType = t.Union[Asset, Markdown]


def mk_block(b: BlockType) -> JSON:
    r = Munch()
    r.ref_id = str(uuid.uuid4())
    if isinstance(b, Markdown):
        r.type = "MARKDOWN"
        r.content = b.content
    elif isinstance(b, Asset):
        r.type = "ASSET"
        r.asset = None  # block.asset
    return r


class Report(BEObjectRef):
    """create, run, and delete ops only, retrieve and update unsupported"""

    endpoint: str = "/reports/"

    @classmethod
    def create(cls, *blocks: BlockType, make_public: bool = False, **kwargs) -> "Report":
        """Create a simple app based on datasets, dfs, and plots"""
        new_blocks = [mk_block(b) for b in blocks]
        # post report to api
        res = Resource(cls.endpoint).post(blocks=new_blocks, **process_args(make_public, kwargs))
        # upload assets and attach to the report
        #  - this is a bit hacky as relies on the ordering staying the same
        #  - could update by using refId
        log.info("Uploading assets for Report")
        for (idx, b) in enumerate(res.blocks):
            if b.type == "ASSET":
                asset: Asset = blocks[idx]
                asset._post_update(b.id)
        # recreate from url so have latest assets
        return cls(res.url)

    def __getitem__(self, key: int) -> JSON:
        """Return the block for the report"""
        return self.dto.blocks[key]

    def render(self, output_fn: Path):
        raise NotImplementedError("")

    def preview(self, width: int = 600, height: int = 500):
        # Preview reports inside IPython notebooks in browser
        if is_jupyter():
            from IPython.display import IFrame

            embed_url = self.embed_url
            if self.visibility != "PUBLIC":
                embed_url = self.private_embed_url
            return IFrame(src=embed_url, width=width, height=height)
