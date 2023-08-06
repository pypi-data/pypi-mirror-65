"""
Data filters filter out data that is of dubious quality and should not be trained on.
Feature selection contains feature filters that are used to get rid of undesirable features.
"""

import json
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple, Union

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer

from dp_common.df_processor import parse_dates

ColumnFilterReturn = List[str]
ReportColumnEntry = List[Tuple[ColumnFilterReturn, str]]
ReportRowEntry = List[Tuple[pd.Index, str]]
ReportProcessEntry = List[str]


@dataclass
class Report:
    """Class that records the output of row, column filters and data processors."""

    df: pd.DataFrame
    columns_to_remove: ReportColumnEntry = field(default_factory=list)
    row_numbers_to_remove: ReportRowEntry = field(default_factory=list)
    processed_reports: ReportProcessEntry = field(default_factory=list)

    def to_dict(self) -> Dict:
        """Serialise into a succinct summary dictionary"""
        rows_removed: List[str] = []
        columns_removed: List[str] = []
        dataset_changed: List[str] = []

        row_numbers_to_remove: pd.Index
        for row_numbers_to_remove, reason in self.row_numbers_to_remove:
            # row_numbers_to_remove are 0-indexed row numbers, but this is unnatural for most
            # people: 0'th row makes little sense as opposed to 1st row
            examples = row_numbers_to_remove[:5] + 1
            examples_end = "..." if len(row_numbers_to_remove) > 5 else ""
            examples_string = ", ".join([str(x) for x in examples]) + examples_end

            rows_removed.append(f"{reason}: {examples_string}")

        for cols, reason in self.columns_to_remove:
            col_names = ", ".join(cols)
            columns_removed.append(f"{col_names}: {reason}")

        for reason in self.processed_reports:
            dataset_changed.append(reason)

        return dict(
            rows_removed=rows_removed,
            columns_removed=columns_removed,
            dataset_changed=dataset_changed,
        )

    def to_json(self) -> str:
        """Serialise into a succinct summary json"""
        return json.dumps(self.to_dict())

    def take_subdf(self) -> pd.DataFrame:
        """Take groups of unfiltered columns and rows according to report"""
        columns_to_remove: Set = set()
        for cols_to_remove, _ in self.columns_to_remove:
            columns_to_remove |= set(cols_to_remove)
        df = self.df[[x for x in self.df.columns if x not in columns_to_remove]]

        index = df.reset_index().index
        row_numbers_to_remove: pd.Index
        for row_numbers_to_remove, _ in self.row_numbers_to_remove:
            index = index.difference(row_numbers_to_remove)

        return df.iloc[index]  # filtered df


class Action(ABC):
    reason: Optional[str] = None

    def __init__(self, report: Report):
        self.report = report
        self.df: pd.DataFrame = report.df

    def run(self, *args, **kwargs):
        ...

    def process(self, *args, **kwargs):
        ...


class ColumnFilter(Action):
    def __init__(self, report: Report, columns_to_keep: Optional[List[str]] = None):
        super().__init__(report)
        self.columns_to_keep = columns_to_keep or []

    def run(self, *args, **kwargs):
        cols_to_remove = self.process(*args, **kwargs)
        if len(cols_to_remove) != 0:
            self.report.columns_to_remove.append((cols_to_remove, self.reason))

    @abstractmethod
    def process(self, *args, **kwargs) -> ColumnFilterReturn:
        ...


class RowFilter(Action):
    def run(self, *args, **kwargs):
        indices_to_remove = self.process(*args, **kwargs)
        if len(indices_to_remove) != 0:
            self.report.row_numbers_to_remove.append(
                (self.index_to_row_numbers(indices_to_remove), self.reason)
            )

    @abstractmethod
    def process(self, *args, **kwargs) -> pd.Index:
        ...

    def index_to_row_numbers(self, index: pd.Index) -> pd.Index:
        """
        Auxiliary function that converts pandas' index to row numbers. We find row numbers
        easier to work with: report surfaces row numbers to clients.
        """
        return pd.Index(
            pd.Series(range(len(self.df)), index=self.df.index).loc[index], dtype="int64"
        )


class Processor(Action):
    def run(self, *args, **kwargs):
        self.process(*args, **kwargs)
        if self.reason:
            self.report.processed_reports.append(self.reason)


