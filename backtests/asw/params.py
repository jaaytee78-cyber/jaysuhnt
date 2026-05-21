"""Parameters for the XAU Asian Sweep + Reversal strategy.

Defaults are taken from the spec. They are NOT to be optimised before
out-of-sample validation has confirmed the hypothesis. If they need to
change, change the spec first, justify in CHANGELOG, then update here.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict


@dataclass(frozen=True)
class AswParams:
    # --- Sessions (UTC) ----------------------------------------------------
    asia_start_utc: int          # Asia opens at this hour (e.g. 22 = 22:00 prev day)
    asia_end_utc: int            # Asia closes at this hour (e.g. 6 = 06:00)
    trade_cutoff_utc: int        # No new entries after this hour (e.g. 17)
    hard_close_utc: int          # Open positions exit at the bar at/before this hour

    # --- Sweep + reclaim ---------------------------------------------------
    sweep_buffer: float          # Sweep requires low < AL - buffer (or high > AH + buffer)
    reclaim_window_bars: int     # Reclaim must happen within this many bars of sweep

    # --- Stop + target ------------------------------------------------------
    atr_period: int
    stop_buffer_atr: float       # Stop = sweep_extreme +/- stop_buffer_atr * ATR
    target_mode: str             # "asian_range" (target = opposite Asian end) or "fixed_rr"
    rr_ratio: float              # Used only when target_mode == "fixed_rr"

    # --- Filter ------------------------------------------------------------
    min_asian_range_atr: float   # Skip days where (AH - AL) < min_asian_range_atr * ATR

    # --- Realistic execution costs ----------------------------------------
    half_spread: float           # Per-side half-spread in instrument price units
    stop_slippage: float         # Extra adverse move on stop hits

    def as_dict(self) -> Dict:
        return asdict(self)


# Defaults straight from the spec.
XAU_ASW_PARAMS = AswParams(
    asia_start_utc=22,
    asia_end_utc=6,
    trade_cutoff_utc=17,
    hard_close_utc=21,
    sweep_buffer=0.0,
    reclaim_window_bars=48,         # 4 hours on 5m
    atr_period=14,
    stop_buffer_atr=0.5,
    target_mode="asian_range",
    rr_ratio=2.0,                   # used only when target_mode == "fixed_rr"
    min_asian_range_atr=1.0,
    half_spread=0.18,               # XAU retail mid-of-range
    stop_slippage=0.10,
)
