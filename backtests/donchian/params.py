"""Parameters for the XAU Donchian 4h breakout strategy."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict


@dataclass(frozen=True)
class DonchianParams:
    # --- Bar resolution ---------------------------------------------------
    timeframe: str               # "4h" -- info only; signals operate on whatever bars are passed in

    # --- Donchian breakout ------------------------------------------------
    lookback: int                # N-bar high/low for breakout level (e.g. 20)

    # --- Stop + target ----------------------------------------------------
    atr_period: int
    stop_atr: float              # stop = entry +/- stop_atr * ATR
    rr_ratio: float              # target = entry +/- (stop_atr * ATR * rr_ratio)

    # --- Cooldown ---------------------------------------------------------
    cooldown_bars: int           # min bars between fires (per direction)

    # --- Realistic execution costs ---------------------------------------
    half_spread: float
    stop_slippage: float

    def as_dict(self) -> Dict:
        return asdict(self)


# Defaults, applied to XAU 4h. Conservative; not optimised.
XAU_DONCHIAN_PARAMS = DonchianParams(
    timeframe="4h",
    lookback=20,                # 20 bars on 4h = ~3.3 trading days of breakout level
    atr_period=14,
    stop_atr=2.0,               # 2x ATR(14, 4h)
    rr_ratio=3.0,               # 3:1 RR target
    cooldown_bars=5,            # 20 hours min between same-side fires
    # 4h XAU realistic spread + slippage in USD price units
    half_spread=0.18,
    stop_slippage=0.20,
)
