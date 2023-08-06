"""
Optimal binning algorithm in Spark.
"""

# Guillermo Navas-Palencia <g.navas.palencia@gmail.com>
# Copyright (C) 2020

import pandas as pd

from .binning_sketch import OptimalBinningSketch

try:
    import pyspark.sql.functions as func

    from pyspark.ml.feature import QuantileDiscretizer
    from pyspark.sql.dataframe import DataFrame

    PYSPARK_AVAILABLE = True
except ImportError:
    PYSPARK_AVAILABLE = False


class OptimalBinningSpark:
    def __init__(self, variable, target, name="", sketch="gk",
                 eps=1e-4, K=25, solver="cp"):

        self.variable = variable
        self.target = target
        self.name = name
        self.sketch = sketch
        self.eps = eps
        self.K = K
        self.solver = solver

        # info
        self._optb = None

        self._is_fitted = False

    def fit(self, df):
        # Check Spark availability
        if not PYSPARK_AVAILABLE:
            raise ImportError('Cannot import pyspark. Install pyspark or '
                              'choose data streaming alternative.')

        self._check_input(df)

        self._columns = [self.variable, self.target]

        self._optb = df.select(self._columns).rdd.mapPartitions(
            lambda partition: self._add(partition)).reduce(self._merge)

        self._optb.solve()

        self._is_fitted = True

    def fit_transform(self, df, metric="woe", metric_special=0,
                      metric_missing=0):
        pass

    def transform(self, df, metric="woe", metric_special=0,
                  metric_missing=0):
        pass

    def _add(self, partition):
        df_pandas = pd.DataFrame.from_records(partition, columns=self._columns)
        x = df_pandas[self.variable]
        y = df_pandas[self.target]
        optbsketch = OptimalBinningSketch(name=self.name, sketch=self.sketch,
                                          eps=self.eps, K=self.K,
                                          solver=self.solver)
        optbsketch.add(x, y)

        return [optbsketch]

    def _check_input(self, df):
        if not isinstance(df, DataFrame):
            raise TypeError()

        if self.variable not in df.columns:
            raise ValueError()

        if self.target not in df.columns:
            raise ValueError()

    @staticmethod
    def _merge(optbsketch, other_optbsketch):
        optbsketch.merge(other_optbsketch)

        return optbsketch

    @property
    def binning_table(self):
        """Return an instantiated binning table. Please refer to
        :ref:`Binning table: binary target`.

        Returns
        -------
        binning_table : BinningTable.
        """
        return self._optb.binning_table

    @property
    def splits(self):
        """List of optimal split points when ``dtype`` is set to "numerical" or
        list of optimal bins when ``dtype`` is set to "categorical".

        Returns
        -------
        splits : numpy.ndarray
        """
        return self._optb.splits

    @property
    def status(self):
        """The status of the underlying optimization solver.

        Returns
        -------
        status : str
        """
        return self._optb.status
