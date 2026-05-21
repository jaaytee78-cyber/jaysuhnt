"""Current PSS parameter sets, copied verbatim from
indicators/pine-script/phase4_signals.pine.

DO NOT MODIFY these to "tune" the strategy. The whole point of the
validation is to test the parameters AS WRITTEN. If the .pine values
change, update this file to match and re-run.
"""

from dataclasses import dataclass, asdict
from typing import Dict


@dataclass(frozen=True)
class PSSParams:
    # --- Phase 4 signal params ------------------------------------------
    sd_mult:        float
    atr_period:     int
    stop_mult:      float
    rr_ratio:       float
    cooldown:       int
    level_tol:      float
    compress_pct:   float
    min_score:      int
    # --- Hour filter (UTC) ----------------------------------------------
    hour_filter:    bool
    hour_start_utc: int
    hour_end_utc:   int
    # --- Realistic execution costs (NOT in .pine; used by backtest only) -
    # Average half-spread + slippage per side, in instrument price units.
    # Doubling occurs naturally because we pay it on entry and exit.
    half_spread:    float
    stop_slippage:  float

    def as_dict(self) -> Dict:
        return asdict(self)


# Source of truth for these values: phase4_signals.pine.
XAU_PARAMS = PSSParams(
    sd_mult=1.50,
    atr_period=14,
    stop_mult=2.00,
    rr_ratio=2.00,
    cooldown=12,
    level_tol=0.25,
    compress_pct=0.85,
    # XAU at min_score=4 still produces 0 signals after the L redesign
    # (prev-day H/L). Spot XAU does not respect prior-day levels the
    # way stocks do (24-hour markets, no clear daily anchor); the L
    # redesign improved QQQ but did not save XAU. PSS effectively off
    # on XAU until the strategy itself is reconsidered for this
    # instrument class.
    min_score=4,
    hour_filter=True,
    hour_start_utc=7,
    hour_end_utc=16,
    # XAU spreads on retail demo platforms typically run 0.20-0.40 USD;
    # 0.18 half-spread = 0.36 round-trip, mid-of-range realistic.
    half_spread=0.18,
    # Stop-out slippage on a 5m bar that breaches the level: extra 0.10.
    stop_slippage=0.10,
)


# QQQ stands in for NQ futures because Polygon free tier has stocks but
# not futures. Same Phase-4 params from the .pine -- we are NOT re-tuning
# for QQQ; we are testing whether the NQ-tuned params have ANY signal on
# the closest accessible proxy. Spreads/slippage are scaled to QQQ's
# instrument units (USD per share), not NQ futures points.
QQQ_PARAMS = PSSParams(
    sd_mult=1.25,
    atr_period=14,
    stop_mult=1.25,
    rr_ratio=2.50,
    cooldown=8,
    level_tol=0.25,
    compress_pct=0.85,
    # After the L redesign (prev-day H/L), score=3 became canonical for
    # QQQ: 316 trades, +0.096R/trade, PF 1.14 vs the previous score=3's
    # PF 0.89 with old L. Score=4 still produces a higher per-trade edge
    # (29 trades, +0.430R, PF 1.72) but the smaller sample is less
    # trustworthy for forward verification.
    min_score=3,
    hour_filter=True,
    hour_start_utc=13,
    hour_end_utc=21,
    # QQQ retail spread typically 0.01 USD; 0.005 half-spread is fair.
    half_spread=0.005,
    # Stop-out slippage on QQQ 5m: 0.01 USD additional.
    stop_slippage=0.01,
)


PROFILES = {
    "XAU": XAU_PARAMS,
    "QQQ": QQQ_PARAMS,
}