class ProcessImpute(Processor):
    """Impute missing with the given sentinel"""

    def fillna(self, value):
        """Pandas' fillna that deals with categories"""
        categorical = self.df.select_dtypes("category")
        if not categorical.empty:
            self.df.loc[:, categorical.columns] = categorical.apply(
                lambda x: x.cat.add_categories(value)
            )
        self.df.fillna(value, inplace=True)

    def process(self, impute_strategy: Optional[str] = "constant", impute_sentinel: Any = None):
        if impute_strategy == "constant" or impute_strategy is None:
            if impute_sentinel is None:
                self.reason = None
                return

            self.reason = f"missing data imputed with {impute_sentinel}"
            self.fillna(impute_sentinel)
            return

        elif impute_strategy in ["backfill", "bfill", "pad", "ffill"]:
            self.reason = f"missing data imputed with {impute_strategy} strategy"
            self.df.fillna(method=impute_strategy, inplace=True)

        elif impute_strategy in ["mean", "median", "most_frequent"]:
            df_num = self.df.select_dtypes("number")
            self.reason = f"missing data imputed with {impute_strategy} strategy"
            if not df_num.empty:
                self.df[df_num.columns] = SimpleImputer(strategy=impute_strategy).fit_transform(
                    df_num
                )

        else:
            raise NotImplementedError(f"imputation strategy {impute_strategy} not recognised")

        if impute_sentinel is not None:
            self.reason += f"; remaining missing replaced with {impute_sentinel}"
            self.fillna(impute_sentinel)


class ProcessCastToString(Processor):
    """Cast specifies columns to string"""

    def process(self, columns: Optional[List[str]] = None):
        if columns is None:
            return

        self.reason = f"columns {columns} converted to string type"
        self.df[columns] = self.df[columns].astype(str)


class ProcessFixNulls(Processor):
    """Detect a null sentinel and reparse numeric columns"""

    def process(self):
        pattern = re.compile(r'Unable to parse string "(.*)" at position .*')
        null_candidates = []
        for col in self.df.columns:
            try:
                if pd.to_numeric(self.df[col], errors="coerce").isnull().all():
                    # column doesn't have any numeric values!
                    continue

                pd.to_numeric(self.df[col])
            except ValueError as e:
                match = pattern.match(e.args[0])
                if match:
                    null_candidates.append(match.group(1))

        # filter dates out - never a good sentinel
        null_candidates = [
            x for x in null_candidates if isinstance(pd.to_datetime(x, errors="ignore"), str)
        ]

        if not null_candidates:
            self.reason = "no null sentinel detected"
            return

        most_common = max(set(null_candidates), key=null_candidates.count)

        self.reason = f"{most_common} was detected to represent null values"
        self.df.replace(most_common, np.nan, inplace=True)
        df_subset = self.df.select_dtypes(["object", "category"])

        def to_numeric(ser):
            """Needed because pd.to_numeric coerces categories into strings"""
            was_caterical = hasattr(ser, "cat")
            new = pd.to_numeric(ser, errors="ignore")
            is_object = new.dtype == np.dtype("O")
            if was_caterical and is_object:
                return ser
            return new

        self.df[df_subset.columns] = df_subset.apply(lambda x: to_numeric(x))


class ProcessConvertDates(Processor):
    """Detect all date columns and convert them to dates"""

    def process(self):
        parse_dates(self.df)


class ProcessCastToNumeric(Processor):
    """Tries to convert string columns into numeric."""

    def process(self):
        df_subset = self.df.select_dtypes("object")
        if df_subset.empty:
            return

        self.reason = f"tried casting {', '.join(df_subset.columns.tolist())} to numeric"
        self.df[df_subset.columns] = df_subset.apply(lambda x: pd.to_numeric(x, errors="ignore"))


class FilterFutureDates(RowFilter):
    """Removes rows that contains future dates."""

    def process(self, current_datetime=pd.to_datetime("now", utc=True)) -> pd.Index:
        index_removed_rows = pd.Index([], dtype="int64")

        date_columns_naive = self.df.select_dtypes("datetime").columns.tolist()
        for col in date_columns_naive:
            index_removed_rows |= self.df.index[self.df[col] > current_datetime.tz_convert(None)]

        date_columns_tz = self.df.select_dtypes("datetimetz").columns.tolist()
        for col in date_columns_tz:
            index_removed_rows |= self.df.index[self.df[col] > current_datetime]

        date_columns = date_columns_naive + date_columns_tz
        self.reason = f"future dates present in columns - {', '.join(date_columns)}"
        return index_removed_rows


class FilterReactivations(RowFilter):
    reason = "user was active after the cancellation"

    def process(
        self,
        id_column_name: str = "user_id",
        date_column_name: str = "date",
        cancelled_column_name: str = "cancelled",
    ) -> RowFilter:
        """
        Removes rows that have multiple cancellation. Used to only keep the latest subscription for
        any given customer.

        Example:
            user_id,       date, cancelled
                10, 2015-06-01,     False # <--should be removed because of reactivation below
                10, 2015-06-02,     True  # <--should be removed because of reactivation below
                10, 2015-06-20,     False # <- reactivation => should be kept
                10, 2015-06-21,     True  # <- part of the last period => should be kept
        """
        sorted_df = self.df.sort_values([id_column_name, date_column_name, cancelled_column_name])

        def nullify_reactivations(cancelled):
            reindexed = cancelled.reset_index(drop=True)
            # we are going to keep the last entry no matter what
            cancelled_without_last = reindexed[:-1]
            # keep True only: i.e. those rows that have multiple cancellation
            cancelled_without_last = cancelled_without_last[cancelled_without_last]
            # more than one True was found: nullify everything after penultimate True
            if len(cancelled_without_last) > 0:
                last_true_index = cancelled_without_last.index[-1]
                cancelled.iloc[0 : last_true_index + 1] = np.nan
            return cancelled

        grouped = sorted_df.groupby(id_column_name)[cancelled_column_name]
        nullified_reactivations = grouped.transform(nullify_reactivations)
        index_removed_rows = nullified_reactivations.index[nullified_reactivations.isnull()]
        return index_removed_rows


