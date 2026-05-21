"""Momentum-continuation signal detection.

Long fires when, in the trade window after Asia close:
  - Asian range filter passes (AH-AL >= min_asian_range_atr * ATR)
  - close > AH + displacement_atr * ATR (real break with displacement)

Short fires when:
  - close < AL - displacement_atr * ATR

Stop = level +/- stop_buffer_atr * ATR (just inside the broken level).
Target = entry +/- rr_ratio * |entry - stop|.

One long + one short max per trading day.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

_HERE = Path(__file__).resolve().parents[1]
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from asw.indicators import asia_session_levels, pine_atr  # noqa: E402

from .params import MomcontParams


def compute_signals(df: pd.DataFrame, p: MomcontParams) -> pd.DataFrame:
    """Return signal DataFrame with same columns the asw report writer expects."""
    needed = {"open", "high", "low", "close", "volume"}
    missing = needed - set(df.columns)
    if missing:
        raise ValueError(f"compute_signals: missing columns {missing}")

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
    sig_long = np.zeros(n, dtype=bool)
    sig_short = np.zeros(n, dtype=bool)
    stop_l_arr = np.full(n, np.nan)
    tgt_l_arr = np.full(n, np.nan)
    stop_s_arr = np.full(n, np.nan)
    tgt_s_arr = np.full(n, np.nan)

    asia_high = asia["asia_high"].to_numpy()
    asia_low = asia["asia_low"].to_numpy()
    close = df["close"].to_numpy()
    atr_arr = atr.to_numpy()
    bar_dates = pd.to_datetime(df.index.date).to_numpy()

    current_anchor = None
    long_done = False
    short_done = False

    for i in range(n):
        anchor = bar_dates[i]
        if anchor != current_anchor:
            current_anchor = anchor
            long_done = False
            short_done = False

        if not in_trade_window[i]:
            continue
        ah = asia_high[i]
        al = asia_low[i]
        atr_v = atr_arr[i]
        if not (np.isfinite(ah) and np.isfinite(al) and np.isfinite(atr_v)):
            continue
        if (ah - al) < p.min_asian_range_atr * atr_v:
            continue

        # Long: real break ABOVE Asia high
        if not long_done:
            displacement = close[i] - ah
            if displacement >= p.displacement_atr * atr_v:
                stop_long = ah - p.stop_buffer_atr * atr_v
                if close[i] > stop_long:
                    risk = close[i] - stop_long
                    tgt_long = close[i] + p.rr_ratio * risk
                    sig_long[i] = True
                    stop_l_arr[i] = stop_long
                    tgt_l_arr[i] = tgt_long
                    long_done = True

        # Short: real break BELOW Asia low
        if not short_done:
            displacement = al - close[i]
            if displacement >= p.displacement_atr * atr_v:
                stop_short = al + p.stop_buffer_atr * atr_v
                if close[i] < stop_short:
                    risk = stop_short - close[i]
                    tgt_short = close[i] - p.rr_ratio * risk
                    sig_short[i] = True
                    stop_s_arr[i] = stop_short
                    tgt_s_arr[i] = tgt_short
                    short_done = True

    out = pd.DataFrame(index=df.index)
    out["close"] = df["close"]
    out["high"] = df["high"]
    out["low"] = df["low"]
    out["asia_high"] = asia["asia_high"]
    out["asia_low"] = asia["asia_low"]
    out["atr"] = atr
    out["signal_long"] = sig_long
    out["signal_short"] = sig_short
    out["entry"] = df["close"]
    out["stop_long"] = stop_l_arr
    out["tgt_long"] = tgt_l_arr
    out["stop_short"] = stop_s_arr
    out["tgt_short"] = tgt_s_arr
    return out
