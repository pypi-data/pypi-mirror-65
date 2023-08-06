import ast
import builtins
from functools import partial
from pathlib import Path
from types import FrameType
from typing import List

from munch import Munch

import datapane.api as api
from datapane.files import show
from dp_common import SDict, log
from dp_common.config import RunnerConfig

from .exceptions import CodeRaisedError, CodeSyntaxError

ENVIRON_CONFIG = {"banned_builtins": {"compile", "exec", "eval"}, "default_environment": []}
USER_CODE_NAME = "<snippet>"


def filter_frame_by_filename(filename: str, frame: FrameType) -> bool:
    return frame.f_code.co_filename == filename


################################################################################
# Misc
def gen_df_describe(df, fn: Path):
    try:
        desc = df.describe(include="all")
        show(desc, filename=fn)
    except ValueError:
        log.debug("Couldn't generate dataframe stats for empty dataframe")


def run(run_config: RunnerConfig) -> List[api.BlockType]:
    """Snippet - run a python function embedded within in the snippet config field"""
    code = run_config.code
    user_config: SDict = Munch.fromDict(run_config.format())
    # call to_df locally
    # convert to dfs if needed
    # dp._snippet_init(config=user_config)

    # NOTE(MG): currently just exec the script - do we need to load it as a module via importlib?
    try:
        # pass in 'snippet_name' explicitly as we depend on it below.
        init_state: SDict = {"params": user_config, "parameters": user_config, "on_datapane": True}
        res_scope = exec_user_script(code, init_state, snippet_name=USER_CODE_NAME)

        # call render function/extract report var
        if "render" in res_scope:
            report = res_scope["render"]()
        elif "report" in res_scope:
            report = res_scope["report"]
        else:
            log.warning("report variable nor render function found in script")
            report = []
        return report
    except SyntaxError:
        raise CodeSyntaxError.from_exception()
    except Exception:
        raise CodeRaisedError.from_exception(partial(filter_frame_by_filename, USER_CODE_NAME))


################################################################################
# internal
def exec_user_script(script, init_scope: SDict, snippet_name=USER_CODE_NAME) -> SDict:
    a = ast.parse(script, snippet_name, "exec")
    ast_validation(a)
    c = compile(a, snippet_name, "exec")
    globalscope = {
        # "df": single_input,
        # "params": Munch(config),
        "__builtins__": override_builtins(__import__)
    }
    globalscope.update(init_scope)
    exec(c, globalscope, globalscope)
    return globalscope


def ast_validation(node):
    for n in ast.walk(node):
        # TODO: implement check for import statements
        if isinstance(n, ast.Import):
            pass
        if isinstance(n, ast.ImportFrom):
            pass


class OverriddenBuiltins(dict):
    def __getitem__(self, name):
        if name in ENVIRON_CONFIG["banned_builtins"]:
            raise RuntimeError("Illegal builtin {}".format(name))
        return super().__getitem__(name)


def override_builtins(importer):
    b = OverriddenBuiltins(builtins.__dict__)
    b["__import__"] = importer
    return b


def importer(name, *x, **y):
    rootpkg = name.split(".")[0]
    if rootpkg not in ("dp_runner",):  # TODO: module check
        return builtins.__import__(name, *x, **y)
    raise ImportError("Cannot import banned module")
