"""
Session, timezone, and Opening Range utilities.

All bar DataFrames are assumed to be UTC-indexed with columns
``open, high, low, close, volume`` (the schema produced by ``data.load_aggs``).

The functions here add NY-local context, filter to specific sessions or
killzones, and compute the per-day Opening Range that the strategy is built on.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import time
from zoneinfo import ZoneInfo

import pandas as pd

NY_TZ = ZoneInfo("America/New_York")

# Regular US cash session (NYSE/NASDAQ).
RTH_OPEN = time(9, 30)
RTH_CLOSE = time(16, 0)

# Strategy-specific windows (NY local time).
OR_START = time(9, 30)
OR_END = time(9, 45)            # exclusive: OR is the [09:30, 09:45) interval
TRADE_START = time(9, 45)
TRADE_END = time(11, 0)         # flat-by time

# ICT-style killzones (NY local time), kept here for future filters / dashboard.
KILLZONES: dict[str, tuple[time, time]] = {
    "asia": (time(20, 0), time(0, 0)),       # 20:00 -> 00:00
    "london": (time(2, 0), time(5, 0)),
    "ny_am": (time(7, 0), time(11, 0)),
    "ny_pm": (time(13, 30), time(16, 0)),
}


# --------------------------------------------------------------------------- #
# Timezone helpers
# --------------------------------------------------------------------------- #
def add_ny_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return ``df`` with extra columns: ``ny_ts``, ``ny_date``, ``ny_time``.

    Does not mutate the original. Index stays in UTC.
    """
    if df.empty:
        out = df.copy()
        out["ny_ts"] = pd.Series(dtype="datetime64[ns, America/New_York]")
        out["ny_date"] = pd.Series(dtype="object")
        out["ny_time"] = pd.Series(dtype="object")
        return out

    out = df.copy()
    ny_ts = out.index.tz_convert(NY_TZ)
    out["ny_ts"] = ny_ts
    out["ny_date"] = ny_ts.date
    out["ny_time"] = ny_ts.time
    return out


# --------------------------------------------------------------------------- #
# Session / window filters
# --------------------------------------------------------------------------- #
def regular_session(df: pd.DataFrame) -> pd.DataFrame:
    """Keep only bars inside the NY regular cash session [09:30, 16:00)."""
    return _between_ny_time(df, RTH_OPEN, RTH_CLOSE)


def opening_range_window(df: pd.DataFrame) -> pd.DataFrame:
    """Bars in the OR window [09:30, 09:45) NY."""
    return _between_ny_time(df, OR_START, OR_END)


def trade_window(df: pd.DataFrame) -> pd.DataFrame:
    """Bars in the trade window [09:45, 11:00) NY."""
    return _between_ny_time(df, TRADE_START, TRADE_END)


def in_killzone(df: pd.DataFrame, name: str) -> pd.DataFrame:
    """Filter to bars inside one of the named killzones (see ``KILLZONES``)."""
    if name not in KILLZONES:
        raise KeyError(f"Unknown killzone {name!r}; choose from {list(KILLZONES)}")
    start, end = KILLZONES[name]
    return _between_ny_time(df, start, end)


def _between_ny_time(df: pd.DataFrame, start: time, end: time) -> pd.DataFrame:
    """
    Keep rows whose NY-local time falls in ``[start, end)``.

    Handles wrap-around (e.g. Asia killzone 20:00 -> 00:00) by OR-ing the two
    half-windows.
    """
    if df.empty:
        return df

    ny = df.index.tz_convert(NY_TZ).time
    if start < end:
        mask = (ny >= start) & (ny < end)
    else:
        mask = (ny >= start) | (ny < end)
    return df.loc[mask]


# --------------------------------------------------------------------------- #
# Opening Range computation
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class OpeningRange:
    """Per-session OR levels."""
    date: pd.Timestamp     # NY-local date (midnight, tz-naive)
    high: float
    low: float
    open: float
    close: float

    @property
    def size(self) -> float:
        return self.high - self.low

    @property
    def mid(self) -> float:
        return (self.high + self.low) / 2.0


def opening_ranges(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute the Opening Range (OR) per NY trading day.

    Parameters
    ----------
    df : DataFrame
        UTC-indexed OHLCV bars (typically 1m). Bars outside the OR window are
        ignored, so passing a full-session frame is fine.

    Returns
    -------
    DataFrame indexed by NY date with columns ``or_open, or_high, or_low,
    or_close, or_size, or_mid, n_bars``.

    Notes
    -----
    Days with zero bars in the OR window (holidays, halts) are dropped rather
    than emitted as NaN — downstream code can left-join if it wants holiday
    rows.
    """
    or_bars = opening_range_window(df)
    if or_bars.empty:
        return pd.DataFrame(
            columns=["or_open", "or_high", "or_low", "or_close", "or_size", "or_mid", "n_bars"]
        )

    ny_ts = or_bars.index.tz_convert(NY_TZ)
    grouper = pd.Series(ny_ts.date, index=or_bars.index, name="ny_date")

    grouped = or_bars.groupby(grouper)
    out = pd.DataFrame(
        {
            "or_open": grouped["open"].first(),
            "or_high": grouped["high"].max(),
            "or_low": grouped["low"].min(),
            "or_close": grouped["close"].last(),
            "n_bars": grouped["close"].size(),
        }
    )
    out["or_size"] = out["or_high"] - out["or_low"]
    out["or_mid"] = (out["or_high"] + out["or_low"]) / 2.0
    out.index = pd.to_datetime(out.index)
    out.index.name = "ny_date"
    return out[["or_open", "or_high", "or_low", "or_close", "or_size", "or_mid", "n_bars"]]
