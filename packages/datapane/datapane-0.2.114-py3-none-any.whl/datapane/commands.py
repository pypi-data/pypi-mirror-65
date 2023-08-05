import dataclasses as dc
import os
import uuid
from distutils.dir_util import copy_tree
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import click
from jinja2 import Environment, FileSystemLoader
from requests import HTTPError

from dp_common import log

from . import __rev__, __version__, api
from . import config as c
from . import project as p

# TODO
#  - add info subcommand
#  - convert to use typer (https://github.com/tiangolo/typer) or autoclick


def init(debug: Optional[bool], config_env: str):
    """Init the cmd-line env"""
    api.init(config_env=config_env, debug=debug or False)
    # config_f = c.load_from_envfile(config_env)
    # _debug = debug if debug is not None else c.config.debug
    # setup_logging(verbose_mode=_debug)
    # log.debug(f"Loaded environment from {config_f}")


@dc.dataclass(frozen=True)
class DPContext:
    """
    Any shared context we want to pass across commands,
    easier to just use globals in general tho
    """

    env: str


def success_msg(msg: str):
    click.secho(msg, fg="green")


def failure_msg(msg: str):
    click.secho(msg, fg="red")


def gen_title() -> str:
    return f"New - {uuid.uuid4().hex}"


###############################################################################
# Main
@click.group()
@click.option("--debug/--no-debug", default=None, help="Enable additional debug output.")
@click.option("--env", default=c.DEFAULT_ENV, help="Alternate config environment to use.")
@click.version_option(version=f"{__version__} ({__rev__})")
@click.pass_context
def cli(ctx, debug: bool, env: str):
    """Datapane CLI Tool"""
    init(debug, env)
    ctx.obj = DPContext(env=env)


###############################################################################
# Auth
@cli.command()
@click.option("--token", prompt="Your API Token", help="API Token to the Datapane server.")
@click.option("--server", default="https://datapane.com", help="Datapane API Server URL.")
@click.pass_obj
def login(obj: DPContext, token, server):
    """Login to a server with the given API token."""
    config = c.Config(server=server, token=token)
    r = api.Resource(endpoint="/settings/login/", config=config).get()

    # update config with valid values
    with c.update_config(obj.env) as x:
        x["server"] = server
        x["token"] = token

    # click.launch(f"{server}/settings/")
    success_msg(f"Logged in to {server} as {r.username}")


@cli.command()
@click.pass_obj
def logout(obj: DPContext):
    """Logout from the server and reset the API token in the config file."""
    with c.update_config(obj.env) as x:
        x["server"] = c.DEFAULT_SERVER
        x["token"] = c.DEFAULT_TOKEN

    success_msg(f"Logged out from {c.config.server}")


@cli.command()
def ping():
    """Check can connect to the server."""
    try:
        r = api.Resource(endpoint="/settings/login").get()
        success_msg(f"Connected to {c.config.server} as {r.username}")
    except HTTPError as e:
        failure_msg(f"Couldn't successfully connect to {c.config.server}, check your login details")
        log.error(e)


###############################################################################
# Blobs
@cli.group()
def blob():
    """Commands to work with Blobs"""
    ...


@blob.command()
@click.argument("file", type=click.Path(exists=True))
@click.option("--public/--not-public", default=False)
@click.option("--title", default=gen_title)
def upload(file: str, public: bool, title: str):
    """Upload a csv or Excel file as a Datapane Blob"""
    log.info(f"Uploading {file}")
    r = api.Blob.upload_file(file, make_public=public, title=title)
    success_msg(f"Uploaded {click.format_filename(file)} to {r.url}")


@blob.command()
@click.argument("id")
@click.argument("file", type=click.Path())
def download(id: str, file: str):
    """Download blob referenced by ID to FILE"""
    r = api.Blob(id).download_file(file)
    success_msg(f"Downloaded {r.url} to {click.format_filename(file)}")


@blob.command()
@click.argument("id")
def delete(id: str):
    """Delete a blob"""
    api.Blob(id).delete()


###############################################################################
# Scripts
@cli.group()
def script():
    """Commands to work with Scripts"""
    ...


@script.command(name="init")
@click.option("--title", default=p.default_title)
@click.option("--name", default=lambda: os.path.basename(os.getcwd()))
def script_init(title: str, name: str):
    """Initialise a new script project"""
    # NOTE - only supports single hierarchy project dirs
    env = Environment(loader=FileSystemLoader("."))

    def render_file(fname: Path, context: Dict):
        rendered_script = env.get_template(fname.name).render(context)
        fname.write_text(rendered_script)

    # copy the scaffolds into the service
    def copy_scaffold(name: str) -> List[Path]:
        dir_path = p.get_res_path(os.path.join("scaffold", name))
        copy_tree(dir_path, ".")
        return [Path(x.name) for x in dir_path.iterdir()]

    if p.DATAPANE_YAML.exists():
        raise ValueError("Found existing project, cancelling")

    p.validate_name(name)
    common_files = copy_scaffold("common")
    stack_files = copy_scaffold("python")

    # run the scripts
    scaffold = dict(name=name, title=title)
    for f in common_files + stack_files:
        if f.exists() and f.is_file():
            render_file(f, dict(scaffold=scaffold))
    success_msg(f"Created script '{name}', edit as needed and upload")


@script.command()
@click.option("--config", type=click.Path(exists=True))
@click.option("--script", type=click.Path(exists=True))
@click.option("--public/--not-public", default=None)
@click.option("--title")
def upload(
    public: Optional[bool], title: Optional[str], script: Optional[str], config: Optional[str]
):
    """Upload a Python script or Jupyter notebook as a Datapane Script"""
    script = script and Path(script)
    config = config and Path(config)
    init_kwargs = dict(public=public, title=title, script=script, config_file=config)
    kwargs = {k: v for k, v in init_kwargs.items() if v is not None}
    proj = p.DatapaneCfg.create(**kwargs)

    log.debug(f"Uploading datapane project {proj.name}")
    r: api.Script = api.Script.upload_file(**proj.to_dict())
    success_msg(f"Uploaded {click.format_filename(str(proj.script))} to {r.web_url}")


@script.command()
@click.argument("id")
@click.argument("file", type=click.Path())
def download(id: str, file: str):
    """Download script referenced by ID to FILE"""
    r = api.Script(id).download_file(file)
    success_msg(f"Downloaded {r.url} to {click.format_filename(file)}")


@script.command()
@click.argument("id")
def delete(id: str):
    """Delete a script"""
    api.Script(id).delete()


@script.command()
# @click.option("--clone", help="Clone the report before running.")
def run(id):
    """Run a report"""
    r = api.Script(id).run()
    success_msg(f"Script generated report at {r.url}")


###############################################################################
# Reports
@cli.group()
def report():
    """Commands to work with Reports"""
    ...


@report.command()
@click.argument("files", type=click.Path(), nargs=-1, required=True)
@click.option("--public/--not-public", default=False)
@click.option("--title", default=gen_title)
def create(files: Tuple[str], public: bool, title: str):
    """Create a Report from the provided FILES"""
    blocks = [api.Asset.upload_file(file=Path(f)) for f in files]
    r = api.Report.create(*blocks, make_public=public, title=title)
    success_msg(f"Created Report {r.web_url}")


@report.command()
@click.argument("id")
def delete(id: str):
    """Delete a report"""
    api.Report(id).delete()


@report.command()
@click.argument("id")
@click.option("--filename", default="output.html", type=click.Path())
def render(id: str, filename: str):
    """Render a report to a static file"""
    api.Report(id).render()
