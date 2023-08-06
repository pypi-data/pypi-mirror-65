"""
Binning sketch.
"""

# Guillermo Navas-Palencia <g.navas.palencia@gmail.com>
# Copyright (C) 2020

import numbers

import numpy as np

from tdigest import TDigest

from ...preprocessing import split_data
from .gk import GK


def _check_parameters(sketch, eps, K, special_codes):
    if sketch not in ("gk", "t-digest"):
        raise ValueError("")

    if not isinstance(eps, numbers.Number) and not 0 <= eps <= 1:
        raise ValueError("")

    if not isinstance(K, numbers.Integral) or K <= 0:
        raise ValueError("")

    if special_codes is not None:
        if not isinstance(special_codes, (np.ndarray, list)):
            raise TypeError("special_codes must be a list or numpy.ndarray.")


class BSketch:
    """BSketch: binning sketch for binary target.

    Parameters
    ----------
    sketch : string (default="gk")
        Sketch algorithm. Supported algorithms are "gk" (Greenwald-Khanna's)
        and "t-digest" (Ted Dunning) algorithm. Algorithm "t-digest" relies on 
        `tdigest <https://github.com/CamDavidsonPilon/tdigest>`_.

    eps : float (default=0.01)
        Relative error epsilon.

    K : int (default=25)
        Parameter excess growth K to compute compress threshold in t-digest.

    special_codes : array-like or None, optional (default=None)
        List of special codes. Use special codes to specify the data values
        that must be treated separately.
    """
    def __init__(self, sketch="gk", eps=0.01, K=25, special_codes=None):
        self.sketch = sketch
        self.eps = eps
        self.K = K
        self.special_codes = special_codes

        _check_parameters(sketch, eps, K, special_codes)

        self._count_missing_e = 0
        self._count_missing_ne = 0
        self._count_special_e = 0
        self._count_special_ne = 0

        if sketch == "gk":
            self._sketch_e = GK(eps)
            self._sketch_ne = GK(eps)
        elif sketch == "t-digest":
            self._sketch_e = TDigest(eps, K)
            self._sketch_ne = TDigest(eps, K)

    def add(self, x, y, check_input=False):
        """
        Add arrays to the sketch.

        Parameters
        ----------
        x : array-like, shape = (n_samples,)
            Training vector, where n_samples is the number of samples.

        y : array-like, shape = (n_samples,)
            Target vector relative to x.

        check_input : bool (default=False)
            Whether to check input arrays.
        """
        xc, yc, xm, ym, xs, ys, _, _, _ = split_data(
            dtype=None, x=x, y=y, special_codes=self.special_codes,
            check_input=check_input)

        # Add values to sketch
        mask = yc == 1

        if self.sketch == "gk":
            for v1 in xc[mask]:
                self._sketch_e.add(v1)

            for v0 in xc[~mask]:
                self._sketch_ne.add(v0)

        if self.sketch == "t-digest":
            self._sketch_e.batch_update(xc[mask])
            self._sketch_ne.batch_update(xc[~mask])

        # Keep track of missing and special counts
        n_missing = len(ym)
        if n_missing:
            self._count_missing_e += np.count_nonzero(ym == 1)
            self._count_missing_ne += np.count_nonzero(ym == 0)

        n_special = len(ys)
        if n_special:
            self._count_special_e += np.count_nonzero(ys == 1)
            self._count_special_ne += np.count_nonzero(ys == 0)

    def bins(self, splits):
        """Event and non-events counts for each bin given a list of split
        points.

        Parameters
        ----------
        splits : array-like, shape = (n_splits,)
            List of split points.

        Returns
        -------
        bins : tuples of arrays of size n_splits + 1.
        """
        n_bins = len(splits) + 1
        bins_e = np.zeros(n_bins).astype(np.int64)
        bins_ne = np.zeros(n_bins).astype(np.int64)

        indices_e, count_e = self._indices_count(self._sketch_e, splits)
        indices_ne, count_ne = self._indices_count(self._sketch_ne, splits)

        for i in range(n_bins):
            bins_e[i] = count_e[(indices_e == i)].sum()
            bins_ne[i] = count_ne[(indices_ne == i)].sum()

        return bins_e, bins_ne

    def merge(self, bsketch):
        """Merge current instance with another BSketch instance.

        Parameters
        ----------
        bsketch : object
            BSketch instance.
        """
        if not self._mergeable(bsketch):
            raise Exception()

        if bsketch._sketch_e.n == 0 and bsketch._sketch_ne.n == 0:
            return

        if self._sketch_e.n == 0 and self._sketch_ne.n == 0:
            self._copy(bsketch)
            return

        # Merge sketches
        if self.sketch == "gk":
            self._sketch_e.merge(bsketch._sketch_e)
            self._sketch_ne.merge(bsketch._sketch_ne)
        elif self.sketch == "t-digest":
            self._sketch_e += bsketch._sketch_e
            self._sketch_ne += bsketch._sketch_ne

        # Merge missing and special counts
        self._count_missing_e += bsketch._count_missing_e
        self._count_missing_ne += bsketch._count_missing_ne
        self._count_special_e += bsketch._count_special_e
        self._count_special_ne += bsketch._count_special_ne

    def merge_sketches(self):
        """Merge event and non-event data internal sketches."""
        if self.sketch == "gk":
            new_sketch = GK(self.eps)

            new_sketch.merge(self._sketch_e)
            new_sketch.merge(self._sketch_ne)
        else:
            new_sketch = self._sketch_e + self._sketch_ne

        return new_sketch

    def _copy(self, bsketch):
        self._sketch_e = bsketch._sketch_e
        self._sketch_ne = bsketch._sketch_ne

        # Merge missing and special counts
        self._count_missing_e = bsketch._count_missing_e
        self._count_missing_ne = bsketch._count_missing_ne
        self._count_special_e = bsketch._count_special_e
        self._count_special_ne = bsketch._count_special_ne

    def _indices_count(self, sketch, splits):
        values = np.zeros(len(sketch))
        count = np.zeros(len(sketch))

        if self.sketch == "gk":
            for i, entry in enumerate(sketch.entries):
                values[i] = entry.value
                count[i] = entry.g

        elif self.sketch == "t-digest":
            for i, key in enumerate(sketch.C.keys()):
                centroid = sketch.C.get_value(key)
                values[i] = centroid.mean
                count[i] = centroid.count

        indices = np.searchsorted(splits, values, side='left')
        return indices, count

    def _mergeable(self, other):
        special_eq = True
        if self.special_codes is not None and other.special_codes is not None:
            special_eq = set(self.special_codes) == set(other.special_codes)

        return (self.sketch == other.sketch and self.eps == other.eps and
                self.K == other.K and special_eq)

    @property
    def n_event(self):
        """Event count.

        Returns
        -------
        n_event : int
        """
        count = self._sketch_e.n
        return count + self._count_missing_e + self._count_special_e

    @property
    def n_nonevent(self):
        """Non-event count.

        Returns
        -------
        n_nonevent : int
        """
        count = self._sketch_ne.n
        return count + self._count_missing_ne + self._count_special_ne

    @property
    def n(self):
        """Records count.

        Returns
        -------
        n : int
        """
        return self.n_event + self.n_nonevent
