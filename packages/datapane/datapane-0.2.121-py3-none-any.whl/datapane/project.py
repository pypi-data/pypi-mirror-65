"""Support for handling datapane script projects"""

import dataclasses as dc
import json
import re
import sys
from pathlib import Path
from typing import List, Optional

import dacite
import jsonschema
import yaml

from dp_common import SDict, log

# app paths
sys_dir = Path(sys.executable if getattr(sys, "frozen", False) else __file__).parent
res_dir = sys_dir / "resources"
DATAPANE_YAML = Path("datapane.yaml")
DEFAULT_PY = Path("template.py")
DEFAULT_IPYNB = Path("template.ipynb")
re_check_name = re.compile("^[a-z0-9-_]+$")


def get_res_path(res_name: str) -> Path:
    return res_dir / res_name


def validate_name(x: str):
    if re_check_name.match(x) is None:
        raise AssertionError(f"'{x}' is not a valid service name, must be [a-z0-9-_]")


def default_title() -> str:
    return "New Untitled Script"


@dc.dataclass
class DatapaneCfg:
    """Wrapper around the datapane config file"""

    name: str = "cmdline"
    script: Path = dc.field(
        default_factory=lambda: DEFAULT_IPYNB if DEFAULT_IPYNB.exists() else DEFAULT_PY
    )
    docker_image: Optional[str] = None
    parameters: List[SDict] = dc.field(default_factory=list)
    title: str = dc.field(default_factory=default_title)
    public: bool = False

    def __post_init__(self):
        validate_name(self.name)

        # validate config
        if self.parameters:
            config_schema = json.loads(get_res_path("script_parameter_def.schema.json").read_text())
            jsonschema.validate(self.parameters, config_schema)

    @classmethod
    def create(cls, config_file: Path = DATAPANE_YAML, **kw) -> "DatapaneCfg":
        if config_file.exists():
            log.debug(f"Reading datapane config file at {config_file}")
            with config_file.open("r") as f:
                config = yaml.safe_load(f)
        else:
            config = {}
        config.update(kw)
        return dacite.from_dict(cls, data=config)

    @staticmethod
    def exists() -> bool:
        return DATAPANE_YAML.exists()

    def to_dict(self) -> SDict:
        d = dc.asdict(self)
        return d
