"""
Optimal binning algorithm in Spark.
"""

# Guillermo Navas-Palencia <g.navas.palencia@gmail.com>
# Copyright (C) 2020

import time

import numpy as np

from ...logging import Logger
from ..binning import _check_parameters
from ..binning import OptimalBinning
from ..binning_statistics import bin_info
from ..binning_statistics import BinningTable

try:
    import pyspark.sql.functions as func

    from pyspark.ml.feature import QuantileDiscretizer
    from pyspark.sql.dataframe import DataFrame

    PYSPARK_AVAILABLE = True
except ImportError:
    PYSPARK_AVAILABLE = False


class OptimalBinningSpark(OptimalBinning):
    def __init__(self, variable, target, dtype="numerical", name="",
                 solver="cp", prebinning_eps=0.001, max_n_prebins=20,
                 min_n_bins=None, max_n_bins=None, min_bin_size=None,
                 max_bin_size=None, min_bin_n_nonevent=None,
                 max_bin_n_nonevent=None, min_bin_n_event=None,
                 max_bin_n_event=None, monotonic_trend="auto",
                 min_event_rate_diff=0, max_pvalue=None,
                 max_pvalue_policy="consecutive", gamma=0, special_codes=None,
                 time_limit=100, verbose=False):

        self.variable = variable
        self.target = target
        self.dtype = dtype
        self.name = name
        
        self.solver = solver

        self.prebinning_eps = prebinning_eps
        self.max_n_prebins = max_n_prebins

        self.min_n_bins = min_n_bins
        self.max_n_bins = max_n_bins
        self.min_bin_size = min_bin_size
        self.max_bin_size = max_bin_size
        self.min_bin_n_event = min_bin_n_event
        self.max_bin_n_event = max_bin_n_event
        self.min_bin_n_nonevent = min_bin_n_nonevent
        self.max_bin_n_nonevent = max_bin_n_nonevent

        self.monotonic_trend = monotonic_trend
        self.min_event_rate_diff = min_event_rate_diff
        self.max_pvalue = max_pvalue
        self.max_pvalue_policy = max_pvalue_policy
        self.gamma = gamma

        self.special_codes = special_codes

        self.time_limit = time_limit
        
        self.verbose = verbose

        # auxiliary
        self._categories = None
        self._cat_others = None
        self._n_event = None
        self._n_nonevent = None
        self._n_nonevent_missing = None
        self._n_event_missing = None
        self._n_nonevent_special = None
        self._n_event_special = None
        self._n_nonevent_cat_others = None
        self._n_event_cat_others = None
        self._user_splits = None
        self._user_splits_fixed = None

        # info
        self._binning_table = None
        self._n_prebins = None
        self._n_refinements = 0
        self._n_samples = None
        self._optimizer = None
        self._splits_optimal = None
        self._status = None

        # timing
        self._time_total = None
        self._time_preprocessing = None
        self._time_prebinning = None
        self._time_solver = None
        self._time_postprocessing = None

        self._is_fitted = False

    def fit(self, df):
        return self._fit(df)

    def _fit(self, df):
        # Check Spark availability
        if not PYSPARK_AVAILABLE:
            raise ImportError('Cannot import pyspark. Install pyspark or '
                              'choose data streaming alternative.')

        time_init = time.perf_counter()

        # _check_parameters(**self.get_params())

        # Pre-processing
        self._check_input(df)

        self._columns = [self.variable, self.target]

        time_preprocessing = time.perf_counter()
        # df_clean, df_missing, df_special = split_data()
        self._time_preprocessing = time.perf_counter() - time_preprocessing

        # Pre-binning
        time_prebinning = time.perf_counter()

        splits, n_nonevent, n_event = self._fit_prebinning(df)

        self._n_prebins = len(n_nonevent)

        self._time_prebinning = time.perf_counter() - time_prebinning

        # Optimization
        self._fit_optimizer(splits, n_nonevent, n_event)        

        # Post-processing # TODO: reuse optimalbinning
        time_postprocessing = time.perf_counter()

        # self._postprocessing(n_nonevent, n_event)

        self._n_nonevent, self._n_event = bin_info(
            self._solution, n_nonevent, n_event, self._n_nonevent_missing,
            self._n_event_missing, self._n_nonevent_special,
            self._n_event_special, 0, 0, [])

        self._binning_table = BinningTable(
            self.name, self.dtype, self._splits_optimal, self._n_nonevent,
            self._n_event, self._categories, self._cat_others, None)

        self._time_postprocessing = time.perf_counter() - time_postprocessing

        self._time_total = time.perf_counter() - time_init

        self._is_fitted = True

        return self

    def fit_transform(self, df, metric="woe", metric_special=0,
                      metric_missing=0):
        
        return self.fit(df).transform(
            df, metric, metric_special, metric_missing)

    def transform(self, df, metric="woe", metric_special=0,
                  metric_missing=0):
        pass

    def _check_input(self, df):
        if not isinstance(df, DataFrame):
            raise TypeError()

        if self.variable not in df.columns:
            raise ValueError()

        if self.target not in df.columns:
            raise ValueError()

    def _fit_prebinning(self, df):
        # Missing data
        mask_missing = func.col(self.variable).isNull()
        dfm = df.filter(mask_missing)
        n_nonevent_missing, n_event_missing = self._target_info(dfm)
        self._n_nonevent_missing = n_nonevent_missing
        self._n_event_missing = n_event_missing

        # Special data
        if self.special_codes is None:
            mask_clean = ~mask_missing
            n_nonevent_special = 0,
            n_event_special = 0
        else:
            mask_special = func.col(self.variable).isin(self.special_codes)
            mask_clean = ~mask_missing & ~mask_special

            dfs = df.filter(mask_special)
            n_nonevent_special, n_event_special = self._target_info(dfs)
        self._n_nonevent_special = n_nonevent_special
        self._n_event_special = n_event_special

        # Clean data
        dfc = df.filter(mask_clean)

        quantile_discretizer = QuantileDiscretizer(
            numBuckets=self.max_n_prebins, inputCol=self.variable,
            outputCol="ID", relativeError=self.prebinning_eps).fit(dfc)

        splits_prebinning = quantile_discretizer.getSplits()

        df_binning = quantile_discretizer.transform(dfc).groupBy("ID").agg(
            func.count("*").alias("n_records"),
            func.sum(self.target).alias("n_event")
            ).orderBy("ID", ascending=True).toPandas()

        n_records = df_binning["n_records"].values
        n_event = df_binning["n_event"].values
        n_nonevent = n_records - n_event

        # Count total number of records/samples
        n_missing = n_nonevent_missing + n_event_missing
        n_special = n_nonevent_special + n_event_special
        self._n_samples = n_records + n_missing + n_special

        return np.array(splits_prebinning[1:-1]), n_nonevent, n_event

    def _target_info(self, df):
        df_binning = df.agg(func.count("*").alias("n_records"),
                            func.sum(self.target).alias("n_event")
                            ).toPandas()

        n_records = df_binning["n_records"].values

        if n_records:
            n_event = df_binning["n_event"].values
            n_nonevent = n_records - n_event
        else:
            n_event = 0
            n_nonevent = 0

        return n_nonevent, n_event
