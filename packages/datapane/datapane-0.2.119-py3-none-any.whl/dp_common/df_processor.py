import datetime
import textwrap
from io import StringIO
from numbers import Number
from typing import Any, Dict, List, TextIO

# import pyarrow as pa
import numpy as np
import pandas as pd
from pandas.errors import ParserError

from .config import empty_schema
from .dp_types import DFSchema
from .utils import log


def parse_dates(data: pd.DataFrame):
    """Tries to convert strings to dates"""
    potential_dates = data.select_dtypes(["object", "category"])

    def try_to_datetime(ser: pd.Series) -> datetime.datetime:
        return pd.to_datetime(ser, infer_datetime_format=True, errors="ignore", utc=True)

    data[potential_dates.columns] = potential_dates.apply(try_to_datetime)


def parse_categories(data: pd.DataFrame):
    """Detect and converts categories"""
    potential_cats = data.select_dtypes(object)

    def criteria(ser: pd.Series) -> bool:
        """Decides whether to convert into categorical"""
        nunique: int = ser.nunique()
        if nunique <= 20:
            # few unique values => make it a category regardless of the proportion
            return True

        prop_unique = (nunique + 1) / (ser.size + 1)  # + 1 for nan

        if prop_unique <= 0.05:
            # a lot of redundant information => categories are more compact
            return True

        return False

    def try_to_category(ser: pd.Series) -> pd.Series:
        return ser.astype("category") if criteria(ser) else ser

    data[potential_cats.columns] = potential_cats.apply(try_to_category)


def downcast_numbers(data: pd.DataFrame):
    """Downcast numerics"""

    def downcast(ser: pd.Series) -> pd.Series:
        ser = pd.to_numeric(ser, downcast="signed")
        ser = pd.to_numeric(ser, downcast="unsigned")
        return ser

    df_num = data.select_dtypes("number")
    data[df_num.columns] = df_num.apply(downcast)


def to_str(df: pd.DataFrame):
    """Converts remaining objects columns to str"""
    df_str = df.select_dtypes("object")
    df[df_str.columns] = df_str.astype(str)
    df_cat = df.select_dtypes("category")

    def to_str_cat_vals(x: pd.Series) -> pd.Series:
        if x.cat.categories.dtype == np.dtype("O"):
            x.cat.categories = x.cat.categories.astype(str)
        return x

    # make sure categorical values are strings for serialisation
    df[df_cat.columns] = df_cat.apply(to_str_cat_vals)


def process_df(df: pd.DataFrame) -> None:
    """
    Processing steps needed before writing / after reading
    NOTE - this mutates the dataframe
    """
    parse_dates(df)
    parse_categories(df)
    downcast_numbers(df)
    to_str(df)


def df_info(df: pd.DataFrame) -> Dict[str, Any]:
    """Basic structure of the dataframe, used internally"""
    # extract the Arrow schema here
    # _: pa.Schema = pa.Schema.from_pandas(df, preserve_index=False)
    # obsolete avro schema for now
    schema: DFSchema = empty_schema()

    (rows, cols) = df.shape

    return {"schema": schema, "num_rows": rows, "num_columns": cols}


def convert_csv_pd(string: str) -> pd.DataFrame:
    """Helper function to convert a well-formatted csv into a DataFrame"""
    buf: TextIO = StringIO(textwrap.dedent(string).strip())

    try:
        df = pd.read_csv(buf, engine="c", sep=",")
    except ParserError as e:
        log.warning(f"Error parsing CSV file ({e}), trying python fallback")
        df = pd.read_csv(buf, engine="python", sep=None)

    process_df(df)
    return df


def to_df(value: Any) -> pd.DataFrame:
    """Converts a python object, i.e. a script's output, to a dataframe"""
    if value is None:
        # This return the empty dataframe, which atm is the same as
        # the empty file object in the CAS.
        # However this is not ensured as pyarrow changes
        return pd.DataFrame()

    if isinstance(value, pd.DataFrame):
        # extract all indices to columns if all are not numerical and don't clash with existing column names
        col_names: List[str] = value.columns.values.tolist()
        if (
            all(
                [
                    value.index.get_level_values(x).dtype != np.dtype("int64")
                    for x in range(value.index.nlevels)
                ]
            )
            and len(set(value.index.names)) == len(value.index.names)
            and not any([x in col_names for x in value.index.names])
        ):
            value.reset_index(inplace=True)
        return value

    if isinstance(value, (pd.Series, pd.Index)):
        if value.name is not None:
            return pd.DataFrame(value)

        return pd.DataFrame({"Result": value})

    if isinstance(value, (Number, str, bool, datetime.datetime)):
        return pd.DataFrame({"Result": value}, index=[0])

    if isinstance(value, np.ndarray):
        try:
            out_df = pd.DataFrame(value)
        except ValueError:
            squeezed = np.squeeze(value)
            if squeezed.shape == ():
                # must be a scalar
                out_df = pd.DataFrame({"Result": squeezed}, index=[0])
            else:
                out_df = pd.DataFrame(squeezed)

        if out_df.columns.tolist() == [0]:
            out_df.columns = ["Result"]

        return out_df

    raise ValueError("Must return a primitive, pd.DataFrame, pd.Series or numpy array.")
