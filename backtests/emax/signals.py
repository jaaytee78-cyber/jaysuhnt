"""9/21 EMA crossover signal detection."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

_HERE = Path(__file__).resolve().parents[1]
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from asw.indicators import pine_atr  # noqa: E402

from .params import EmaxParams


def _ema(x: pd.Series, length: int) -> pd.Series:
    """Pine ta.ema: alpha = 2/(length+1)."""
    return x.ewm(span=length, adjust=False).mean()


def compute_signals(df: pd.DataFrame, p: EmaxParams) -> pd.DataFrame:
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

    fast = _ema(df["close"], p.fast_period)
    slow = _ema(df["close"], p.slow_period)
    atr = pine_atr(df, p.atr_period)

    fast_prev = fast.shift(1)
    slow_prev = slow.shift(1)

    # Crossover detection: cross above for long, cross below for short
    cross_up = (fast > slow) & (fast_prev <= slow_prev)
    cross_dn = (fast < slow) & (fast_prev >= slow_prev)

    atr_ready = atr.notna()
    sig_long = (cross_up & atr_ready).fillna(False).to_numpy()
    sig_short = (cross_dn & atr_ready).fillna(False).to_numpy()

    entry = df["close"]
    stop_long = entry - p.stop_atr * atr
    tgt_long = entry + p.stop_atr * atr * p.rr_ratio
    stop_short = entry + p.stop_atr * atr
    tgt_short = entry - p.stop_atr * atr * p.rr_ratio

    out = pd.DataFrame(index=df.index)
    out["close"] = df["close"]
    out["high"] = df["high"]
    out["low"] = df["low"]
    out["fast_ema"] = fast
    out["slow_ema"] = slow
    out["atr"] = atr
    out["signal_long"] = sig_long
    out["signal_short"] = sig_short
    out["entry"] = entry
    out["stop_long"] = stop_long
    out["tgt_long"] = tgt_long
    out["stop_short"] = stop_short
    out["tgt_short"] = tgt_short
    return out
