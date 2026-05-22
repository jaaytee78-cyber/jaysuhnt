"""
Lightweight bootstrap utilities for confidence intervals on R-multiples.

We use a non-parametric percentile bootstrap: resample the R-multiples with
replacement many times, compute the statistic of interest each time, take
the empirical 2.5%/97.5% percentiles for a 95% CI.

This is sufficient for trading-edge inference when the R-distribution is
fat-tailed (which it is here - the wins are heavy-tailed). Parametric
methods (t-test) understate uncertainty in that regime.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class BootstrapResult:
    statistic: float           # point estimate (mean of input)
    ci_low: float              # 2.5th percentile of bootstrap means
    ci_high: float             # 97.5th percentile
    n: int
    n_iter: int

    @property
    def crosses_zero(self) -> bool:
        return self.ci_low <= 0.0 <= self.ci_high


def bootstrap_mean(
    values: np.ndarray | list[float],
    n_iter: int = 10_000,
    confidence: float = 0.95,
    seed: int = 42,
) -> BootstrapResult:
    """
    Non-parametric bootstrap of the mean of ``values``.

    Returns a :class:`BootstrapResult` with the point estimate and the lower
    and upper bounds of the requested confidence interval.
    """
    arr = np.asarray(values, dtype=float)
    arr = arr[~np.isnan(arr)]
    n = len(arr)
    if n == 0:
        return BootstrapResult(np.nan, np.nan, np.nan, 0, n_iter)

    rng = np.random.default_rng(seed)
    # Vectorised: draw all samples at once. n_iter x n is fine at our sizes.
    idx = rng.integers(0, n, size=(n_iter, n))
    means = arr[idx].mean(axis=1)

    alpha = (1.0 - confidence) / 2.0
    lo = float(np.quantile(means, alpha))
    hi = float(np.quantile(means, 1.0 - alpha))
    return BootstrapResult(
        statistic=float(arr.mean()),
        ci_low=lo,
        ci_high=hi,
        n=n,
        n_iter=n_iter,
    )


def bootstrap_win_rate(
    wins: np.ndarray | list[bool],
    n_iter: int = 10_000,
    confidence: float = 0.95,
    seed: int = 42,
) -> BootstrapResult:
    """Bootstrap CI for a binary win-rate."""
    arr = np.asarray(wins, dtype=float)
    return bootstrap_mean(arr, n_iter=n_iter, confidence=confidence, seed=seed)
