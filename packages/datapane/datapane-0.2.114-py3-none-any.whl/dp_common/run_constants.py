"""
App-wide constant values and types
 - this module should have no external dependencies
 - hard-coded constants for now, but could move to env-var if need configurable
"""
import dataclasses as dc
import json
from abc import ABC
from enum import IntEnum
from pathlib import Path
from typing import ClassVar, List, Optional, TextIO

from .dp_types import REGISTRY, Hash, MountVolume, NPath

# TODO - most these dirs / statics can be removed with new runner mechanism

# Directories

# From Ed:
# the subdirs were split into user/system/internal iirc. user is the dir that all files a user
# writes go into, system is where all the system files are written to (so thats input/output arrow,
# the result json, etc), and internal are where additional files that aren't user go into
# (such as the dataframe statistics. all files that we want stored as 'additional files' but we
# create not the user). the perms should be set so that the user cannot traverse into those from
# their scripts. (note the perms on the parent /runner dir not having the exec bit iirc)
#
# so, regarding the paths that can be set via the command line args to the inner process. the basic
# premise is that those are controlled by the outer process and they need to be communicated to the
# inner process somehow. that could be via the shared `run_constants.py` module for instance, or it
# could be that they're passed in via the cmd line args (or env vars). I think I went for the latter
# for ease of testing (we don't have them but potentially for tests run in multiplae threads where
# those args can be supplied by the equivalent of `mktemp -d`). In my testing when writing I ended
# up with many clashes on test files that hadn't been deleted from the last test, so was easy just
# to pass those in so they would be fresh tmp dirs each time.

# shared dir between system and user code
RES_DIR = Path("/runner")
# cwd that the user code is run in
USER_RES_DIR = RES_DIR / "user"
# holds input/output datasets
SYS_RES_DIR = RES_DIR / "system"
# stores extra files, e.g. logs, df.describe, etc.
INT_RES_DIR = SYS_RES_DIR / "additional-files"

STDOUT = INT_RES_DIR / "stdout.txt"
STDERR = INT_RES_DIR / "stderr.txt"

# code locations within the container
APP_DIR = Path("/app")
# wrapper code
SYS_CODE_DIR = APP_DIR / "system"
# lang-specific code
USER_CODE_DIR = APP_DIR / "user"


REPO_DIR = Path(__file__).parent.parent.parent
IMAGES_DIR = REPO_DIR / "container-images"
HOST_SHARED_DIR = REPO_DIR / "dp-common"

INT_SHARED_DIR = APP_DIR / "dp-common"
# File names / paths
RESULT_FN = SYS_RES_DIR / "result.json"
CONFIG_FN = SYS_RES_DIR / "config.json"
MODEL_CONFIG_FN = SYS_RES_DIR / "model_config.json"


# def get_input_dataframe_fn(x: int) -> Path:
#     return SYS_RES_DIR / "input-dataframe-{:d}.arrow".format(x)
#
#
# def get_output_dataframe_fn(x: int) -> Path:
#     return SYS_RES_DIR / "output-dataframe-{:d}.arrow".format(x)


# Users
SYS_UID = "1001"
SYS_USER = "syscode"
USER_UID = "1002"
USER_USER = "usercode"

# TODO - use the Docker Python API


class StepType(IntEnum):
    # DOCKER = 0
    PYTHON = 1
    SQL = 2
    JULIA = 3
    R = 4


@dc.dataclass
class LanguageImage(ABC):
    image_name: str

    step_type: ClassVar[StepType]
    exe: ClassVar[List[str]]
    volumes: ClassVar[List[MountVolume]]

    def full_name(self, tag: str) -> str:
        return f"{REGISTRY}/{self.image_name}:{tag}"

    # TODO - this is only valid for default images
    @property
    def build_dir(self) -> Path:
        return Path("container-images") / self.image_name


HOST_CLI_DIR = IMAGES_DIR.parent / "dp-cli"
INT_SITE_PKGS = Path("/usr/local/lib/python3.7/site-packages")


@dc.dataclass
class PythonImage(LanguageImage):
    step_type = StepType.PYTHON
    exe = ["dp-runner"]  # /usr/local/bin/dp-runner
    volumes = [
        MountVolume(host_dir=HOST_CLI_DIR / "datapane", container_dir=INT_SITE_PKGS / "datapane"),
        MountVolume(host_dir=HOST_CLI_DIR / "dp_runner", container_dir=INT_SITE_PKGS / "dp_runner"),
        MountVolume(host_dir=HOST_CLI_DIR / "dp_common", container_dir=INT_SITE_PKGS / "dp_common"),
    ]


python_default_image = PythonImage(image_name="dp-python-default")

all_images: List[LanguageImage] = [python_default_image]


def get_default_image(st: StepType) -> LanguageImage:
    if st == StepType.PYTHON:
        return python_default_image
    raise ValueError(f"{st.name} functions are currently unsupported")


@dc.dataclass
class RunResult:
    report_id: str
    cacheable: bool = False
    # used for GC - tho could get by xpath
    cas_refs: List[Hash] = dc.field(default_factory=list)
    asset_ids: List[int] = dc.field(default_factory=list)

    def to_json(self, stream: TextIO):
        json.dump(dc.asdict(self), stream)


@dc.dataclass
class ErrorResult:
    error: str
    error_detail: str = ""
    debug: Optional[str] = None

    def to_json(self, stream: TextIO):
        json.dump(dc.asdict(self), stream)


def internal_filename(fn: NPath) -> Path:
    fn = Path(fn)
    if fn.is_absolute():
        fn = fn.relative_to("/")
    return INT_RES_DIR / fn
