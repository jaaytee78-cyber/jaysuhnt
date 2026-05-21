"""Realistic backtest of PSS signals.

Design choices, all intentional:

1. Costs are real:  half-spread + slippage applied on entry, half-spread
   applied on exit; on stop hits we also add stop_slippage to the worst
   side. This matches what a paper trading account at a retail broker
   would actually fill.

2. Pessimistic same-bar resolution: when a single 5m bar straddles both
   the stop and the target, we assume the stop hit first. Without
   intra-bar tick data this is the only safe assumption.

3. No silent drops: every signal becomes a trade. If neither stop nor
   target is hit before the bar's session ends, we exit at the last
   bar's close and compute the trade in R from the actual fill, not
   discard it.

4. R is computed on a PER-TRADE basis from realised P&L divided by the
   intended risk distance (stop_mult * ATR at entry). A trade that
   stopped out at the planned stop = -1.00R; a trade that hit target
   = +rr_ratio R; a partial mark-to-market exit = whatever it was worth.

The output is a DataFrame with one row per trade, suitable for the
report writer.
"""

from __future__ import annotations

from typing import Optional

import numpy as np
import pandas as pd

from .indicators import session_id
from .params import PSSParams


def _exit_index_for_session(
    sid: pd.Series,
    entry_idx: int,
) -> int:
    """Return the integer location of the LAST bar of the session
    containing `entry_idx`. Used for end-of-session mark-to-market.
    """
    s = sid.iloc[entry_idx]
    # bars in same session, on or after entry
    same_session = sid.iloc[entry_idx:] == s
    # iloc index of the last True
    return entry_idx + int(same_session.values.cumsum().argmax())


def run_backtest(
    sig: pd.DataFrame,
    p: PSSParams,
    max_bars: int = 240,
) -> pd.DataFrame:
    """Walk through every fired signal and resolve to a trade outcome.

    Args:
        sig: output of compute_signals(); must contain signal_long,
             signal_short, entry, stop_long, tgt_long, stop_short,
             tgt_short, atr, high, low, close.
        p:   the PSSParams used to generate the signals; needed for
             half_spread, stop_slippage, stop_mult, rr_ratio.
        max_bars: hard cap on trade duration in bars. Beyond this we
             still mark-to-market exit. Default 240 = 20 hours on 5m;
             realistically every trade exits at session end well before.

    Returns:
        DataFrame indexed by entry timestamp with columns:
            side, entry_price, fill_price, stop_price, tgt_price,
            exit_price, exit_bar_offset, exit_reason, r_realised,
            risk_distance, atr_at_entry, score, hour_utc, session_id
    """
    if not {"signal_long", "signal_short"}.issubset(sig.columns):
        raise ValueError("run_backtest: sig must come from compute_signals()")

    sid = session_id(sig.index)
    high = sig["high"].to_numpy()
    low = sig["low"].to_numpy()
    close = sig["close"].to_numpy()
    atr = sig["atr"].to_numpy()
    entry_arr = sig["entry"].to_numpy()
    stop_l = sig["stop_long"].to_numpy()
    tgt_l = sig["tgt_long"].to_numpy()
    stop_s = sig["stop_short"].to_numpy()
    tgt_s = sig["tgt_short"].to_numpy()
    sig_l = sig["signal_long"].to_numpy()
    sig_s = sig["signal_short"].to_numpy()
    score_l = sig["score_long"].to_numpy()
    score_s = sig["score_short"].to_numpy()

    n = len(sig)
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
            score = int(score_l[i])
        else:
            fill = entry_arr[i] - p.half_spread
            stop_p = stop_s[i]
            tgt_p = tgt_s[i]
            score = int(score_s[i])

        risk_distance = p.stop_mult * atr[i]
        if not np.isfinite(risk_distance) or risk_distance <= 0:
            # ATR not warm or pathological; skip this signal explicitly
            # rather than recording a garbage trade
            continue

        end_of_session = _exit_index_for_session(sid, i)
        last_search = min(i + max_bars, end_of_session)

        exit_price = np.nan
        exit_offset = 0
        exit_reason = "mtm_session_end"

        for j in range(i + 1, last_search + 1):
            bar_lo = low[j]
            bar_hi = high[j]
            if side == "long":
                # Pessimistic: check stop FIRST on a both-touched bar
                if bar_lo <= stop_p:
                    exit_price = stop_p - p.stop_slippage - p.half_spread
                    exit_offset = j - i
                    exit_reason = "stop"
                    break
                if bar_hi >= tgt_p:
                    # Targets are limit orders; fill at level minus exit half-spread
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
            # Mark to market at the last searched bar's close
            j = last_search
            if side == "long":
                exit_price = close[j] - p.half_spread
            else:
                exit_price = close[j] + p.half_spread
            exit_offset = j - i
            # Distinguish session-end vs hard cap for diagnostics
            exit_reason = (
                "mtm_session_end" if j == end_of_session else "mtm_max_bars"
            )

        # Realised R: P&L / intended risk distance
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
                atr_at_entry=float(atr[i]),
                score=score,
                hour_utc=int(sig.index[i].tz_convert("UTC").hour
                              if sig.index.tz else sig.index[i].hour),
                session_id=int(sid.iloc[i]),
            )
        )

    if not rows:
        return pd.DataFrame(
            columns=[
                "side", "entry_ts", "entry_price", "fill_price",
                "stop_price", "tgt_price", "exit_price",
                "exit_bar_offset", "exit_reason", "r_realised",
                "risk_distance", "atr_at_entry", "score",
                "hour_utc", "session_id",
            ]
        )

    return pd.DataFrame(rows).set_index("entry_ts")
