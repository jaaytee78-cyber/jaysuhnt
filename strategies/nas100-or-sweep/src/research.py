"""
Research helpers: sweep detection, day classification, R-multiple computation.

Definitions we use throughout EDA
--------------------------------
**Opening Range (OR)**
    OR-H = max high of bars in [09:30, 09:45) NY local.
    OR-L = min low of bars in same window.
    OR-size = OR-H - OR-L.

**Trade window**
    [09:45, 11:00) NY local.

**Upper sweep bar** (1m bar in trade window)
    bar.high > OR-H + epsilon  AND  bar.close <= OR-H

**Lower sweep bar** (1m bar in trade window)
    bar.low  < OR-L - epsilon  AND  bar.close >= OR-L

**First sweep**
    The earliest upper-or-lower sweep bar in the trade window. That's the
    setup we analyse - multi-sweep days are recorded but we never re-enter.

**Reversal success** (post-sweep)
    After the first sweep, price reaches the *opposite* OR side before either
    (a) the trade window ends or (b) price breaks the sweep wick (stop).

These are deliberately strict and objective. We can relax them later (e.g.
require closure of the next bar back inside, allow partial-wick targets) and
measure how each relaxation changes the edge.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from . import sessions


EPS = 0.0  # add a small offset (e.g. 0.005) if you want to require strict overshoot


# --------------------------------------------------------------------------- #
# Per-day setup table
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class _SweepResult:
    side: str | None              # "upper", "lower", or None (no sweep)
    sweep_ts: pd.Timestamp | None # NY-local timestamp of the sweep bar
    sweep_high: float | None      # bar high (max excursion of the sweep wick)
    sweep_low: float | None       # bar low
    sweep_close: float | None     # close of the sweep bar (entry price for v1)


def build_setup_table(bars: pd.DataFrame) -> pd.DataFrame:
    """
    Compute per-NY-day setup features required for the rest of the EDA.

    Output columns
    --------------
    or_open, or_high, or_low, or_close, or_size, or_mid, or_n_bars
        Opening Range descriptors.
    sweep_side          str | NaN         "upper" / "lower" / NaN
    sweep_ts            datetime64[ns]    NY-local time of first sweep
    sweep_high/low/close                  Sweep bar OHLC fields we care about
    target_hit          bool              Reached opposite OR side before stop
    stop_hit            bool              Broke sweep wick before opposite OR
    timed_out           bool              Neither, ran out of trade window
    bars_to_target      int | NaN         Minutes from sweep bar to target hit
    bars_to_stop        int | NaN
    mfe                 float             Max favourable excursion in points (post-entry)
    mae                 float             Max adverse excursion in points (post-entry)
    r_multiple          float             Realised R = pnl / stop_distance
    """
    if bars.empty:
        return pd.DataFrame()

    or_table = sessions.opening_ranges(bars)
    trade = sessions.trade_window(bars)

    # Add NY-date column once for fast grouping in the trade window too.
    ny_dates = trade.index.tz_convert(sessions.NY_TZ).date
    trade = trade.copy()
    trade["__ny_date"] = ny_dates

    rows: list[dict] = []
    for ny_date, day_or in or_table.iterrows():
        if day_or["n_bars"] < 10:
            # Half-day or partial-data day - skip for v1 cleanliness.
            continue

        day_trade = trade[trade["__ny_date"] == ny_date.date()]
        if day_trade.empty:
            continue

        sweep = _first_sweep(day_trade, day_or["or_high"], day_or["or_low"])

        row: dict = {
            "ny_date": ny_date,
            "or_open": day_or["or_open"],
            "or_high": day_or["or_high"],
            "or_low": day_or["or_low"],
            "or_close": day_or["or_close"],
            "or_size": day_or["or_size"],
            "or_mid": day_or["or_mid"],
            "or_n_bars": int(day_or["n_bars"]),
            "sweep_side": sweep.side,
            "sweep_ts": sweep.sweep_ts,
            "sweep_high": sweep.sweep_high,
            "sweep_low": sweep.sweep_low,
            "sweep_close": sweep.sweep_close,
        }

        if sweep.side is None:
            row.update(
                target_hit=False, stop_hit=False, timed_out=True,
                bars_to_target=np.nan, bars_to_stop=np.nan,
                mfe=np.nan, mae=np.nan, r_multiple=np.nan,
            )
        else:
            outcome = _evaluate_outcome(
                day_trade, sweep, day_or["or_high"], day_or["or_low"]
            )
            row.update(outcome)

        rows.append(row)

    if not rows:
        return pd.DataFrame()

    return (
        pd.DataFrame(rows)
        .set_index("ny_date")
        .sort_index()
    )


# --------------------------------------------------------------------------- #
# Internals
# --------------------------------------------------------------------------- #
def _first_sweep(day_trade: pd.DataFrame, or_high: float, or_low: float) -> _SweepResult:
    """Find the first bar in the trade window that wicks beyond OR and closes back inside."""
    upper_mask = (day_trade["high"] > or_high + EPS) & (day_trade["close"] <= or_high)
    lower_mask = (day_trade["low"] < or_low - EPS) & (day_trade["close"] >= or_low)
    candidate_mask = upper_mask | lower_mask
    if not candidate_mask.any():
        return _SweepResult(None, None, None, None, None)

    first_idx = candidate_mask.idxmax()  # first True
    bar = day_trade.loc[first_idx]
    side = "upper" if upper_mask.loc[first_idx] else "lower"
    ny_ts = first_idx.tz_convert(sessions.NY_TZ)
    return _SweepResult(
        side=side,
        sweep_ts=ny_ts,
        sweep_high=float(bar["high"]),
        sweep_low=float(bar["low"]),
        sweep_close=float(bar["close"]),
    )


def _evaluate_outcome(
    day_trade: pd.DataFrame,
    sweep: _SweepResult,
    or_high: float,
    or_low: float,
) -> dict:
    """
    Walk forward from the bar after the sweep and decide whether the trade hit
    target (opposite OR side), stop (beyond sweep wick by 1 tick), or timed out.
    """
    # We use $0.01 as one "tick" for QQQ (penny pricing).
    tick = 0.01
    after = day_trade.loc[day_trade.index > sweep.sweep_ts.tz_convert("UTC")]
    if after.empty:
        return _empty_outcome()

    if sweep.side == "upper":
        entry = sweep.sweep_close
        stop = sweep.sweep_high + tick
        target = or_low
        # short trade: pnl positive when price falls
        risk = stop - entry
        if risk <= 0:
            return _empty_outcome()

        target_hit_ts = _first_hit(after["low"] <= target, after.index)
        stop_hit_ts = _first_hit(after["high"] >= stop, after.index)
        target_hit, stop_hit, hit_ts = _resolve(target_hit_ts, stop_hit_ts)

        # MFE/MAE measured up to the first hit (or end of window if neither).
        end_ts = hit_ts if hit_ts is not None else after.index[-1]
        slice_ = after.loc[:end_ts]
        mfe = entry - slice_["low"].min()        # short: lower price is favourable
        mae = slice_["high"].max() - entry

        if target_hit:
            r_multiple = (entry - target) / risk
        elif stop_hit:
            r_multiple = -1.0
        else:
            # Timed out - mark to last bar's close.
            close = float(after["close"].iloc[-1])
            r_multiple = (entry - close) / risk

    else:  # lower sweep => long trade
        entry = sweep.sweep_close
        stop = sweep.sweep_low - tick
        target = or_high
        risk = entry - stop
        if risk <= 0:
            return _empty_outcome()

        target_hit_ts = _first_hit(after["high"] >= target, after.index)
        stop_hit_ts = _first_hit(after["low"] <= stop, after.index)
        target_hit, stop_hit, hit_ts = _resolve(target_hit_ts, stop_hit_ts)

        end_ts = hit_ts if hit_ts is not None else after.index[-1]
        slice_ = after.loc[:end_ts]
        mfe = slice_["high"].max() - entry
        mae = entry - slice_["low"].min()

        if target_hit:
            r_multiple = (target - entry) / risk
        elif stop_hit:
            r_multiple = -1.0
        else:
            close = float(after["close"].iloc[-1])
            r_multiple = (close - entry) / risk

    bars_to_target = len(slice_) if target_hit else np.nan
    bars_to_stop = len(slice_) if stop_hit else np.nan

    return {
        "target_hit": bool(target_hit),
        "stop_hit": bool(stop_hit),
        "timed_out": bool(not target_hit and not stop_hit),
        "bars_to_target": bars_to_target,
        "bars_to_stop": bars_to_stop,
        "mfe": float(mfe),
        "mae": float(mae),
        "r_multiple": float(r_multiple),
    }


def _first_hit(mask: pd.Series, index: pd.DatetimeIndex) -> pd.Timestamp | None:
    if not mask.any():
        return None
    return index[mask.values.argmax()]


def _resolve(
    target_ts: pd.Timestamp | None,
    stop_ts: pd.Timestamp | None,
) -> tuple[bool, bool, pd.Timestamp | None]:
    """
    If both target and stop are touched, the earlier wins. If they happen on
    the same bar, we conservatively take the stop (worst case for the trader).
    """
    if target_ts is None and stop_ts is None:
        return False, False, None
    if target_ts is None:
        return False, True, stop_ts
    if stop_ts is None:
        return True, False, target_ts
    if stop_ts <= target_ts:
        return False, True, stop_ts
    return True, False, target_ts


def _empty_outcome() -> dict:
    return {
        "target_hit": False, "stop_hit": False, "timed_out": True,
        "bars_to_target": np.nan, "bars_to_stop": np.nan,
        "mfe": np.nan, "mae": np.nan, "r_multiple": np.nan,
    }


# --------------------------------------------------------------------------- #
# Aggregate stats
# --------------------------------------------------------------------------- #
def edge_summary(setups: pd.DataFrame) -> pd.Series:
    """One-shot summary of the unconditional edge across all setups with a sweep."""
    s = setups[setups["sweep_side"].notna()].copy()
    n = len(s)
    if n == 0:
        return pd.Series(dtype=float)

    return pd.Series(
        {
            "days_total": int(len(setups)),
            "days_with_sweep": int(n),
            "sweep_rate": n / len(setups),
            "p_upper_first": float((s["sweep_side"] == "upper").mean()),
            "p_target_hit": float(s["target_hit"].mean()),
            "p_stop_hit": float(s["stop_hit"].mean()),
            "p_timeout": float(s["timed_out"].mean()),
            "expectancy_R": float(s["r_multiple"].mean()),
            "median_R": float(s["r_multiple"].median()),
            "win_rate": float((s["r_multiple"] > 0).mean()),
            "avg_win_R": float(s.loc[s["r_multiple"] > 0, "r_multiple"].mean()) if (s["r_multiple"] > 0).any() else float("nan"),
            "avg_loss_R": float(s.loc[s["r_multiple"] < 0, "r_multiple"].mean()) if (s["r_multiple"] < 0).any() else float("nan"),
            "or_size_median": float(s["or_size"].median()),
        }
    )
