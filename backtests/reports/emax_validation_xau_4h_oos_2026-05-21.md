# ASW validation report — XAU/USD (4h_oos)

_Generated 2026-05-21 22:02 UTC; strategy spec: backtests/specs/xau_asian_sweep.md._

## What this report is

Asian Sweep + Reversal logic, run on real 5-minute Polygon data with the parameters as written in `backtests/asw/params.py` and the spec. **No optimisation. No tuning.** The question: does the strategy show a measurable edge on this data window?

_Notes: OOS held-out 4h._

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
| bars (5m) | 789 |
| first bar | 2025-11-18T20:00:00+00:00 |
| last bar | 2026-05-20T20:00:00+00:00 |

## Asian session diagnostics

_(strategy does not use Asian session levels)_

## Headline performance

| metric | value |
|---|---|
| trades total | 25 |
| longs / shorts | 12 / 13 |
| win rate |  44.0% |
| expectancy per trade | +0.577R |
| avg R per trade | +0.577R |
| avg win | +2.592R |
| avg loss | -1.007R |
| profit factor | 2.02 |
| total R | +14.417R |
| max drawdown | -5.012R |
| longest loss streak | 5 |
| longest win streak | 2 |

## R-multiple distribution

| bucket | count | share |
|---|---|---|
| below -1R | 0 |   0.0% |
| -1.05R to -0.5R | 14 |  56.0% |
| -0.5R to -0.05R | 0 |   0.0% |
| -0.05R to +0.05R | 0 |   0.0% |
| +0.05R to +0.5R | 1 |   4.0% |
| +0.5R to +1.0R | 0 |   0.0% |
| +1.0R to +2.0R | 1 |   4.0% |
| +2.0R to +3.0R | 9 |  36.0% |
| above +3R | 0 |   0.0% |

## Exit reason breakdown

| exit reason | count | share |
|---|---|---|
| stop | 14 |  56.0% |
| target | 9 |  36.0% |
| mtm_max_hold | 2 |   8.0% |

## Performance by hour-of-day (UTC)

| hour | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| 4 | 7 |  57.1% | +0.869R | +6.083R | 3.01 |

## Performance by day-of-week (0=Mon)

| dow | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| 0 | 7 |  42.9% | +0.298R | +2.086R | 1.52 |
| 2 | 6 |  16.7% | -0.344R | -2.061R | 0.59 |
| 3 | 6 |  66.7% | +1.403R | +8.416R | 5.20 |

## Long vs short

| side | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| long | 12 |  50.0% | +0.755R | +9.059R | 2.50 |
| short | 13 |  38.5% | +0.412R | +5.358R | 1.66 |

## Performance by month

| month | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| 2025-12 | 5 |  40.0% | +0.591R | +2.953R | 1.97 |
| 2026-02 | 5 |  20.0% | -0.203R | -1.014R | 0.75 |

## Coin-flip baseline

Random-direction baseline: keep the |R| outcomes from the strategy's actual trades, randomise the sign of each, sum total R. Repeat 1000 times. The probability that random direction matches or beats the strategy is reported below.

| metric | value |
|---|---|
| strategy total R | +14.417R |
| coin-flip mean total R | -0.208R |
| coin-flip std total R | 9.99 |
| P(coin flip >= strategy) | 0.078 |

P > 0.20 means the result is indistinguishable from coin-flip noise. P < 0.05 is the conventional 'real signal' threshold. Anything in between is gray.
