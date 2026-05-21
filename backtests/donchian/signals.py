"""Donchian-channel breakout signals.

Long fires when current bar's close > the highest high of the prior
`lookback` bars (excluding current). Short fires when close < the
lowest low of the prior `lookback` bars (excluding current).

Stops and targets are ATR-based and frozen at fire time.
Cooldown prevents the same-direction signal from re-firing within
`cooldown_bars` of the last fire.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from .params import DonchianParams

# We reuse the asw.indicators helpers (pine_atr) to stay consistent with
# the validation harness used elsewhere.
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parents[1]
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from asw.indicators import pine_atr  # noqa: E402


def compute_signals(df: pd.DataFrame, p: DonchianParams) -> pd.DataFrame:
    """Returns a DataFrame indexed like df with the same columns the
    asw report writer expects: signal_long, signal_short, entry,
    stop_long, tgt_long, stop_short, tgt_short, atr, plus high/low/close
    pass-through.
    """
    needed = {"open", "high", "low", "close", "volume"}
    missing = needed - set(df.columns)
    if missing:
        raise ValueError(f"compute_signals: missing columns {missing}")

    # Donchian channel: highest high / lowest low of the PRIOR `lookback`
    # bars (i.e. rolling max/min of high/low shifted by 1 bar).
    high = df["high"]
    low = df["low"]
    close = df["close"]

    upper = high.rolling(p.lookback, min_periods=p.lookback).max().shift(1)
    lower = low.rolling(p.lookback, min_periods=p.lookback).min().shift(1)

    atr = pine_atr(df, p.atr_period)

    # Raw breakout candidates
    long_break = close > upper
    short_break = close < lower

    n = len(df)
    sig_long = np.zeros(n, dtype=bool)
    sig_short = np.zeros(n, dtype=bool)
    last_long_fire = -p.cooldown_bars - 1
    last_short_fire = -p.cooldown_bars - 1

    long_arr = long_break.fillna(False).to_numpy()
    short_arr = short_break.fillna(False).to_numpy()
    atr_arr = atr.to_numpy()

    for i in range(n):
        if not np.isfinite(atr_arr[i]):
            continue
        if long_arr[i] and (i - last_long_fire) > p.cooldown_bars:
            sig_long[i] = True
            last_long_fire = i
        if short_arr[i] and (i - last_short_fire) > p.cooldown_bars:
            sig_short[i] = True
            last_short_fire = i

    entry = close
    stop_long = entry - p.stop_atr * atr
    tgt_long = entry + p.stop_atr * atr * p.rr_ratio
    stop_short = entry + p.stop_atr * atr
    tgt_short = entry - p.stop_atr * atr * p.rr_ratio

    out = pd.DataFrame(index=df.index)
    out["close"] = close
    out["high"] = high
    out["low"] = low
    out["atr"] = atr
    out["upper_donchian"] = upper
    out["lower_donchian"] = lower
    out["signal_long"] = sig_long
    out["signal_short"] = sig_short
    out["entry"] = entry
    out["stop_long"] = stop_long
    out["tgt_long"] = tgt_long
    out["stop_short"] = stop_short
    out["tgt_short"] = tgt_short
    return out
