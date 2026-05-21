# ASW validation report — XAU/USD (is)

_Generated 2026-05-21 21:48 UTC; strategy spec: backtests/specs/xau_asian_sweep.md._

## What this report is

Asian Sweep + Reversal logic, run on real 5-minute Polygon data with the parameters as written in `backtests/asw/params.py` and the spec. **No optimisation. No tuning.** The question: does the strategy show a measurable edge on this data window?

_Notes: In-sample window. Donchian 4h on XAU._

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
| bars (5m) | 2392 |
| first bar | 2024-05-21T00:00:00+00:00 |
| last bar | 2025-11-18T16:00:00+00:00 |

## Asian session diagnostics

_(strategy does not use Asian session levels)_

## Headline performance

| metric | value |
|---|---|
| trades total | 149 |
| longs / shorts | 105 / 44 |
| win rate |  28.2% |
| expectancy per trade | +0.101R |
| avg R per trade | +0.101R |
| avg win | +2.928R |
| avg loss | -1.009R |
| profit factor | 1.14 |
| total R | +15.035R |
| max drawdown | -26.493R |
| longest loss streak | 19 |
| longest win streak | 6 |

## R-multiple distribution

| bucket | count | share |
|---|---|---|
| below -1R | 0 |   0.0% |
| -1.05R to -0.5R | 106 |  71.1% |
| -0.5R to -0.05R | 1 |   0.7% |
| -0.05R to +0.05R | 0 |   0.0% |
| +0.05R to +0.5R | 1 |   0.7% |
| +0.5R to +1.0R | 0 |   0.0% |
| +1.0R to +2.0R | 0 |   0.0% |
| +2.0R to +3.0R | 41 |  27.5% |
| above +3R | 0 |   0.0% |

## Exit reason breakdown

| exit reason | count | share |
|---|---|---|
| stop | 105 |  70.5% |
| target | 41 |  27.5% |
| mtm_max_hold | 3 |   2.0% |

## Performance by hour-of-day (UTC)

| hour | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| 0 | 28 |  32.1% | +0.271R | +7.584R | 1.39 |
| 4 | 18 |  44.4% | +0.762R | +13.709R | 2.35 |
| 8 | 25 |  16.0% | -0.379R | -9.479R | 0.56 |
| 12 | 51 |  27.5% | +0.049R | +2.522R | 1.07 |
| 16 | 17 |  29.4% | +0.167R | +2.834R | 1.23 |
| 20 | 10 |  20.0% | -0.214R | -2.136R | 0.74 |

## Performance by day-of-week (0=Mon)

| dow | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| 0 | 31 |  25.8% | +0.021R | +0.636R | 1.03 |
| 1 | 33 |  27.3% | -0.001R | -0.040R | 1.00 |
| 2 | 29 |  20.7% | -0.189R | -5.494R | 0.77 |
| 3 | 24 |  33.3% | +0.315R | +7.558R | 1.46 |
| 4 | 29 |  34.5% | +0.394R | +11.425R | 1.62 |

## Long vs short

| side | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| long | 105 |  38.1% | +0.507R | +53.252R | 1.80 |
| short | 44 |   4.5% | -0.869R | -38.217R | 0.08 |

## Performance by month

| month | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| 2024-06 | 5 |   0.0% | -1.024R | -5.120R | 0.00 |
| 2024-07 | 11 |  18.2% | -0.295R | -3.247R | 0.65 |
| 2024-08 | 6 |  33.3% | +0.315R | +1.889R | 1.46 |
| 2024-09 | 10 |  30.0% | +0.179R | +1.785R | 1.25 |
| 2024-10 | 9 |  44.4% | +0.757R | +6.816R | 2.33 |
| 2024-11 | 8 |  25.0% | -0.017R | -0.137R | 0.98 |
| 2024-12 | 8 |   0.0% | -1.023R | -8.180R | 0.00 |
| 2025-01 | 8 |  50.0% | +0.978R | +7.821R | 2.90 |
| 2025-02 | 8 |  25.0% | -0.018R | -0.141R | 0.98 |
| 2025-03 | 8 |  50.0% | +0.983R | +7.865R | 2.93 |
| 2025-04 | 8 |  37.5% | +0.490R | +3.921R | 1.77 |
| 2025-05 | 9 |  11.1% | -0.566R | -5.092R | 0.37 |
| 2025-06 | 7 |   0.0% | -1.013R | -7.092R | 0.00 |
| 2025-07 | 9 |   0.0% | -1.019R | -9.170R | 0.00 |
| 2025-08 | 12 |  50.0% | +0.984R | +11.813R | 2.93 |
| 2025-09 | 9 |  55.6% | +1.210R | +10.893R | 3.68 |
| 2025-10 | 8 |  37.5% | +0.179R | +1.430R | 1.28 |
| 2025-11 | 6 |  16.7% | -0.170R | -1.019R | 0.75 |

## Coin-flip baseline

Random-direction baseline: keep the |R| outcomes from the strategy's actual trades, randomise the sign of each, sum total R. Repeat 1000 times. The probability that random direction matches or beats the strategy is reported below.

| metric | value |
|---|---|
| strategy total R | +15.035R |
| coin-flip mean total R | +0.009R |
| coin-flip std total R | 22.61 |
| P(coin flip >= strategy) | 0.247 |

P > 0.20 means the result is indistinguishable from coin-flip noise. P < 0.05 is the conventional 'real signal' threshold. Anything in between is gray.
