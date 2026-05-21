"""Parameters for the momentum-continuation strategy."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict


@dataclass(frozen=True)
class MomcontParams:
    # Sessions (UTC)
    asia_start_utc: int          # 22 = 22:00 prev day
    asia_end_utc: int            # 6
    trade_cutoff_utc: int        # 17
    hard_close_utc: int          # 21

    # Displacement threshold for the breakout to count as momentum
    displacement_atr: float      # 0.25 = close must be >= 0.25 ATR beyond AH/AL

    # Stop placement
    atr_period: int
    stop_buffer_atr: float       # stop = level +/- stop_buffer_atr * ATR
                                 # (level = AH for long, AL for short, so stop is
                                 #  just inside the broken level)

    # Target
    rr_ratio: float              # target = entry +/- rr_ratio * (entry - stop)

    # Filter: skip days with too-small Asian range (same idea as ASW)
    min_asian_range_atr: float

    # Costs
    half_spread: float
    stop_slippage: float

    def as_dict(self) -> Dict:
        return asdict(self)


XAU_MOMCONT_PARAMS = MomcontParams(
    asia_start_utc=22,
    asia_end_utc=6,
    trade_cutoff_utc=17,
    hard_close_utc=21,
    displacement_atr=0.25,
    atr_period=14,
    stop_buffer_atr=0.5,
    rr_ratio=1.5,                # 1.5:1 target. WR breakeven ~40%
    min_asian_range_atr=1.0,
    half_spread=0.18,
    stop_slippage=0.10,
)
