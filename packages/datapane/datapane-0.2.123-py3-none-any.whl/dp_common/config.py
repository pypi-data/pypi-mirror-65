from __future__ import annotations

import base64
import dataclasses as dc
import datetime
import json
import zlib
from typing import Any, Dict

import dacite

from .dp_types import DFSchema, JDict, JList
from .run_constants import StepType
from .utils import log


def empty_schema() -> DFSchema:
    """Callable that returns an empty Avro schema"""
    return {"name": "x", "type": "record", "fields": []}


# TODO - move
def empty_parameter_spec() -> JList:
    return list()


@dc.dataclass
class RunnerConfig:
    """Runtime config for a form/form, including user props"""

    code: str = ""
    config: JDict = dc.field(default_factory=dict)
    formats: JDict = dc.field(default_factory=dict)

    def _format(self, format: str, v: Any) -> Any:
        """Convert a config object using the specified formats"""
        if v is not None:
            if format == "date":
                return datetime.date.fromisoformat(v)
            elif format == "time":
                utc_t: str = v.replace("Z", "+00:00")
                return datetime.time.fromisoformat(utc_t)
            elif format == "date-time":
                utc_t: str = v.replace("Z", "+00:00")
                return datetime.datetime.fromisoformat(utc_t)
            else:
                log.debug(f"Unknown config format {format}")
        return v

    def format(self) -> JDict:
        """Convert a config object using the specified formats"""
        conf: JDict = self.config.copy()
        format: str
        for (name, format) in self.formats.items():
            conf[name] = self._format(format, conf.get(name))
        return conf

    @classmethod
    def create(cls, config: Dict) -> RunnerConfig:
        _config = config  # {snakecase(k): v for (k, v) in config.items()}
        d_config = dacite.Config(type_hooks={StepType: StepType})
        return dacite.from_dict(cls, data=_config, config=d_config)


# NOTE - any reason we don't use pickle here?
def encode(config: RunnerConfig, compressed: bool) -> str:
    """Encode model and user config into a serialised string"""
    _config = json.dumps(dc.asdict(config))
    if compressed:
        return base64.b64encode(zlib.compress(_config.encode())).decode()
    else:
        return _config


def decode(config: str, compressed: bool) -> RunnerConfig:
    """Decode config into model and user config from a serialised string"""
    if compressed:
        config = zlib.decompress(base64.b64decode(config.encode())).decode()
    return RunnerConfig.create(json.loads(config))
