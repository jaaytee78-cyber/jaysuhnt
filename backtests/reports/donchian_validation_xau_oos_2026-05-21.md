# ASW validation report — XAU/USD (oos)

_Generated 2026-05-21 21:48 UTC; strategy spec: backtests/specs/xau_asian_sweep.md._

## What this report is

Asian Sweep + Reversal logic, run on real 5-minute Polygon data with the parameters as written in `backtests/asw/params.py` and the spec. **No optimisation. No tuning.** The question: does the strategy show a measurable edge on this data window?

_Notes: Out-of-sample held-out window._

## Parameters used

| param | value |
|---|---|
| timeframe | 4h |
| lookback | 20 |
| atr_period | 14 |
| stop_atr | 2.0 |
| rr_ratio | 3.0 |
| cooldown_bars | 5 |
| half_spread | 0.18 |
| stop_slippage | 0.2 |

## Data window

| field | value |
|---|---|
| instrument | XAU/USD (Polygon C:XAUUSD) |
| bars (5m) | 789 |
| first bar | 2025-11-18T20:00:00+00:00 |
| last bar | 2026-05-20T20:00:00+00:00 |

## Asian session diagnostics

_(strategy does not use Asian session levels)_

## Headline performance

| metric | value |
|---|---|
| trades total | 43 |
| longs / shorts | 30 / 13 |
| win rate |  41.9% |
| expectancy per trade | +0.621R |
| avg R per trade | +0.621R |
| avg win | +2.880R |
| avg loss | -1.006R |
| profit factor | 2.06 |
| total R | +26.690R |
| max drawdown | -6.144R |
| longest loss streak | 5 |
| longest win streak | 3 |

## R-multiple distribution

| bucket | count | share |
|---|---|---|
| below -1R | 0 |   0.0% |
| -1.05R to -0.5R | 25 |  58.1% |
| -0.5R to -0.05R | 0 |   0.0% |
| -0.05R to +0.05R | 0 |   0.0% |
| +0.05R to +0.5R | 0 |   0.0% |
| +0.5R to +1.0R | 1 |   2.3% |
| +1.0R to +2.0R | 0 |   0.0% |
| +2.0R to +3.0R | 17 |  39.5% |
| above +3R | 0 |   0.0% |

## Exit reason breakdown

| exit reason | count | share |
|---|---|---|
| stop | 25 |  58.1% |
| target | 17 |  39.5% |
| mtm_max_hold | 1 |   2.3% |

## Performance by hour-of-day (UTC)

| hour | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| 0 | 5 |  60.0% | +0.979R | +4.894R | 3.42 |
| 4 | 5 |  40.0% | +0.593R | +2.966R | 1.98 |
| 12 | 14 |  28.6% | +0.136R | +1.906R | 1.19 |
| 16 | 9 |  33.3% | +0.329R | +2.965R | 1.49 |
| 20 | 7 |  57.1% | +1.281R | +8.970R | 3.97 |

## Performance by day-of-week (0=Mon)

| dow | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| 0 | 8 |  37.5% | +0.494R | +3.955R | 1.79 |
| 1 | 10 |  20.0% | -0.206R | -2.063R | 0.74 |
| 2 | 8 |  25.0% | -0.005R | -0.044R | 0.99 |
| 4 | 11 |  54.5% | +0.988R | +10.869R | 3.16 |

## Long vs short

| side | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| long | 30 |  43.3% | +0.728R | +21.828R | 2.28 |
| short | 13 |  38.5% | +0.374R | +4.862R | 1.60 |

## Performance by month

| month | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| 2025-12 | 6 |  33.3% | +0.325R | +1.948R | 1.48 |
| 2026-01 | 12 |  58.3% | +1.328R | +15.937R | 4.17 |
| 2026-02 | 6 |  16.7% | -0.338R | -2.027R | 0.60 |
| 2026-03 | 6 |  50.0% | +0.996R | +5.977R | 2.98 |
| 2026-04 | 6 |  16.7% | -0.340R | -2.038R | 0.60 |

## Coin-flip baseline

Random-direction baseline: keep the |R| outcomes from the strategy's actual trades, randomise the sign of each, sum total R. Repeat 1000 times. The probability that random direction matches or beats the strategy is reported below.

| metric | value |
|---|---|
| strategy total R | +26.690R |
| coin-flip mean total R | -0.097R |
| coin-flip std total R | 13.73 |
| P(coin flip >= strategy) | 0.029 |

P > 0.20 means the result is indistinguishable from coin-flip noise. P < 0.05 is the conventional 'real signal' threshold. Anything in between is gray.
