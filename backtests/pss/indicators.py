"""TA primitives used by the PSS port.

Every helper here is written to match Pine Script v6 semantics exactly.
Where Pine and pandas would naturally disagree (e.g. ATR uses Wilder's
RMA, not the more reactive ewm-with-span), we follow Pine.

Indicators are CAUSAL by construction: a value at bar `t` uses only
information from bars `<= t`. No look-ahead.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


# --------------------------------------------------------------------- #
#  Pine-style primitives                                                #
# --------------------------------------------------------------------- #

def pine_sma(x: pd.Series, length: int) -> pd.Series:
    """ta.sma(x, length): simple moving average over the last `length` bars."""
    return x.rolling(length, min_periods=length).mean()


def pine_ema(x: pd.Series, length: int) -> pd.Series:
    """ta.ema(x, length): EMA with alpha = 2/(length+1)."""
    return x.ewm(span=length, adjust=False).mean()


def pine_rma(x: pd.Series, length: int) -> pd.Series:
    """Wilder's RMA: alpha = 1/length. Used by ta.atr internally."""
    return x.ewm(alpha=1.0 / length, adjust=False).mean()


def pine_lowest(x: pd.Series, length: int) -> pd.Series:
    """ta.lowest(x, length): rolling min of the last `length` bars (inclusive)."""
    return x.rolling(length, min_periods=length).min()


def pine_highest(x: pd.Series, length: int) -> pd.Series:
    """ta.highest(x, length): rolling max of the last `length` bars (inclusive)."""
    return x.rolling(length, min_periods=length).max()


def true_range(df: pd.DataFrame) -> pd.Series:
    """Standard True Range: max(H-L, |H-PrevC|, |L-PrevC|)."""
    prev_close = df["close"].shift(1)
    hl = df["high"] - df["low"]
    hc = (df["high"] - prev_close).abs()
    lc = (df["low"] - prev_close).abs()
    return pd.concat([hl, hc, lc], axis=1).max(axis=1)


def pine_atr(df: pd.DataFrame, length: int) -> pd.Series:
    """ta.atr(length) -- Wilder's RMA of True Range."""
    return pine_rma(true_range(df), length)


# --------------------------------------------------------------------- #
#  Session boundary detection                                           #
# --------------------------------------------------------------------- #

def session_id(index: pd.DatetimeIndex) -> pd.Series:
    """Stable per-bar session identifier matching the .pine `newSession`
    rule: change at midnight UTC (i.e. UTC date boundary).

    Returns an int64 series suitable for groupby. The index must be
    timezone-aware (UTC) or naive-but-known-to-be-UTC.
    """
    if index.tz is None:
        # Treat naive as UTC -- caller is responsible for ensuring this.
        utc = index
    else:
        utc = index.tz_convert("UTC")
    # date() drops time-of-day; same date == same session.
    dates = pd.Series(pd.to_datetime(utc.date), index=index)
    # int64 for fast groupby
    return dates.astype("int64")


# --------------------------------------------------------------------- #
#  Session VWAP + SD bands (causal, per session)                        #
# --------------------------------------------------------------------- #

def session_vwap_bands(
    df: pd.DataFrame,
    sd_mult: float,
) -> pd.DataFrame:
    """Compute session-cumulative VWAP and +/-1SD bands.

    Returns a DataFrame indexed like df with columns:
        vwap, vwap_sd, upper1, lower1, upper2, lower2

    Causal: each value at bar t uses only bars in the same session
    with index <= t. Matches the .pine cumTPV/cumVol/cumSQ accumulators
    that reset at session change.
    """
    sid = session_id(df.index)
    tp = (df["high"] + df["low"] + df["close"]) / 3.0
    tpv = tp * df["volume"]

    # Cumulative within session
    cum_tpv = tpv.groupby(sid).cumsum()
    cum_vol = df["volume"].groupby(sid).cumsum()

    # Avoid div-by-zero at session start with no volume yet
    vwap = np.where(cum_vol > 0, cum_tpv / cum_vol.replace(0, np.nan), tp)
    vwap = pd.Series(vwap, index=df.index)

    # Volume-weighted variance: E[(tp - vwap)^2 * vol] / sum(vol)
    sq_dev = df["volume"] * (tp - vwap) ** 2
    cum_sq = sq_dev.groupby(sid).cumsum()
    var = (cum_sq / cum_vol.replace(0, np.nan)).clip(lower=0)
    vwap_sd = np.sqrt(var)

    out = pd.DataFrame(index=df.index)
    out["vwap"] = vwap
    out["vwap_sd"] = vwap_sd
    out["upper1"] = vwap + sd_mult * vwap_sd
    out["lower1"] = vwap - sd_mult * vwap_sd
    out["upper2"] = vwap + 2 * sd_mult * vwap_sd
    out["lower2"] = vwap - 2 * sd_mult * vwap_sd
    return out


