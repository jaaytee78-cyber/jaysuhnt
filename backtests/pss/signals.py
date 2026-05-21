"""Bit-exact port of indicators/pine-script/phase4_signals.pine.

For every Pine line of signal logic there is a Python line here, in the
same order. Look-ahead has been audited line-by-line. The only inputs
that matter are 5m OHLCV; everything else is computed.

This module is intentionally narrow. It does not handle data fetching,
backtesting, or reporting -- it only takes a DataFrame of bars and the
PSSParams for the instrument and returns a DataFrame of signals.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from .indicators import (
    band_state,
    bull_bear_divergence,
    pine_atr,
    prev_day_levels,
    session_cvd_smoothed,
    session_vwap_bands,
)
from .params import PSSParams


# --------------------------------------------------------------------- #
#  Cooldown gating in vectorised form                                   #
# --------------------------------------------------------------------- #

def _apply_cooldown(candidate: np.ndarray, cooldown: int) -> np.ndarray:
    """Pine logic:
        barsLastLong = barsLastLong + 1   (every bar)
        if signal: barsLastLong = 0
        longReady = barsLastLong > p_cool

    So the FIRST candidate fires, then any candidate within `cooldown`
    bars after a fire is suppressed. Equivalent to: greedy first-match
    within blocks.

    Note: in the .pine, `var int barsLastLong = 0` and the increment
    happens before the check. So at bar index 0 with no prior fire,
    barsLastLong = 1, and `1 > p_cool` is False unless p_cool == 0. To
    match that exactly, the FIRST candidate after start cannot fire
    until bar `p_cool + 1`. We replicate this by initialising the
    "bars since last fire" counter to 1 at index 0.
    """
    n = len(candidate)
    fired = np.zeros(n, dtype=bool)
    bars_since = 1  # matches Pine `var int barsLastLong = 0` then `+= 1`
    for i in range(n):
        if candidate[i] and bars_since > cooldown:
            fired[i] = True
            bars_since = 0
        bars_since += 1
    return fired


# --------------------------------------------------------------------- #
#  Main port                                                            #
# --------------------------------------------------------------------- #

def compute_signals(
    df: pd.DataFrame,
    p: PSSParams,
) -> pd.DataFrame:
    """Returns a DataFrame indexed like df with all intermediate state
    plus the boolean columns `signal_long`, `signal_short` plus the
    per-trade `entry`, `stop_long`, `tgt_long`, `stop_short`, `tgt_short`
    columns populated only on the bar a signal fires.

    df must contain columns: open, high, low, close, volume.
    df.index must be a DatetimeIndex assumed to be UTC.
    """
    needed = {"open", "high", "low", "close", "volume"}
    missing = needed - set(df.columns)
    if missing:
        raise ValueError(f"compute_signals: missing columns {missing}")
    if not isinstance(df.index, pd.DatetimeIndex):
        raise TypeError("compute_signals: df.index must be DatetimeIndex")

    # ── VWAP + SD bands ────────────────────────────────────────────────
    bands = session_vwap_bands(df, sd_mult=p.sd_mult)
    vwap = bands["vwap"]
    upper1 = bands["upper1"]
    lower1 = bands["lower1"]

    # ── Compression / expansion ───────────────────────────────────────
    bs = band_state(upper1, lower1, p.compress_pct)
    is_compressed = bs["is_compressed"]
    is_expanded = bs["is_expanded"]

    # ── ATR (Wilder's RMA) ─────────────────────────────────────────────
    atr = pine_atr(df, p.atr_period)
    near_tol = p.level_tol * atr

    # ── CVD + smoothed line ────────────────────────────────────────────
    cvd_block = session_cvd_smoothed(df, smooth_len=3)  # .pine hard-codes 3
    bd = cvd_block["bar_delta"]
    cvd_sm = cvd_block["cvd_smoothed"]
    cvd_rising = cvd_sm > cvd_sm.shift(3)
    cvd_falling = cvd_sm < cvd_sm.shift(3)

    # ── Divergence at 8-bar pivots ────────────────────────────────────
    div = bull_bear_divergence(df, cvd_sm, pivot_len=8)
    bull_div = div["bull_div"]
    bear_div = div["bear_div"]

    # ── Prior-day H/L (used by the redesigned L condition) ───────────
    pdl = prev_day_levels(df)
    prev_day_high = pdl["prev_day_high"]
    prev_day_low = pdl["prev_day_low"]

    # ── VDLC condition booleans (long) ────────────────────────────────
    # L redesign (option 1): proximity to a level NOT used by V.
    # Long entries near prior-day low (real support).
    cond_v_long = df["close"] <= lower1
    cond_d_long = bull_div | (cvd_rising & (bd > 0))
    near_level_long = (df["close"] - prev_day_low).abs() < near_tol
    cond_l_long = near_level_long.fillna(False)
    cond_c_long = is_compressed

    # ── VDLC condition booleans (short) ───────────────────────────────
    # Short entries near prior-day high (real resistance).
    cond_v_short = df["close"] >= upper1
    cond_d_short = bear_div | (cvd_falling & (bd < 0))
    near_level_short = (df["close"] - prev_day_high).abs() < near_tol
    cond_l_short = near_level_short.fillna(False)
    cond_c_short = is_compressed | is_expanded

    # ── Scores ────────────────────────────────────────────────────────
    score_long = (
        cond_v_long.astype(int)
        + cond_d_long.astype(int)
        + cond_l_long.astype(int)
        + cond_c_long.astype(int)
    )
    score_short = (
        cond_v_short.astype(int)
        + cond_d_short.astype(int)
        + cond_l_short.astype(int)
        + cond_c_short.astype(int)
    )

    # ── Trend filter ──────────────────────────────────────────────────
    vwap_above_band = df["close"] > upper1
    vwap_below_band = df["close"] < lower1
    vwap_bull = df["close"] > vwap
    long_trend_ok = ~(vwap_below_band & is_expanded)
    short_trend_ok = (~(vwap_above_band & is_expanded)) & vwap_bull

    # ── Hour filter (UTC) ─────────────────────────────────────────────
    if df.index.tz is None:
        hour = df.index.hour  # treat as UTC
    else:
        hour = df.index.tz_convert("UTC").hour
    if p.hour_filter:
        hour_ok = (hour >= p.hour_start_utc) & (hour <= p.hour_end_utc)
    else:
        hour_ok = np.ones(len(df), dtype=bool)
    hour_ok = pd.Series(hour_ok, index=df.index)

    # ── Candidate signals (pre-cooldown) ──────────────────────────────
    cand_long = (
        (score_long >= p.min_score)
        & long_trend_ok
        & hour_ok
        & atr.notna()  # don't fire before ATR has warmed up
    ).fillna(False).to_numpy()
    cand_short = (
        (score_short >= p.min_score)
        & short_trend_ok
        & hour_ok
        & atr.notna()
    ).fillna(False).to_numpy()

    # ── Cooldown ──────────────────────────────────────────────────────
    fired_long = _apply_cooldown(cand_long, p.cooldown)
    fired_short = _apply_cooldown(cand_short, p.cooldown)

    # ── Stops & targets at fire bar (no spread baked in here -- that
    #    is the backtest's job) ────────────────────────────────────────
    entry = df["close"]
    stop_long = entry - p.stop_mult * atr
    tgt_long = entry + p.stop_mult * atr * p.rr_ratio
    stop_short = entry + p.stop_mult * atr
    tgt_short = entry - p.stop_mult * atr * p.rr_ratio

    # ── Assemble output ───────────────────────────────────────────────
    out = pd.DataFrame(index=df.index)
    out["close"] = df["close"]
    out["high"] = df["high"]
    out["low"] = df["low"]
    out["vwap"] = vwap
    out["upper1"] = upper1
    out["lower1"] = lower1
    out["prev_day_high"] = prev_day_high
    out["prev_day_low"] = prev_day_low
    out["atr"] = atr
    out["score_long"] = score_long
    out["score_short"] = score_short
    out["cond_v_long"] = cond_v_long
    out["cond_d_long"] = cond_d_long
    out["cond_l_long"] = cond_l_long
    out["cond_c_long"] = cond_c_long
    out["cond_v_short"] = cond_v_short
    out["cond_d_short"] = cond_d_short
    out["cond_l_short"] = cond_l_short
    out["cond_c_short"] = cond_c_short
    out["long_trend_ok"] = long_trend_ok
    out["short_trend_ok"] = short_trend_ok
    out["hour_ok"] = hour_ok
    out["signal_long"] = fired_long
    out["signal_short"] = fired_short
    out["entry"] = entry
    out["stop_long"] = stop_long
    out["tgt_long"] = tgt_long
    out["stop_short"] = stop_short
    out["tgt_short"] = tgt_short
    return out
