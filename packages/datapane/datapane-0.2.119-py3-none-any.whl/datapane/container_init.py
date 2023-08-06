# TODO - do we make as main __init__ - or call this when we're running on datapane?
"""Public API for use from models / snippets"""
import logging
from typing import List

import pandas as pd
from munch import Munch

log = logging.getLogger("model")


class ObsoleteAPIError(Exception):
    pass


def init(out_stream, verbose: bool):
    """
    Sets up the datapane_dp helper lib
    """

    # configure the app logger
    ch = logging.StreamHandler(stream=out_stream)
    formatter = logging.Formatter("%(asctime)s %(levelname)8s %(name)s: %(message)s")
    ch.setFormatter(formatter)
    log.addHandler(ch)
    log.setLevel(logging.DEBUG if verbose else logging.INFO)
    log.propagate = False

    log.info("mod init")


# External module API (plus imports above)

# OK - this is very hacky - but we can fuck around with globals in the short-term
# so long as only modify/mutate existing references rather than create new values
__in_datasets: List[pd.DataFrame] = []
__config: Munch = Munch()
_out_datasets: List[pd.DataFrame] = []

datasets = __in_datasets
config = __config


def _snippet_init(in_datasets: List[pd.DataFrame], config: Munch):
    log.info("snippet init")
    global __in_datasets
    # __in_datasets: List[pd.DataFrame]
    __in_datasets.extend(in_datasets)

    global __config
    # __config: Munch
    __config.update(config)


# show imported from files
def save(df: pd.DataFrame):
    global _out_datasets
    # _out_datasets: List[pd.DataFrame]
    _out_datasets.append(df)