# --------------------------------------------------------------------- #
#  Compression / expansion of band width                                #
# --------------------------------------------------------------------- #

def band_state(
    upper1: pd.Series,
    lower1: pd.Series,
    compress_pct: float,
) -> pd.DataFrame:
    """is_compressed = bandwidth < compress_pct * sma(bandwidth, 10)
    is_expanded   = bandwidth > 1.15        * sma(bandwidth, 10)

    Matches the .pine block exactly. The 10-bar SMA is past-only (Pine
    `ta.sma` is past-only by definition).
    """
    bw = upper1 - lower1
    bw_avg = pine_sma(bw, 10)
    out = pd.DataFrame(index=upper1.index)
    out["band_width"] = bw
    out["bw_avg"] = bw_avg
    out["is_compressed"] = bw < (compress_pct * bw_avg)
    out["is_expanded"] = bw > (1.15 * bw_avg)
    return out


# --------------------------------------------------------------------- #
#  Session-cumulative CVD + Pine 3-EMA smoothing                        #
# --------------------------------------------------------------------- #

def bar_delta(df: pd.DataFrame) -> pd.Series:
    """Pine: barDelta = volume * (closePos*2 - 1)
            where closePos = (close - low) / max(high - low, 1e-4).
    Range cap of 1e-4 prevents zero-range bars from producing inf.
    """
    rng = (df["high"] - df["low"]).clip(lower=1e-4)
    close_pos = (df["close"] - df["low"]) / rng
    return df["volume"] * (close_pos * 2.0 - 1.0)


def session_cvd_smoothed(
    df: pd.DataFrame,
    smooth_len: int = 3,
) -> pd.DataFrame:
    """Returns DataFrame with: bar_delta, session_cvd, cvd_smoothed.

    session_cvd resets at each session boundary. cvd_smoothed is the
    Pine `ta.ema(sessionDelta, smooth_len)` applied to the cumulative
    series. .pine uses smooth_len = 3.
    """
    sid = session_id(df.index)
    bd = bar_delta(df)
    cvd = bd.groupby(sid).cumsum()
    cvd_smoothed = pine_ema(cvd, smooth_len)

    out = pd.DataFrame(index=df.index)
    out["bar_delta"] = bd
    out["session_cvd"] = cvd
    out["cvd_smoothed"] = cvd_smoothed
    return out


# --------------------------------------------------------------------- #
#  CVD divergence at 8-bar pivots                                       #
# --------------------------------------------------------------------- #

def bull_bear_divergence(
    df: pd.DataFrame,
    cvd_smoothed: pd.Series,
    pivot_len: int = 8,
) -> pd.DataFrame:
    """Pine:
        priceLow8  = ta.lowest(low,  8)
        priceHigh8 = ta.highest(high, 8)
        bullDiv    = low  == priceLow8  and cvdSmoothed > cvdSmoothed[8]
        bearDiv    = high == priceHigh8 and cvdSmoothed < cvdSmoothed[8]

    Past-only by construction. No argrelextrema look-ahead.
    """
    price_lo = pine_lowest(df["low"], pivot_len)
    price_hi = pine_highest(df["high"], pivot_len)
    cvd_prev = cvd_smoothed.shift(pivot_len)

    bull = (df["low"] == price_lo) & (cvd_smoothed > cvd_prev)
    bear = (df["high"] == price_hi) & (cvd_smoothed < cvd_prev)

    out = pd.DataFrame(index=df.index)
    out["bull_div"] = bull.fillna(False)
    out["bear_div"] = bear.fillna(False)
    return out
