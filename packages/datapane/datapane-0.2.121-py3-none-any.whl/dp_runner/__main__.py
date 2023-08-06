import argparse
import grp
import os
import pwd
import sys
import traceback
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Optional, TextIO, Tuple

from packaging import version as v
from packaging.specifiers import SpecifierSet

from datapane import __version__, api
from datapane import config as c
from dp_common import log
from dp_common.config import RunnerConfig, decode
from dp_common.run_constants import USER_USER, ErrorResult, RunResult

from .exceptions import ModelRunError
from .exec_snippet import run


def setup_api(dp_host: str, dp_token: str, debug: bool = False, logs: TextIO = None):
    """Init the Datapane API for automated use"""
    # setup input and config
    # login, etc.
    config = c.Config(server=dp_host, token=dp_token, analytics=False)
    # datapane.init(stream_logs, verbose=args.debug)
    api.init(config=config, debug=debug, logs_stream=logs)
    # check can login/ping
    r = api.Resource(endpoint="/settings/").get()
    log.debug(f"Running DP on DP as {r.username}")


def run_api(run_config: RunnerConfig) -> RunResult:
    """Wrap the recursive calls into run"""
    # upload the report and create the RunResult
    blocks: List[api.BlockType] = run(run_config)
    report = api.Report.create(*blocks, make_public=True)

    return RunResult(report_id=report.id)


# ensure we copy PYTHONPATH across
ENV_WHITELIST = ("LANG", "PATH", "HOME", "PYTHON_VERSION", "PYTHONPATH")


def make_env(
    input_env: Mapping[str, str], allowed: Iterable[str] = ENV_WHITELIST
) -> Dict[str, str]:

    return {k: input_env[k] for k in allowed if k in input_env}


# TODO - do we still need this??
def drop_privileges(uid_name="nobody", gid_name="nogroup"):
    # from: https://stackoverflow.com/questions/2699907/dropping-root-permissions-in-python
    if os.getuid() != 0:
        return

    # Get the uid/gid from the name
    running_uid = pwd.getpwnam(uid_name).pw_uid
    running_gid = grp.getgrnam(gid_name).gr_gid

    # Remove group privileges
    os.setgroups([])

    # Try setting the new uid/gid
    os.setgid(running_gid)
    os.setuid(running_uid)

    # Ensure a very conservative umask
    os.umask(0o77)


def preexec():
    # NOTE - do we still need this??
    drop_privileges(USER_USER, USER_USER)


def parse_args(argv: Optional[List[str]] = None) -> Tuple[argparse.Namespace, List[str]]:
    # TODO - min version param
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true", default=False, help="Enable debug output")
    parser.add_argument("--config", required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--dp-host", required=True)
    parser.add_argument("--dp-token", required=True)
    parser.add_argument("--server-spec")
    return parser.parse_known_args(argv)


def version_check(server_spec_s: str, cli_version_s: str = __version__):
    """Return True if version compatible"""
    cli_version: v.Version = v.parse(cli_version_s)
    server_spec = SpecifierSet(server_spec_s)
    log.debug(f"Server spec {server_spec}, CLI version {cli_version}")
    if cli_version not in server_spec:
        raise RuntimeError(
            f"Client ({cli_version}) and Server ({server_spec}) versions not compatible"
        )


def main():
    args, unknown_args = parse_args()

    out_dir: Path = args.out_dir
    preexec()
    retcode: int

    with (out_dir / "logs.txt").open("w") as stream_logs, (out_dir / "results.json").open(
        "w"
    ) as results_stream:
        try:
            # check version
            if args.server_spec:
                version_check(args.server_spec)

            # read the config files
            # NOTE - we could supply config also by env-var or already write k8s volume in the future
            run_config = decode(args.config, compressed=True)
            setup_api(args.dp_host, args.dp_token, args.debug, stream_logs)
            res = run_api(run_config)
        except ModelRunError as e:
            ErrorResult(error=e.error, error_detail=e.details).to_json(results_stream)
            retcode = 103  # NOTE - all user errors return 103
        except Exception:
            log.exception("Unhandled Exception in Model Runner")
            # we could send traceback as details, but not useful to end user
            ErrorResult(error="Unhandled Exception", debug=traceback.format_exc()).to_json(
                results_stream
            )
            retcode = 104
        else:
            res.to_json(results_stream)
            retcode = 0

    sys.exit(retcode)


if __name__ == "__main__":
    main()
