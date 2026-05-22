"""
Research helpers: sweep detection, day classification, R-multiple computation.

This module is parameterised over a ``VariantConfig`` so the same evaluation
plumbing can score many alternative entry/stop/target rules. Defaults reproduce
the strict v1 baseline used in ``reports/02_edge_analysis.md``.

Definitions
-----------
**Opening Range (OR)** is computed by ``sessions.opening_ranges``.

**Sweep bar** (1m bar in [09:45, 11:00) NY)
    Upper:  ``bar.high > OR-H``  AND  ``bar.close <= OR-H``
    Lower:  ``bar.low  < OR-L``  AND  ``bar.close >= OR-L``

**Entry methods**
    ``sweep_close``    enter at close of the sweep bar (default)
    ``confirm_close``  require the next bar to also close back inside the OR;
                       enter at that bar's close. If confirmation fails we
                       move on to the next sweep that *does* confirm.

**Stop methods**
    ``wick_tight``    stop = sweep wick + ``stop_buffer`` ($0.01 default)
    ``wick_buffer``   stop = sweep wick + ``stop_buffer`` (any larger buffer)
    ``pct_or``        stop = entry +/- (or_size * ``stop_pct_or``)

**Target methods**
    ``opposite_or``   target = opposite OR side
    ``fixed_R``       target = entry +/- (risk * ``target_R``)

**Costs**
    ``CostConfig.slippage_per_share`` is applied once on entry and once on
    exit (the worst-case retail assumption). It reduces realised PnL but
    does *not* alter the stop or target prices used for trade simulation.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from . import sessions


EPS = 0.0  # require strict overshoot if you set this > 0


# --------------------------------------------------------------------------- #
# Configuration objects
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class VariantConfig:
    """Knobs that define one strategy variant."""
    name: str = "v1_baseline"
    entry_method: str = "sweep_close"          # sweep_close | confirm_close
    stop_method: str = "wick_tight"            # wick_tight | wick_buffer | pct_or
    stop_buffer: float = 0.01                  # $ added beyond wick (wick_*)
    stop_pct_or: float = 0.30                  # fraction of or_size (pct_or)
    target_method: str = "opposite_or"         # opposite_or | fixed_R
    target_R: float = 1.0                      # multiplier (fixed_R)
    description: str = ""


@dataclass(frozen=True)
class CostConfig:
    """Round-trip execution cost per share. Applied to realised PnL."""
    slippage_per_share: float = 0.0
    commission_per_share: float = 0.0

    @property
    def per_round_trip(self) -> float:
        return 2.0 * (self.slippage_per_share + self.commission_per_share)


# --------------------------------------------------------------------------- #
# Per-day setup table
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class _Setup:
    side: str                       # "upper" or "lower"
    sweep_ts: pd.Timestamp          # NY-local timestamp of the sweep bar
    sweep_high: float
    sweep_low: float
    sweep_close: float
    entry_ts: pd.Timestamp          # equals sweep_ts unless confirm_close
    entry_price: float


def build_setup_table(
    bars: pd.DataFrame,
    config: VariantConfig | None = None,
    costs: CostConfig | None = None,
) -> pd.DataFrame:
    """
    Compute per-NY-day setup features under the supplied variant + cost model.

    The output schema is stable across variants so downstream analysis code
    can compare them. Columns include OR descriptors, sweep info, entry/stop/
    target prices, hit-or-miss flags, MFE/MAE, and final R-multiple.
    """
    config = config or VariantConfig()
    costs = costs or CostConfig()

    if bars.empty:
        return pd.DataFrame()

    or_table = sessions.opening_ranges(bars)
    trade = sessions.trade_window(bars)
    if trade.empty:
        return pd.DataFrame()

    ny_dates = trade.index.tz_convert(sessions.NY_TZ).date
    trade = trade.copy()
    trade["__ny_date"] = ny_dates

    rows: list[dict] = []
    for ny_date, day_or in or_table.iterrows():
        if day_or["n_bars"] < 10:
            continue

        day_trade = trade[trade["__ny_date"] == ny_date.date()]
        if day_trade.empty:
            continue

        setup = _find_entry(day_trade, day_or["or_high"], day_or["or_low"], config)

        row: dict = {
            "ny_date": ny_date,
            "or_open": float(day_or["or_open"]),
            "or_high": float(day_or["or_high"]),
            "or_low": float(day_or["or_low"]),
            "or_close": float(day_or["or_close"]),
            "or_size": float(day_or["or_size"]),
            "or_mid": float(day_or["or_mid"]),
            "or_n_bars": int(day_or["n_bars"]),
        }

        if setup is None:
            row.update(
                sweep_side=None, sweep_ts=None,
                sweep_high=None, sweep_low=None, sweep_close=None,
                entry_ts=None, entry_price=None,
                stop_price=None, target_price=None, risk=None,
                target_hit=False, stop_hit=False, timed_out=True,
                bars_to_target=np.nan, bars_to_stop=np.nan,
                mfe=np.nan, mae=np.nan,
                r_multiple_gross=np.nan, r_multiple=np.nan,
            )
        else:
            stop_px = _compute_stop(setup, day_or["or_size"], config)
            target_px = _compute_target(setup, stop_px, day_or["or_high"], day_or["or_low"], config)
            outcome = _evaluate_outcome(day_trade, setup, stop_px, target_px, costs)
            row.update(
                sweep_side=setup.side,
                sweep_ts=setup.sweep_ts,
                sweep_high=setup.sweep_high,
                sweep_low=setup.sweep_low,
                sweep_close=setup.sweep_close,
                entry_ts=setup.entry_ts,
                entry_price=setup.entry_price,
                stop_price=stop_px,
                target_price=target_px,
                **outcome,
            )

        rows.append(row)

    if not rows:
        return pd.DataFrame()

    return (
        pd.DataFrame(rows)
        .set_index("ny_date")
        .sort_index()
    )


# --------------------------------------------------------------------------- #
# Entry detection
# --------------------------------------------------------------------------- #
def _find_entry(
    day_trade: pd.DataFrame,
    or_high: float,
    or_low: float,
    config: VariantConfig,
) -> _Setup | None:
    """Find the first sweep that satisfies the configured entry method."""
    upper_mask = (day_trade["high"] > or_high + EPS) & (day_trade["close"] <= or_high)
    lower_mask = (day_trade["low"] < or_low - EPS) & (day_trade["close"] >= or_low)
    sweep_mask = upper_mask | lower_mask

    if not sweep_mask.any():
        return None

    candidate_indices = day_trade.index[sweep_mask]
    for idx in candidate_indices:
        bar = day_trade.loc[idx]
        side = "upper" if upper_mask.loc[idx] else "lower"
        sweep_ts_ny = idx.tz_convert(sessions.NY_TZ)

        if config.entry_method == "sweep_close":
            return _Setup(
                side=side,
                sweep_ts=sweep_ts_ny,
                sweep_high=float(bar["high"]),
                sweep_low=float(bar["low"]),
                sweep_close=float(bar["close"]),
                entry_ts=sweep_ts_ny,
                entry_price=float(bar["close"]),
            )

        if config.entry_method == "confirm_close":
            after = day_trade.loc[day_trade.index > idx]
            if after.empty:
                continue  # no confirmation bar available
            confirm_bar = after.iloc[0]
            confirm_idx = after.index[0]

            # Confirmation: the next bar must close back inside the OR *and*
            # not break the sweep wick on its own (else we already lost).
            if side == "upper":
                if confirm_bar["close"] > or_high:
                    continue  # close above OR - no confirmation
                if confirm_bar["high"] > bar["high"]:
                    continue  # would have stopped out before we could confirm
            else:
                if confirm_bar["close"] < or_low:
                    continue
                if confirm_bar["low"] < bar["low"]:
                    continue

            return _Setup(
                side=side,
                sweep_ts=sweep_ts_ny,
                sweep_high=float(bar["high"]),
                sweep_low=float(bar["low"]),
                sweep_close=float(bar["close"]),
                entry_ts=confirm_idx.tz_convert(sessions.NY_TZ),
                entry_price=float(confirm_bar["close"]),
            )

        raise ValueError(f"Unknown entry_method: {config.entry_method}")

    return None


# --------------------------------------------------------------------------- #
# Stop / Target pricing
# --------------------------------------------------------------------------- #
def _compute_stop(setup: _Setup, or_size: float, config: VariantConfig) -> float:
    if config.stop_method in ("wick_tight", "wick_buffer"):
        if setup.side == "upper":
            return setup.sweep_high + config.stop_buffer
        return setup.sweep_low - config.stop_buffer

    if config.stop_method == "pct_or":
        offset = or_size * config.stop_pct_or
        if setup.side == "upper":
            return setup.entry_price + offset
        return setup.entry_price - offset

    raise ValueError(f"Unknown stop_method: {config.stop_method}")


def _compute_target(
    setup: _Setup,
    stop_price: float,
    or_high: float,
    or_low: float,
    config: VariantConfig,
) -> float:
    if config.target_method == "opposite_or":
        return or_low if setup.side == "upper" else or_high

    if config.target_method == "fixed_R":
        risk = abs(stop_price - setup.entry_price)
        offset = risk * config.target_R
        if setup.side == "upper":
            return setup.entry_price - offset
        return setup.entry_price + offset

    raise ValueError(f"Unknown target_method: {config.target_method}")


# --------------------------------------------------------------------------- #
# Outcome simulation
# --------------------------------------------------------------------------- #
def _evaluate_outcome(
    day_trade: pd.DataFrame,
    setup: _Setup,
    stop_price: float,
    target_price: float,
    costs: CostConfig,
) -> dict:
    """Walk forward from the bar after entry, evaluating stop/target/timeout."""
    after = day_trade.loc[day_trade.index > setup.entry_ts.tz_convert("UTC")]
    if after.empty:
        return _empty_outcome(setup, stop_price)

    if setup.side == "upper":
        risk = stop_price - setup.entry_price
    else:
        risk = setup.entry_price - stop_price

    if risk <= 0:
        return _empty_outcome(setup, stop_price)

    if setup.side == "upper":
        target_hit_ts = _first_hit(after["low"] <= target_price, after.index)
        stop_hit_ts = _first_hit(after["high"] >= stop_price, after.index)
    else:
        target_hit_ts = _first_hit(after["high"] >= target_price, after.index)
        stop_hit_ts = _first_hit(after["low"] <= stop_price, after.index)

    target_hit, stop_hit, hit_ts = _resolve(target_hit_ts, stop_hit_ts)
    end_ts = hit_ts if hit_ts is not None else after.index[-1]
    slice_ = after.loc[:end_ts]

    if setup.side == "upper":
        mfe = setup.entry_price - slice_["low"].min()
        mae = slice_["high"].max() - setup.entry_price
        if target_hit:
            raw_pnl = setup.entry_price - target_price
        elif stop_hit:
            raw_pnl = -(stop_price - setup.entry_price)
        else:
            close = float(after["close"].iloc[-1])
            raw_pnl = setup.entry_price - close
    else:
        mfe = slice_["high"].max() - setup.entry_price
        mae = setup.entry_price - slice_["low"].min()
        if target_hit:
            raw_pnl = target_price - setup.entry_price
        elif stop_hit:
            raw_pnl = -(setup.entry_price - stop_price)
        else:
            close = float(after["close"].iloc[-1])
            raw_pnl = close - setup.entry_price

    r_gross = raw_pnl / risk
    net_pnl = raw_pnl - costs.per_round_trip
    r_net = net_pnl / risk

    return {
        "risk": float(risk),
        "target_hit": bool(target_hit),
        "stop_hit": bool(stop_hit),
        "timed_out": bool(not target_hit and not stop_hit),
        "bars_to_target": float(len(slice_)) if target_hit else np.nan,
        "bars_to_stop": float(len(slice_)) if stop_hit else np.nan,
        "mfe": float(mfe),
        "mae": float(mae),
        "r_multiple_gross": float(r_gross),
        "r_multiple": float(r_net),
    }


def _first_hit(mask: pd.Series, index: pd.DatetimeIndex) -> pd.Timestamp | None:
    if not mask.any():
        return None
    return index[mask.values.argmax()]


def _resolve(
    target_ts: pd.Timestamp | None,
    stop_ts: pd.Timestamp | None,
) -> tuple[bool, bool, pd.Timestamp | None]:
    """Earlier wins; ties go to the stop (worst case for the trader)."""
    if target_ts is None and stop_ts is None:
        return False, False, None
    if target_ts is None:
        return False, True, stop_ts
    if stop_ts is None:
        return True, False, target_ts
    if stop_ts <= target_ts:
        return False, True, stop_ts
    return True, False, target_ts


def _empty_outcome(setup: _Setup, stop_price: float) -> dict:
    if setup.side == "upper":
        risk = stop_price - setup.entry_price
    else:
        risk = setup.entry_price - stop_price
    return {
        "risk": float(risk) if risk > 0 else np.nan,
        "target_hit": False, "stop_hit": False, "timed_out": True,
        "bars_to_target": np.nan, "bars_to_stop": np.nan,
        "mfe": np.nan, "mae": np.nan,
        "r_multiple_gross": np.nan, "r_multiple": np.nan,
    }


# --------------------------------------------------------------------------- #
# Aggregate stats
# --------------------------------------------------------------------------- #
def edge_summary(setups: pd.DataFrame) -> pd.Series:
    """Summary across all setups that produced an entry."""
    s = setups[setups["sweep_side"].notna()].copy()
    n = len(s)
    if n == 0:
        return pd.Series(dtype=float)

    return pd.Series(
        {
            "days_total": int(len(setups)),
            "days_with_entry": int(n),
            "entry_rate": n / len(setups),
            # Back-compat aliases for the original 02 script.
            "days_with_sweep": int(n),
            "sweep_rate": n / len(setups),
            "p_upper_first": float((s["sweep_side"] == "upper").mean()),
            "p_target_hit": float(s["target_hit"].mean()),
            "p_stop_hit": float(s["stop_hit"].mean()),
            "p_timeout": float(s["timed_out"].mean()),
            "expectancy_R": float(s["r_multiple"].mean()),
            "expectancy_R_gross": float(s["r_multiple_gross"].mean()),
            "median_R": float(s["r_multiple"].median()),
            "win_rate": float((s["r_multiple"] > 0).mean()),
            "avg_win_R": float(s.loc[s["r_multiple"] > 0, "r_multiple"].mean()) if (s["r_multiple"] > 0).any() else float("nan"),
            "avg_loss_R": float(s.loc[s["r_multiple"] < 0, "r_multiple"].mean()) if (s["r_multiple"] < 0).any() else float("nan"),
            "or_size_median": float(s["or_size"].median()),
        }
    )


# --------------------------------------------------------------------------- #
# Standard variant catalogue
# --------------------------------------------------------------------------- #
def standard_variants() -> list[VariantConfig]:
    """The 8 variants we test in scripts/03_variant_grid.py."""
    return [
        VariantConfig(
            name="v1_baseline",
            entry_method="sweep_close",
            stop_method="wick_tight", stop_buffer=0.01,
            target_method="opposite_or",
            description="Strict ICT: sweep close entry, 1c-tight stop, opposite OR target.",
        ),
        VariantConfig(
            name="v2_buffer_5c",
            entry_method="sweep_close",
            stop_method="wick_buffer", stop_buffer=0.05,
            target_method="opposite_or",
            description="Wider 5c stop above wick, opposite OR target.",
        ),
        VariantConfig(
            name="v3_fixed_1R",
            entry_method="sweep_close",
            stop_method="wick_tight", stop_buffer=0.01,
            target_method="fixed_R", target_R=1.0,
            description="Tight stop, target capped at 1R.",
        ),
        VariantConfig(
            name="v4_buffer_2R",
            entry_method="sweep_close",
            stop_method="wick_buffer", stop_buffer=0.05,
            target_method="fixed_R", target_R=2.0,
            description="5c-buffer stop, target 2R.",
        ),
        VariantConfig(
            name="v5_pct_or_30_2R",
            entry_method="sweep_close",
            stop_method="pct_or", stop_pct_or=0.30,
            target_method="fixed_R", target_R=2.0,
            description="Stop = 30% of OR (volatility-scaled), target 2R.",
        ),
        VariantConfig(
            name="v6_confirm_or",
            entry_method="confirm_close",
            stop_method="wick_tight", stop_buffer=0.01,
            target_method="opposite_or",
            description="Confirmation entry, tight stop, opposite OR target.",
        ),
        VariantConfig(
            name="v7_buffer_confirm_2R",
            entry_method="confirm_close",
            stop_method="wick_buffer", stop_buffer=0.05,
            target_method="fixed_R", target_R=2.0,
            description="Confirmation entry, 5c stop, target 2R.",
        ),
        VariantConfig(
            name="v8_pct_or_30_confirm_2R",
            entry_method="confirm_close",
            stop_method="pct_or", stop_pct_or=0.30,
            target_method="fixed_R", target_R=2.0,
            description="Confirmation entry, 30%-OR stop, target 2R.",
        ),
    ]
