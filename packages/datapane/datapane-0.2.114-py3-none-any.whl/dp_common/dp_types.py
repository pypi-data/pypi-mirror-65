import dataclasses as dc
import typing as t
from datetime import timedelta
from os import PathLike
from pathlib import Path

__all__ = [
    "SDict",
    "SList",
    "JSON",
    "JDict",
    "JList",
    "DFSchema",
    "MIME",
    "URL",
    "NPath",
    "Hash",
    "ARROW_MIMETYPE",
    "ARROW_EXT",
    "TD_1_HOUR",
    "SECS_1_HOUR",
    "SECS_1_WEEK",
    "MountVolume",
    "REGISTRY",
]

# Typedefs
# A JSON-serialisable config object

SDict = t.Dict[str, t.Any]
SList = t.List[str]
JSON = t.Union[str, int, float, bool, None, t.Mapping[str, "JSON"], t.List["JSON"]]
JDict = SDict  # should be JSON
JList = t.List[JSON]
DFSchema = SDict
MIME = str
URL = str
NPath = t.Union[PathLike, str]
Hash = str

# Constants
# NOTE - this is a custom mimetype
ARROW_MIMETYPE: MIME = "application/vnd.apache.arrow+binary"
ARROW_EXT = ".arrow"
TD_1_HOUR = timedelta(hours=1)
SECS_1_HOUR: int = int(TD_1_HOUR.total_seconds())
SECS_1_WEEK: int = int(timedelta(weeks=1).total_seconds())
REGISTRY: str = "eu.gcr.io/datapane"


@dc.dataclass
class MountVolume:
    host_dir: Path
    container_dir: Path
    keep: bool = False
