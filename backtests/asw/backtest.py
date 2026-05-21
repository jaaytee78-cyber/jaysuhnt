"""Backtest engine for the ASW strategy.

Different from the PSS backtest in two ways:

1. Risk distance is per-trade, computed from |entry - stop| at fire time
   (not stop_mult * ATR). The ASW stop sits at sweep_extreme +/- some
   ATR buffer; that distance varies by setup.

2. Time stop is hard_close_utc, applied to the SAME UTC date as the
   fire bar. If the entry bar is at 16:50 UTC and hard_close_utc=21,
   we walk forward at most 50 bars (4h10m) before exiting at the
   bar at-or-before 21:00 UTC.

Cost model (half_spread + stop_slippage) is identical to PSS.
Same-bar stop+target ambiguity is resolved pessimistically: stop hits
first.
"""

from __future__ import annotations

from typing import Optional

import numpy as np
import pandas as pd

from .params import AswParams


def _hard_close_idx_for_day(
    bar_dates: np.ndarray,
    hours: np.ndarray,
    minutes: np.ndarray,
    hard_close_utc: int,
    fire_idx: int,
    n: int,
) -> int:
    """Find the integer position of the latest bar on the same UTC date
    as `fire_idx` whose hour < hard_close_utc (i.e. last bar before the
    hard close). If none, return n-1 (end of dataset).
    """
    fire_date = bar_dates[fire_idx]
    last = fire_idx
    for j in range(fire_idx + 1, n):
        if bar_dates[j] != fire_date:
            return last
        if hours[j] < hard_close_utc:
            last = j
        else:
            return last
    return last


def run_backtest(sig: pd.DataFrame, p: AswParams) -> pd.DataFrame:
    """Resolve every fired signal to a trade outcome.

    Returns a DataFrame indexed by entry timestamp with one row per trade.
    """
    needed = {"signal_long", "signal_short", "entry",
              "stop_long", "tgt_long", "stop_short", "tgt_short"}
    missing = needed - set(sig.columns)
    if missing:
        raise ValueError(f"run_backtest: missing columns {missing}")

    n = len(sig)
    high = sig["high"].to_numpy()
    low = sig["low"].to_numpy()
    close = sig["close"].to_numpy()
    entry_arr = sig["entry"].to_numpy()
    stop_l = sig["stop_long"].to_numpy()
    tgt_l = sig["tgt_long"].to_numpy()
    stop_s = sig["stop_short"].to_numpy()
    tgt_s = sig["tgt_short"].to_numpy()
    sig_l = sig["signal_long"].to_numpy()
    sig_s = sig["signal_short"].to_numpy()

    # UTC index components for time-stop logic
    if sig.index.tz is None:
        idx_utc = sig.index.tz_localize("UTC")
    else:
        idx_utc = sig.index.tz_convert("UTC")
    bar_dates = pd.to_datetime(idx_utc.date).to_numpy()
    hours = idx_utc.hour.to_numpy()
    minutes = idx_utc.minute.to_numpy()

    rows = []
    for i in range(n):
        side: Optional[str]
        if sig_l[i]:
            side = "long"
        elif sig_s[i]:
            side = "short"
        else:
            continue

        # Realistic entry: market order pays half-spread on the way in.
        if side == "long":
            fill = entry_arr[i] + p.half_spread
            stop_p = stop_l[i]
            tgt_p = tgt_l[i]
        else:
            fill = entry_arr[i] - p.half_spread
            stop_p = stop_s[i]
            tgt_p = tgt_s[i]

        if not (np.isfinite(stop_p) and np.isfinite(tgt_p)):
            continue

        # Per-trade risk distance: |entry - stop|. Used to scale R.
        risk_distance = abs(entry_arr[i] - stop_p)
        if not np.isfinite(risk_distance) or risk_distance <= 0:
            continue

        # Sanity: target must be on the favourable side
        if side == "long" and tgt_p <= entry_arr[i]:
            continue
        if side == "short" and tgt_p >= entry_arr[i]:
            continue

        last_search = _hard_close_idx_for_day(
            bar_dates, hours, minutes, p.hard_close_utc, i, n
        )

        exit_price = np.nan
        exit_offset = 0
        exit_reason = "mtm_hard_close"

        for j in range(i + 1, last_search + 1):
            bar_lo = low[j]
            bar_hi = high[j]
            if side == "long":
                # Stop checked first on a both-touched bar (pessimistic)
                if bar_lo <= stop_p:
                    exit_price = stop_p - p.stop_slippage - p.half_spread
                    exit_offset = j - i
                    exit_reason = "stop"
                    break
                if bar_hi >= tgt_p:
                    exit_price = tgt_p - p.half_spread
                    exit_offset = j - i
                    exit_reason = "target"
                    break
            else:
                if bar_hi >= stop_p:
                    exit_price = stop_p + p.stop_slippage + p.half_spread
                    exit_offset = j - i
                    exit_reason = "stop"
                    break
                if bar_lo <= tgt_p:
                    exit_price = tgt_p + p.half_spread
                    exit_offset = j - i
                    exit_reason = "target"
                    break

        if not np.isfinite(exit_price):
            j = last_search
            if side == "long":
                exit_price = close[j] - p.half_spread
            else:
                exit_price = close[j] + p.half_spread
            exit_offset = j - i

        if side == "long":
            pnl = exit_price - fill
        else:
            pnl = fill - exit_price
        r_realised = pnl / risk_distance

        rows.append(
            dict(
                side=side,
                entry_ts=sig.index[i],
                entry_price=float(entry_arr[i]),
                fill_price=float(fill),
                stop_price=float(stop_p),
                tgt_price=float(tgt_p),
                exit_price=float(exit_price),
                exit_bar_offset=int(exit_offset),
                exit_reason=exit_reason,
                r_realised=float(r_realised),
                risk_distance=float(risk_distance),
                hour_utc=int(hours[i]),
                day_of_week=int(idx_utc[i].dayofweek),
                trading_date=str(bar_dates[i]),
            )
        )

    if not rows:
        return pd.DataFrame(
            columns=[
                "side", "entry_ts", "entry_price", "fill_price",
                "stop_price", "tgt_price", "exit_price",
                "exit_bar_offset", "exit_reason", "r_realised",
                "risk_distance", "hour_utc", "day_of_week",
                "trading_date",
            ]
        )

    return pd.DataFrame(rows).set_index("entry_ts")
