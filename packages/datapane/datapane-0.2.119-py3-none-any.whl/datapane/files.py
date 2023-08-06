"""
Creating charts.
---------------

We recommend using Altair/pdvega for generating interactive charts: use the supplied `save`
function.

Example
-------

altair_pandas::
  # uses the default pandas plotting API
  from datapane.files import save

  import numpy as np

  pd.set_option('plotting.backend', 'altair')  # Installing altair_pandas registers this.

  data = pd.DataFrame({'x': np.random.randn(200),
                       'y': np.random.randn(200)})

  plot = data.plot.scatter('x', 'y')
  save(plot, "scatter")

pdvega::

  from datapane.files import save

  import numpy as np
  import pdvega

  data = pd.DataFrame({'x': np.random.randn(200),
                       'y': np.random.randn(200)})

  plot = data.vgplot.scatter('x', 'y')
  save(plot, "scatter")

altair::

  from datapane.files import save

  import altair as alt
  import numpy as np

  data = pd.DataFrame({'x': np.random.randn(20),
                      'y': np.random.randn(20)})
  plot = alt.Chart(data).mark_bar().encode(
      y='y',
      x='x'
  )

  save(plot, "bars")

Also for your convenience the `save` function is compatible with matplotlib figures, Bokeh Figures, and pandas dataframes (it saves a table in this instance).

Example
-------

::

  from datapane.files import save

  import matplotlib.pyplot as plt

  fig, ax = plt.subplots()
  ax.plot([1, 2, 3, 4], [1, 4, 9, 16])
  save(figure, "line.svg")
  out_df = in_df
"""

import abc
import json
from functools import singledispatch
from pathlib import Path
from typing import Any, Optional, TextIO, TypeVar, Union

import matplotlib.pyplot as plt
import pandas as pd
from altair.utils import SchemaBase
from bokeh.embed import json_item
from bokeh.plotting.figure import Figure as BFigure
from matplotlib.figure import Axes, Figure
from numpy import ndarray

from dp_common import log

T = TypeVar("T")
NPath = Union[Path, str]
MIME_TYPE_ATTR = "user.mime_type"
PLAIN_TEXT = "text/plain"
RESULT_COUNTER: int = 1


class BasePlot(abc.ABC):
    mimetype: str
    ext: str
    fig_type: T

    # @staticmethod
    # def _set_mimetype(filename: Path, mimetype: str) -> None:
    #     with suppress(OSError):
    #         # NOTE: doesn't work if run in tmpfs
    #         setxattr(str(filename), MIME_TYPE_ATTR, mimetype.encode("utf8"))

    def write(self, file_name: NPath, x: T) -> Path:
        fn = Path(file_name).with_suffix(self.ext)
        with fn.open("w") as f:
            self.write_file(f, x)
        # self._set_mimetype(fn, self.mimetype)
        return fn

    def write_file(self, f: TextIO, x: T):
        pass


class MatplotBasePlot(BasePlot):
    def _write_figure(self, file_name: NPath, x: Figure) -> Path:
        """ Creates an image from figure

        :param file_name: Name of the file.
        :param x: Matplotlib figure, can be created by `plt.figure() or plt.gcf() for the global`.
        """

        # let matplotlib guess the format from extension, defaulting to svg if none present
        fn = Path(file_name)
        if not fn.suffix:
            fn = fn.with_suffix(".svg")
        x = x or plt.gcf()
        x.savefig(str(fn))
        return fn


class MatplotFigurePlot(MatplotBasePlot):
    fig_type = Figure

    def write(self, file_name: NPath, x: Figure) -> Path:
        return super()._write_figure(file_name, x)


class MatplotAxesPlot(MatplotBasePlot):
    fig_type = Axes

    def write(self, file_name: NPath, x: Axes) -> Path:
        f: Figure = x.get_figure()
        return super()._write_figure(file_name, f)


class MatplotNDArrayPlot(MatplotBasePlot):
    fig_type = ndarray

    def write(self, file_name: NPath, x: ndarray) -> Path:
        f: Figure = x.flatten()[0].get_figure()
        return super()._write_figure(file_name, f)


class TablePlot(BasePlot):
    """Creates an html table from the dataframe"""

    mimetype = "application/vnd.nstack.table+html"
    ext = ".html"
    fig_type = pd.DataFrame
    TABLE_CELLS_LIMIT: int = 2000

    def write_file(self, f: TextIO, dataframe: pd.DataFrame):
        n_cells = dataframe.shape[0] * dataframe.shape[1]
        if n_cells > self.TABLE_CELLS_LIMIT:
            log.warning(
                f"Dataframe is has more than {self.TABLE_CELLS_LIMIT} cells. Omitting output."
            )
            # TODO - this should truncate rather than replace
            f.write(
                f"<table><tr><td>omitted as over {self.TABLE_CELLS_LIMIT} cells</td></tr></table>"
            )
        else:
            dataframe.to_html(f)


class BokehPlot(BasePlot):
    """Returns an interactive Bokeh application"""

    mimetype = "application/vnd.bokeh.show+json"
    ext = ".bokeh.json"
    fig_type = BFigure

    def write_file(self, f: TextIO, app: BFigure):
        json.dump(json_item(app), f)


class AltairPlot(BasePlot):
    """Creates a vega-light chart from Altair Chart / pdvega Axes object."""

    mimetype = "application/vnd.vegalite.v3+json"
    ext = ".vl.json"
    fig_type = SchemaBase

    def write_file(self, f: TextIO, chart: SchemaBase):
        json.dump(chart.to_dict(), f)


# register all the plot types
plots = [TablePlot, BokehPlot, AltairPlot, MatplotFigurePlot, MatplotAxesPlot, MatplotNDArrayPlot]


@singledispatch
def get_plotter(figure: Any) -> BasePlot:
    raise NotImplementedError(f"Type {type(figure)} not supported.")


for p in plots:
    get_plotter.register(p.fig_type, lambda _, p=p: p())


def show(figure: Any, filename: Optional[NPath] = None) -> Path:
    global RESULT_COUNTER
    if not filename:
        filename = f"results_{RESULT_COUNTER:03d}"
        RESULT_COUNTER += 1

    return get_plotter(figure).write(filename, figure)
