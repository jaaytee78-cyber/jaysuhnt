"""Backtest engine for Donchian 4h.

Differs from the ASW backtest in one way: NO time-based hard close.
A position is held until either stop or target hits, regardless of how
many bars/days that takes. Only safety net is `max_hold_bars` to prevent
runaway searches at the very end of the dataset (positions that never
resolve are marked-to-market at the last bar).

Cost model and stop-first-on-same-bar resolution are identical to the
ASW backtest.
"""

from __future__ import annotations

from typing import Optional

import numpy as np
import pandas as pd

from .params import DonchianParams


def run_backtest(sig: pd.DataFrame, p: DonchianParams,
                 max_hold_bars: int = 500) -> pd.DataFrame:
    """Resolve every fired signal to a trade outcome."""
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

    if sig.index.tz is None:
        idx_utc = sig.index.tz_localize("UTC")
    else:
        idx_utc = sig.index.tz_convert("UTC")

    rows = []
    for i in range(n):
        side: Optional[str]
        if sig_l[i]:
            side = "long"
        elif sig_s[i]:
            side = "short"
        else:
            continue

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

        risk_distance = abs(entry_arr[i] - stop_p)
        if not np.isfinite(risk_distance) or risk_distance <= 0:
            continue

        last_search = min(i + max_hold_bars, n - 1)

        exit_price = np.nan
        exit_offset = 0
        exit_reason = "mtm_max_hold"

        for j in range(i + 1, last_search + 1):
            bar_lo = low[j]
            bar_hi = high[j]
            if side == "long":
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
                hour_utc=int(idx_utc[i].hour),
                day_of_week=int(idx_utc[i].dayofweek),
                trading_date=str(pd.to_datetime(idx_utc[i].date())),
            )
        )

    if not rows:
        return pd.DataFrame(
            columns=[
                "side", "entry_ts", "entry_price", "fill_price",
                "stop_price", "tgt_price", "exit_price",
                "exit_bar_offset", "exit_reason", "r_realised",
                "risk_distance", "hour_utc", "day_of_week", "trading_date",
            ]
        )

    return pd.DataFrame(rows).set_index("entry_ts")
