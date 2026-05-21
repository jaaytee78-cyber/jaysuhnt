"""XAU Donchian-channel breakout on 4h timeframe (option B).

A simple, single-rule trend-following strategy. Long when close breaks
above the prior 20-bar high. Short when close breaks below the prior
20-bar low. Stop = N x ATR; target = M x ATR (fixed RR).

The hypothesis is that XAU is highly trending on 4h+ timeframes
(opposite of intraday mean reversion), so a Donchian breakout should
capture multi-day trends.
"""

__version__ = "0.1.0"