class FilterOutliers(RowFilter):
    reason = "observation had extreme values"

    def process(self, z_threshold: float = 3, proportion_columns: float = 2 / 3) -> pd.Index:
        """
        Removes rows that are considered as outliers. An outlier is defined as an observation that
        has too many of its feature values above the z_threshold value.

        Parameters:
        -----------
        z_threshold : float
            This is the z_score used to determine what value is an outlier. Usually 3 (= 3 standard
            deviations away from the mean) is used as a default value.

        proportion_columns : float
            If the ratio: (total number of columns where the feature value exceed z_threshold /
            total number of features), is over or equal to proportion_columns, we remove the
            corresponding row.
        """
        df_subset = self.df.select_dtypes("number")
        z_scores = ((df_subset - df_subset.mean()) / df_subset.std()) > z_threshold
        mask_outlier = z_scores.mean(axis=1) >= proportion_columns

        index_removed_rows = df_subset[mask_outlier].index
        return index_removed_rows


class FilterMissing(RowFilter):
    """Removes rows that contain one or more missing values."""

    def process(self):
        self.reason = "contains missing values"
        mask_missing = self.df.isnull().any(axis=1)
        index_removed_rows = mask_missing[mask_missing].index
        return index_removed_rows


class FilterNullColumns(ColumnFilter):
    """Removes columns that are mostly null."""

    def process(self, threshold_missing_prop: float = 0.95) -> ColumnFilterReturn:
        cols_to_remove = []
        self.reason = f"more than {threshold_missing_prop * 100:0.0f}% missing"
        for col in set(list(self.df.columns)) - set(self.columns_to_keep):
            missing_prop = self.df[col].isnull().mean()
            if missing_prop > threshold_missing_prop:
                cols_to_remove.append(col)

        return cols_to_remove


class FilterCorrelatedColumns(ColumnFilter):
    """Removes columns that are highly correlated with the other columns."""

    def process(self, threshold: float = 0.95) -> ColumnFilterReturn:
        self.reason = f"correlation with some other column is above {threshold}"
        corr_matrix = self.df.corr().abs()
        upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(np.bool))
        cols_to_remove = [
            c for c in upper.columns if any(upper[c] > 0.95) and c not in self.columns_to_keep
        ]
        return cols_to_remove


class FilterConstColumns(ColumnFilter):
    """Removes columns that don't change (either globally or don't change in each group)"""

    def process(self, groupby: Optional[Union[List[str], str]] = None) -> ColumnFilterReturn:
        if groupby is not None:
            self.reason = f"columns don't change for each {groupby}"
            nunique = self.df.groupby(groupby).nunique(dropna=False)
            t = (nunique == 1).all()
            columns = nunique.columns
        else:
            self.reason = "columns are constant"
            t = self.df.nunique(dropna=False) == 1
            columns = self.df.columns

        const_features = [x for x in columns[t] if x not in self.columns_to_keep]
        return const_features


class FilterStringColumns(ColumnFilter):
    """Removes columns that are strings"""

    reason = "columns are strings"

    def process(self) -> ColumnFilterReturn:
        df_subset = self.df.select_dtypes("object")
        cols_to_remove = [x for x in df_subset.columns if x not in self.columns_to_keep]
        return cols_to_remove


class FilterLowVarianceColumns(ColumnFilter):
    """Removes columns with variance below a given threshold."""

    def process(self, threshold_low_variance: float = 0.0) -> ColumnFilterReturn:
        cols_to_remove = []
        self.reason = f"variance below {threshold_low_variance:0.0f}"
        df_subset = self.df.select_dtypes("number")
        df_subset = df_subset[[x for x in df_subset.columns if x not in self.columns_to_keep]]
        for col in df_subset.columns:
            var = self.df[col].var()
            if var <= threshold_low_variance:
                cols_to_remove.append(col)

        return cols_to_remove


class FilterDuplicates(RowFilter):
    """Removes duplicate rows"""

    reason = "duplicate row"

    def process(self) -> pd.Index:
        dedupe = self.df.drop_duplicates()
        return self.df.index.drop(dedupe.index)
