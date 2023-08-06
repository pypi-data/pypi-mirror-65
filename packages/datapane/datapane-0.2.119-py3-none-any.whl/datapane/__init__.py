from ._version import __rev__, __version__  # noqa: F401
from .api import Asset, Blob, Plot, Report, Script, Table, init  # noqa: F401

# call init if in jupyter/interactive mode
# TODO - do we want to init only in jupyter / interactive / etc.
init()
