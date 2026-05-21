# ASW validation report — XAU/USD (4h_is)

_Generated 2026-05-21 22:02 UTC; strategy spec: backtests/specs/xau_asian_sweep.md._

## What this report is

Asian Sweep + Reversal logic, run on real 5-minute Polygon data with the parameters as written in `backtests/asw/params.py` and the spec. **No optimisation. No tuning.** The question: does the strategy show a measurable edge on this data window?

_Notes: In-sample 4h 9/21 EMA cross._

## Parameters used

| param | value |
|---|---|
| timeframe | 4h |
| fast_period | 9 |
| slow_period | 21 |
| atr_period | 14 |
| stop_atr | 2.0 |
| rr_ratio | 3.0 |
| hard_close_utc | 24 |
| half_spread | 0.18 |
| stop_slippage | 0.2 |

## Data window

| field | value |
|---|---|
| instrument | XAU/USD (Polygon C:XAUUSD) |
| bars (5m) | 2392 |
| first bar | 2024-05-21T00:00:00+00:00 |
| last bar | 2025-11-18T16:00:00+00:00 |

## Asian session diagnostics

_(strategy does not use Asian session levels)_

## Headline performance

| metric | value |
|---|---|
| trades total | 92 |
| longs / shorts | 46 / 46 |
| win rate |  25.0% |
| expectancy per trade | -0.030R |
| avg R per trade | -0.030R |
| avg win | +2.892R |
| avg loss | -1.004R |
| profit factor | 0.96 |
| total R | -2.781R |
| max drawdown | -14.031R |
| longest loss streak | 10 |
| longest win streak | 3 |

## R-multiple distribution

| bucket | count | share |
|---|---|---|
| below -1R | 0 |   0.0% |
| -1.05R to -0.5R | 68 |  73.9% |
| -0.5R to -0.05R | 0 |   0.0% |
| -0.05R to +0.05R | 1 |   1.1% |
| +0.05R to +0.5R | 0 |   0.0% |
| +0.5R to +1.0R | 1 |   1.1% |
| +1.0R to +2.0R | 0 |   0.0% |
| +2.0R to +3.0R | 22 |  23.9% |
| above +3R | 0 |   0.0% |

## Exit reason breakdown

| exit reason | count | share |
|---|---|---|
| stop | 68 |  73.9% |
| target | 22 |  23.9% |
| mtm_max_hold | 2 |   2.2% |

## Performance by hour-of-day (UTC)

| hour | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| 0 | 13 |  23.1% | -0.096R | -1.251R | 0.88 |
| 4 | 14 |  21.4% | -0.159R | -2.229R | 0.80 |
| 8 | 18 |  33.3% | +0.193R | +3.482R | 1.28 |
| 12 | 13 |   7.7% | -0.710R | -9.236R | 0.24 |
| 16 | 22 |  31.8% | +0.257R | +5.649R | 1.37 |
| 20 | 12 |  25.0% | +0.067R | +0.803R | 1.10 |

## Performance by day-of-week (0=Mon)

| dow | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| 0 | 19 |  10.5% | -0.595R | -11.313R | 0.35 |
| 1 | 20 |  20.0% | -0.217R | -4.340R | 0.73 |
| 2 | 12 |  25.0% | -0.018R | -0.217R | 0.98 |
| 3 | 17 |  47.1% | +0.865R | +14.706R | 2.60 |
| 4 | 20 |  30.0% | +0.123R | +2.462R | 1.19 |

## Long vs short

| side | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| long | 46 |  41.3% | +0.588R | +27.031R | 1.98 |
| short | 46 |   8.7% | -0.648R | -29.812R | 0.29 |

## Performance by month

| month | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| 2024-06 | 9 |  11.1% | -0.579R | -5.214R | 0.36 |
| 2024-08 | 7 |  14.3% | -0.449R | -3.143R | 0.49 |
| 2024-09 | 6 |  33.3% | +0.312R | +1.872R | 1.46 |
| 2024-10 | 5 |  20.0% | -0.222R | -1.111R | 0.73 |
| 2024-12 | 7 |   0.0% | -1.023R | -7.163R | 0.00 |
| 2025-03 | 7 |  42.9% | +0.697R | +4.879R | 2.20 |
| 2025-04 | 5 |  20.0% | -0.208R | -1.041R | 0.74 |
| 2025-06 | 6 |  16.7% | -0.346R | -2.075R | 0.59 |
| 2025-07 | 8 |  25.0% | -0.016R | -0.131R | 0.98 |
| 2025-08 | 5 |  40.0% | +0.583R | +2.913R | 1.95 |
| 2025-11 | 5 |  20.0% | -0.008R | -0.039R | 0.99 |

## Coin-flip baseline

Random-direction baseline: keep the |R| outcomes from the strategy's actual trades, randomise the sign of each, sum total R. Repeat 1000 times. The probability that random direction matches or beats the strategy is reported below.

| metric | value |
|---|---|
| strategy total R | -2.781R |
| coin-flip mean total R | -0.184R |
| coin-flip std total R | 16.29 |
| P(coin flip >= strategy) | 0.560 |

P > 0.20 means the result is indistinguishable from coin-flip noise. P < 0.05 is the conventional 'real signal' threshold. Anything in between is gray.
