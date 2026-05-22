"""
Higher-timeframe bias signals available at 09:30 NY (i.e. before the OR window
even starts). Each bias function returns a Series of "bull" / "bear" /
"neutral" indexed by NY date, where the value is the bias to use *for that
day's trade decision* (so it never peeks ahead - all inputs come from prior
sessions or from already-closed bars at 09:30 NY).

A setup is "bias-aligned" when:
    bias=="bull" and sweep_side=="lower"   (long, with the trend)
    bias=="bear" and sweep_side=="upper"   (short, with the trend)

It is "against" the bias for the other two combinations, and we drop
neutral-bias days from both subsets.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from . import sessions


# --------------------------------------------------------------------------- #
# Daily aggregates (RTH only)
# --------------------------------------------------------------------------- #
def _daily_rth_aggs(bars: pd.DataFrame) -> pd.DataFrame:
    """One row per NY date: open (first RTH bar), close (last RTH bar)."""
    rth = sessions.regular_session(bars)
    if rth.empty:
        return pd.DataFrame(columns=["open", "close"], dtype=float)

    ny_dates = rth.index.tz_convert(sessions.NY_TZ).date
    df = (
        pd.DataFrame({
            "open": rth["open"].values,
            "close": rth["close"].values,
            "ny_date": ny_dates,
        })
        .groupby("ny_date")
        .agg(open=("open", "first"), close=("close", "last"))
    )
    df.index = pd.to_datetime(df.index)
    df.index.name = "ny_date"
    return df


# --------------------------------------------------------------------------- #
# Bias methods
# --------------------------------------------------------------------------- #
def bias_prev_close_dir(bars: pd.DataFrame) -> pd.Series:
    """Bullish today if (prev day RTH close) > (day-before RTH close)."""
    daily = _daily_rth_aggs(bars)
    prev = daily["close"].shift(1)
    prev_prev = daily["close"].shift(2)
    return _classify(prev, prev_prev, name="bias_prev_close_dir")


def bias_gap_dir(bars: pd.DataFrame) -> pd.Series:
    """Bullish today if today's RTH open > yesterday's RTH close (gap up)."""
    daily = _daily_rth_aggs(bars)
    today_open = daily["open"]
    prev_close = daily["close"].shift(1)
    return _classify(today_open, prev_close, name="bias_gap_dir")


def bias_ema_20(bars: pd.DataFrame, period: int = 20) -> pd.Series:
    """Bullish today if prev day RTH close > N-period EMA of RTH closes."""
    daily = _daily_rth_aggs(bars)
    ema = daily["close"].ewm(span=period, adjust=False).mean()
    prev = daily["close"].shift(1)
    prev_ema = ema.shift(1)
    return _classify(prev, prev_ema, name=f"bias_ema_{period}")


def _classify(numerator: pd.Series, denominator: pd.Series, name: str) -> pd.Series:
    out = pd.Series(
        np.where(
            numerator.notna() & denominator.notna() & (numerator > denominator),
            "bull",
            np.where(
                numerator.notna() & denominator.notna() & (numerator < denominator),
                "bear",
                "neutral",
            ),
        ),
        index=numerator.index,
        name=name,
    )
    return out


# --------------------------------------------------------------------------- #
# Bias-alignment helper
# --------------------------------------------------------------------------- #
def alignment(bias: pd.Series, sweep_side: pd.Series) -> pd.Series:
    """
    Compare a bias series with a sweep-side series, both indexed by ny_date.
    Returns "aligned" / "against" / "neutral" / "no_setup" per row.
    """
    aligned = (
        ((bias == "bull") & (sweep_side == "lower")) |
        ((bias == "bear") & (sweep_side == "upper"))
    )
    against = (
        ((bias == "bull") & (sweep_side == "upper")) |
        ((bias == "bear") & (sweep_side == "lower"))
    )
    neutral = bias == "neutral"
    no_setup = sweep_side.isna()

    out = pd.Series("none", index=bias.index, dtype=object)
    out[no_setup] = "no_setup"
    out[neutral & ~no_setup] = "neutral"
    out[aligned & ~no_setup] = "aligned"
    out[against & ~no_setup] = "against"
    return out


def standard_bias_methods() -> dict[str, callable]:
    """Catalogue of bias methods we test."""
    return {
        "prev_close_dir": bias_prev_close_dir,
        "gap_dir": bias_gap_dir,
        "ema_20": bias_ema_20,
    }
