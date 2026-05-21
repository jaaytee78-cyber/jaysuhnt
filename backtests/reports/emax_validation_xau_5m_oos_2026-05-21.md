# ASW validation report — XAU/USD (5m_oos)

_Generated 2026-05-21 22:02 UTC; strategy spec: backtests/specs/xau_asian_sweep.md._

## What this report is

Asian Sweep + Reversal logic, run on real 5-minute Polygon data with the parameters as written in `backtests/asw/params.py` and the spec. **No optimisation. No tuning.** The question: does the strategy show a measurable edge on this data window?

_Notes: OOS held-out 5m._

## Parameters used

| param | value |
|---|---|
| timeframe | 5m |
| fast_period | 9 |
| slow_period | 21 |
| atr_period | 14 |
| stop_atr | 2.0 |
| rr_ratio | 2.0 |
| hard_close_utc | 21 |
| half_spread | 0.18 |
| stop_slippage | 0.1 |

## Data window

| field | value |
|---|---|
| instrument | XAU/USD (Polygon C:XAUUSD) |
| bars (5m) | 34783 |
| first bar | 2025-11-18T23:55:00+00:00 |
| last bar | 2026-05-20T23:55:00+00:00 |

## Asian session diagnostics

_(strategy does not use Asian session levels)_

## Headline performance

| metric | value |
|---|---|
| trades total | 1594 |
| longs / shorts | 797 / 797 |
| win rate |  31.2% |
| expectancy per trade | -0.076R |
| avg R per trade | -0.076R |
| avg win | +1.679R |
| avg loss | -0.871R |
| profit factor | 0.87 |
| total R | -120.670R |
| max drawdown | -149.113R |
| longest loss streak | 20 |
| longest win streak | 4 |

## R-multiple distribution

| bucket | count | share |
|---|---|---|
| below -1R | 332 |  20.8% |
| -1.05R to -0.5R | 571 |  35.8% |
| -0.5R to -0.05R | 100 |   6.3% |
| -0.05R to +0.05R | 100 |   6.3% |
| +0.05R to +0.5R | 41 |   2.6% |
| +0.5R to +1.0R | 38 |   2.4% |
| +1.0R to +2.0R | 412 |  25.8% |
| +2.0R to +3.0R | 0 |   0.0% |
| above +3R | 0 |   0.0% |

## Exit reason breakdown

| exit reason | count | share |
|---|---|---|
| stop | 880 |  55.2% |
| target | 391 |  24.5% |
| mtm_hard_close | 323 |  20.3% |

## Performance by hour-of-day (UTC)

| hour | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| 0 | 64 |  35.9% | +0.029R | +1.867R | 1.04 |
| 1 | 57 |  45.6% | +0.327R | +18.639R | 1.58 |
| 2 | 68 |  25.0% | -0.288R | -19.576R | 0.63 |
| 3 | 54 |  29.6% | -0.187R | -10.102R | 0.75 |
| 4 | 60 |  40.0% | +0.151R | +9.075R | 1.24 |
| 5 | 75 |  34.7% | -0.008R | -0.588R | 0.99 |
| 6 | 58 |  34.5% | -0.013R | -0.781R | 0.98 |
| 7 | 81 |  30.9% | -0.117R | -9.446R | 0.84 |
| 8 | 66 |  18.2% | -0.499R | -32.947R | 0.42 |
| 9 | 77 |  26.0% | -0.267R | -20.540R | 0.66 |
| 10 | 86 |  20.9% | -0.422R | -36.328R | 0.49 |
| 11 | 89 |  36.0% | +0.027R | +2.359R | 1.04 |
| 12 | 105 |  25.7% | -0.276R | -29.021R | 0.65 |
| 13 | 87 |  40.2% | +0.157R | +13.688R | 1.26 |
| 14 | 71 |  35.2% | -0.038R | -2.718R | 0.94 |
| 15 | 60 |  48.3% | +0.174R | +10.464R | 1.36 |
| 16 | 38 |  39.5% | -0.057R | -2.175R | 0.89 |
| 17 | 62 |  45.2% | +0.089R | +5.515R | 1.18 |
| 18 | 68 |  41.2% | -0.081R | -5.504R | 0.85 |
| 19 | 64 |  34.4% | -0.117R | -7.473R | 0.75 |
| 20 | 67 |  43.3% | +0.015R | +0.974R | 1.06 |
| 21 | 34 |   0.0% | -0.047R | -1.612R | 0.00 |
| 22 | 38 |   0.0% | -0.037R | -1.421R | 0.00 |
| 23 | 65 |   0.0% | -0.046R | -3.018R | 0.00 |

## Performance by day-of-week (0=Mon)

| dow | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| 0 | 330 |  30.9% | -0.025R | -8.254R | 0.95 |
| 1 | 336 |  33.0% | -0.037R | -12.497R | 0.94 |
| 2 | 354 |  29.1% | -0.132R | -46.772R | 0.78 |
| 3 | 296 |  28.7% | -0.163R | -48.208R | 0.75 |
| 4 | 260 |  36.9% | -0.017R | -4.469R | 0.97 |
| 6 | 18 |   0.0% | -0.026R | -0.470R | 0.00 |

## Long vs short

| side | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| long | 797 |  30.1% | -0.114R | -91.141R | 0.81 |
| short | 797 |  32.2% | -0.037R | -29.529R | 0.94 |

## Performance by month

| month | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| 2025-11 | 104 |  30.8% | -0.049R | -5.049R | 0.92 |
| 2025-12 | 287 |  28.6% | -0.161R | -46.192R | 0.74 |
| 2026-01 | 268 |  29.1% | -0.191R | -51.135R | 0.71 |
| 2026-02 | 257 |  33.1% | -0.015R | -3.800R | 0.97 |
| 2026-03 | 262 |  33.2% | +0.043R | +11.337R | 1.08 |
| 2026-04 | 270 |  33.0% | -0.070R | -18.783R | 0.89 |
| 2026-05 | 146 |  30.1% | -0.048R | -7.048R | 0.91 |

## Coin-flip baseline

Random-direction baseline: keep the |R| outcomes from the strategy's actual trades, randomise the sign of each, sum total R. Repeat 1000 times. The probability that random direction matches or beats the strategy is reported below.

| metric | value |
|---|---|
| strategy total R | -120.670R |
| coin-flip mean total R | -0.868R |
| coin-flip std total R | 49.73 |
| P(coin flip >= strategy) | 0.990 |

P > 0.20 means the result is indistinguishable from coin-flip noise. P < 0.05 is the conventional 'real signal' threshold. Anything in between is gray.
