# NOTE - this is a bit hacky as symlinked across modules
import logging
import mimetypes
import os
import subprocess
import sys
import time
import typing as t
from contextlib import contextmanager
from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory, mkstemp

from colorlog import ColoredFormatter

from .dp_types import NPath

__all__ = [
    "log",
    "get_logger",
    "setup_logging",
    "log_command",
    "create_temp_file",
    "temp_fname",
    "compress_file",
    "temp_workdir",
    "pushd",
    "unixtime",
]


mimetypes.init()


################################################################################
# Logging
logging.getLogger().disabled = True  # disable the root logger

# export the default application logger
log: logging.Logger = logging.getLogger("datapane")
get_logger: t.Callable[..., logging.Logger] = log.getChild


def setup_logging(verbose_mode: bool, logs_stream: t.TextIO = None) -> None:
    """Call to configure logging outside of django for scripts / tasks"""
    global log
    # log.propagate = False
    log.setLevel(logging.DEBUG if verbose_mode else logging.INFO)
    log_formatter = ColoredFormatter(
        "%(blue)s%(asctime)s%(reset)s [%(log_color)s%(levelname)-5s%(reset)s] %(message)s",
        datefmt="%H:%M:%S",
        reset=True,
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red,bg_white",
        },
        secondary_log_colors={},
        style="%",
    )

    log.handlers.clear()

    # file output
    # fileHandler = logging.FileHandler(LOGFILE, mode='w')
    # fileHandler.setFormatter(log_formatter)
    # log.addHandler(fileHandler)

    # console
    console_handler = logging.StreamHandler(stream=logs_stream or sys.stdout)
    console_handler.setFormatter(log_formatter)
    log.addHandler(console_handler)


@contextmanager
def log_command(command: str) -> t.ContextManager[None]:
    """Log an internal process"""
    log.info(f"Starting {command}")
    yield
    log.info(f"Finished {command}")


@contextmanager
def create_temp_file(
    suffix: str, prefix: str = "datapane-temp-", mode: str = "w+b"
) -> t.ContextManager[NamedTemporaryFile]:
    """Creates a NamedTemporaryFile that doesn't disappear on .close()"""
    temp_file = NamedTemporaryFile(suffix=suffix, prefix=prefix, mode=mode, delete=False)
    try:
        yield temp_file
    finally:
        os.unlink(temp_file.name)


@contextmanager
def temp_fname(
    suffix: str, prefix: str = "datapane-temp-", keep: bool = False
) -> t.ContextManager[str]:
    """Wrapper to generate a temporary filename only that is deleted on leaving context"""
    (in_f, in_f_name) = mkstemp(suffix=suffix, prefix=prefix)
    try:
        os.close(in_f)
        yield in_f_name
    finally:
        if not keep:
            os.unlink(in_f_name)


@contextmanager
def compress_file(f_name: str, level: int = 6) -> t.ContextManager[str]:
    """Return path to a compressed version of the input filename"""
    subprocess.run(["gzip", "-kf", f"-{level}", f_name], check=True)
    f_name_gz = f"{f_name}.gz"
    try:
        yield f_name_gz
    finally:
        os.unlink(f_name_gz)


@contextmanager
def temp_workdir() -> t.ContextManager[None]:
    """Set working dir to a tempdir for duration of context"""
    with TemporaryDirectory() as tmp_dir:
        curdir = os.getcwd()
        os.chdir(tmp_dir)
        try:
            yield None
        finally:
            os.chdir(curdir)


@contextmanager
def pushd(directory: NPath) -> t.ContextManager[None]:
    """Switch dir and push it onto the (call-)stack"""
    cwd = os.getcwd()
    log.debug(f"[cd] {cwd} -> {directory}")
    os.chdir(directory)
    try:
        yield
    finally:
        log.debug(f"[cd] {cwd} <- {directory}")
        os.chdir(cwd)


def unixtime() -> int:
    return int(time.time())


def get_filesize(filename: Path) -> int:
    return filename.stat().st_size


def guess_type(filename: Path) -> str:
    mtype, _ = mimetypes.guess_type(str(filename))
    return mtype or "application/octet-stream"


def mimetype_for_file(filename: Path) -> str:
    try:
        # attempt to read from extended attributes
        import xattr

        mtype_b = xattr.getxattr(str(filename), "user.mime_type")
        if mtype_b:
            return mtype_b.decode("utf8")
    except (ImportError, IOError):
        pass
    return guess_type(filename)


def walk_path(path: Path) -> t.Iterable[Path]:
    for p in path.rglob("*"):
        if not p.is_dir():
            yield p
