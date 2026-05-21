"""Parameters for the 9/21 EMA crossover strategy."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict


@dataclass(frozen=True)
class EmaxParams:
    timeframe: str
    fast_period: int
    slow_period: int
    atr_period: int
    stop_atr: float
    rr_ratio: float
    hard_close_utc: int
    half_spread: float
    stop_slippage: float

    def as_dict(self) -> Dict:
        return asdict(self)


# 5m XAU preset -- to confirm/disconfirm the "5m XAU is dead" finding
XAU_EMAX_5M_PARAMS = EmaxParams(
    timeframe="5m",
    fast_period=9,
    slow_period=21,
    atr_period=14,
    stop_atr=2.0,
    rr_ratio=2.0,
    hard_close_utc=21,
    half_spread=0.18,
    stop_slippage=0.10,
)

# 4h XAU preset -- sibling test to Donchian 4h
XAU_EMAX_4H_PARAMS = EmaxParams(
    timeframe="4h",
    fast_period=9,
    slow_period=21,
    atr_period=14,
    stop_atr=2.0,
    rr_ratio=3.0,
    hard_close_utc=24,
    half_spread=0.18,
    stop_slippage=0.20,
)
