"""Sweep + reclaim signal detection for the Asian Sweep strategy.

Stateful per-trading-day. State resets at midnight UTC. Bars during
the Asia session are skipped (asia_high / asia_low are NaN there). Bars
in the trade window are checked for sweep first, then reclaim.

One long-side and one short-side trade max per trading day. After a
fire on either side, that side is locked for the rest of the day.

Signal output is a DataFrame with one row per input bar plus columns:
  signal_long, signal_short                : bool, fire markers
  entry, stop_long, tgt_long, stop_short, tgt_short : prices at fire
  asia_high, asia_low, atr                 : diagnostic columns
  sweep_low_at_fire, sweep_high_at_fire    : the sweep extreme used for stops
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from .indicators import asia_session_levels, pine_atr
from .params import AswParams


def compute_signals(df: pd.DataFrame, p: AswParams) -> pd.DataFrame:
    """Return the per-bar signal DataFrame as described in the module docstring."""
    needed = {"open", "high", "low", "close", "volume"}
    missing = needed - set(df.columns)
    if missing:
        raise ValueError(f"compute_signals: missing columns {missing}")
    if not isinstance(df.index, pd.DatetimeIndex):
        raise TypeError("compute_signals: df.index must be DatetimeIndex")

    # Ensure UTC index for consistent hour math
    if df.index.tz is None:
        df = df.copy()
        df.index = df.index.tz_localize("UTC")
    else:
        df = df.copy()
        df.index = df.index.tz_convert("UTC")

    asia = asia_session_levels(df, p.asia_start_utc, p.asia_end_utc)
    atr = pine_atr(df, p.atr_period)

    hours = df.index.hour
    in_trade_window = (hours >= p.asia_end_utc) & (hours < p.trade_cutoff_utc)

    n = len(df)
    signal_long = np.zeros(n, dtype=bool)
    signal_short = np.zeros(n, dtype=bool)
    stop_long = np.full(n, np.nan)
    tgt_long = np.full(n, np.nan)
    stop_short = np.full(n, np.nan)
    tgt_short = np.full(n, np.nan)
    sweep_low_arr = np.full(n, np.nan)
    sweep_high_arr = np.full(n, np.nan)

    asia_high = asia["asia_high"].to_numpy()
    asia_low = asia["asia_low"].to_numpy()
    high = df["high"].to_numpy()
    low = df["low"].to_numpy()
    close = df["close"].to_numpy()
    atr_arr = atr.to_numpy()
    bar_dates = pd.to_datetime(df.index.date).to_numpy()

    # Per-day state
    current_anchor = None
    long_done = False
    short_done = False
    sweep_low_active = False
    sweep_low_value = np.nan
    sweep_low_bar = -1
    sweep_high_active = False
    sweep_high_value = np.nan
    sweep_high_bar = -1

    for i in range(n):
        anchor = bar_dates[i]

        # Day boundary: reset all per-day state. Trading day = UTC date.
        # Asia bars (00:00-05:55) of this date will be skipped via in_trade_window.
        if anchor != current_anchor:
            current_anchor = anchor
            long_done = False
            short_done = False
            sweep_low_active = False
            sweep_low_value = np.nan
            sweep_low_bar = -1
            sweep_high_active = False
            sweep_high_value = np.nan
            sweep_high_bar = -1

        if not in_trade_window[i]:
            continue
        if not (np.isfinite(asia_low[i]) and np.isfinite(asia_high[i])):
            continue
        if not np.isfinite(atr_arr[i]):
            continue

        ah = asia_high[i]
        al = asia_low[i]

        # Range filter: skip days where Asian range is too tight to be meaningful
        if (ah - al) < p.min_asian_range_atr * atr_arr[i]:
            continue

        # ---- LONG SIDE: sweep low + reclaim ---------------------------------
        if not long_done:
            if not sweep_low_active:
                # Detect initial sweep
                if low[i] < al - p.sweep_buffer:
                    sweep_low_active = True
                    sweep_low_value = low[i]
                    sweep_low_bar = i
            else:
                # Already in a sweep; track lower extreme and look for reclaim
                if low[i] < sweep_low_value:
                    sweep_low_value = low[i]
                    sweep_low_bar = i

                bars_since_sweep = i - sweep_low_bar
                if bars_since_sweep > p.reclaim_window_bars:
                    # Reclaim window expired; reset sweep state, no fire
                    sweep_low_active = False
                    sweep_low_value = np.nan
                    sweep_low_bar = -1
                elif close[i] > al:
                    # Reclaim: fire long
                    signal_long[i] = True
                    sweep_low_arr[i] = sweep_low_value
                    stop_long[i] = sweep_low_value - p.stop_buffer_atr * atr_arr[i]
                    if p.target_mode == "asian_range":
                        tgt_long[i] = ah
                    elif p.target_mode == "fixed_rr":
                        risk = close[i] - stop_long[i]
                        tgt_long[i] = close[i] + p.rr_ratio * risk
                    else:
                        raise ValueError(f"unknown target_mode: {p.target_mode}")
                    long_done = True
                    sweep_low_active = False
                    sweep_low_value = np.nan
                    sweep_low_bar = -1

        # ---- SHORT SIDE: sweep high + reclaim -------------------------------
        if not short_done:
            if not sweep_high_active:
                if high[i] > ah + p.sweep_buffer:
                    sweep_high_active = True
                    sweep_high_value = high[i]
                    sweep_high_bar = i
            else:
                if high[i] > sweep_high_value:
                    sweep_high_value = high[i]
                    sweep_high_bar = i

                bars_since_sweep = i - sweep_high_bar
                if bars_since_sweep > p.reclaim_window_bars:
                    sweep_high_active = False
                    sweep_high_value = np.nan
                    sweep_high_bar = -1
                elif close[i] < ah:
                    signal_short[i] = True
                    sweep_high_arr[i] = sweep_high_value
                    stop_short[i] = sweep_high_value + p.stop_buffer_atr * atr_arr[i]
                    if p.target_mode == "asian_range":
                        tgt_short[i] = al
                    elif p.target_mode == "fixed_rr":
                        risk = stop_short[i] - close[i]
                        tgt_short[i] = close[i] - p.rr_ratio * risk
                    else:
                        raise ValueError(f"unknown target_mode: {p.target_mode}")
                    short_done = True
                    sweep_high_active = False
                    sweep_high_value = np.nan
                    sweep_high_bar = -1

    out = pd.DataFrame(index=df.index)
    out["close"] = df["close"]
    out["high"] = df["high"]
    out["low"] = df["low"]
    out["asia_high"] = asia["asia_high"]
    out["asia_low"] = asia["asia_low"]
    out["atr"] = atr
    out["signal_long"] = signal_long
    out["signal_short"] = signal_short
    out["entry"] = df["close"]
    out["stop_long"] = stop_long
    out["tgt_long"] = tgt_long
    out["stop_short"] = stop_short
    out["tgt_short"] = tgt_short
    out["sweep_low_at_fire"] = sweep_low_arr
    out["sweep_high_at_fire"] = sweep_high_arr
    return out
