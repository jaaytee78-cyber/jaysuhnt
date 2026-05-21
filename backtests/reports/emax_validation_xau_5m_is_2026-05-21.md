# ASW validation report — XAU/USD (5m_is)

_Generated 2026-05-21 22:02 UTC; strategy spec: backtests/specs/xau_asian_sweep.md._

## What this report is

Asian Sweep + Reversal logic, run on real 5-minute Polygon data with the parameters as written in `backtests/asw/params.py` and the spec. **No optimisation. No tuning.** The question: does the strategy show a measurable edge on this data window?

_Notes: In-sample 5m 9/21 EMA cross._

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
| bars (5m) | 105782 |
| first bar | 2024-05-21T00:00:00+00:00 |
| last bar | 2025-11-18T23:50:00+00:00 |

## Asian session diagnostics

_(strategy does not use Asian session levels)_

## Headline performance

| metric | value |
|---|---|
| trades total | 4828 |
| longs / shorts | 2414 / 2414 |
| win rate |  33.1% |
| expectancy per trade | -0.085R |
| avg R per trade | -0.085R |
| avg win | +1.627R |
| avg loss | -0.934R |
| profit factor | 0.86 |
| total R | -412.520R |
| max drawdown | -463.330R |
| longest loss streak | 21 |
| longest win streak | 5 |

## R-multiple distribution

| bucket | count | share |
|---|---|---|
| below -1R | 2382 |  49.3% |
| -1.05R to -0.5R | 228 |   4.7% |
| -0.5R to -0.05R | 556 |  11.5% |
| -0.05R to +0.05R | 80 |   1.7% |
| +0.05R to +0.5R | 136 |   2.8% |
| +0.5R to +1.0R | 117 |   2.4% |
| +1.0R to +2.0R | 1329 |  27.5% |
| +2.0R to +3.0R | 0 |   0.0% |
| above +3R | 0 |   0.0% |

## Exit reason breakdown

| exit reason | count | share |
|---|---|---|
| stop | 2540 |  52.6% |
| target | 1254 |  26.0% |
| mtm_hard_close | 1034 |  21.4% |

## Performance by hour-of-day (UTC)

| hour | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| 0 | 239 |  35.6% | -0.094R | -22.390R | 0.88 |
| 1 | 263 |  35.4% | -0.062R | -16.210R | 0.92 |
| 2 | 200 |  37.5% | +0.006R | +1.292R | 1.01 |
| 3 | 168 |  40.5% | +0.087R | +14.651R | 1.13 |
| 4 | 154 |  30.5% | -0.228R | -35.064R | 0.72 |
| 5 | 243 |  36.6% | -0.041R | -10.008R | 0.94 |
| 6 | 208 |  35.1% | -0.076R | -15.713R | 0.90 |
| 7 | 231 |  36.4% | -0.034R | -7.871R | 0.95 |
| 8 | 193 |  31.1% | -0.186R | -35.951R | 0.76 |
| 9 | 213 |  30.5% | -0.205R | -43.631R | 0.74 |
| 10 | 214 |  35.5% | -0.052R | -11.135R | 0.93 |
| 11 | 244 |  37.7% | +0.014R | +3.342R | 1.02 |
| 12 | 248 |  33.5% | -0.105R | -26.157R | 0.86 |
| 13 | 257 |  38.9% | +0.041R | +10.548R | 1.06 |
| 14 | 196 |  37.2% | -0.070R | -13.656R | 0.89 |
| 15 | 164 |  42.7% | -0.000R | -0.065R | 1.00 |
| 16 | 172 |  39.5% | -0.173R | -29.787R | 0.71 |
| 17 | 209 |  37.3% | -0.234R | -48.995R | 0.62 |
| 18 | 202 |  42.1% | -0.112R | -22.718R | 0.80 |
| 19 | 183 |  41.0% | -0.068R | -12.428R | 0.85 |
| 20 | 177 |  34.5% | -0.168R | -29.769R | 0.48 |
| 21 | 63 |   0.0% | -0.152R | -9.578R | 0.00 |
| 22 | 152 |   0.0% | -0.123R | -18.710R | 0.00 |
| 23 | 235 |   0.0% | -0.138R | -32.518R | 0.00 |

## Performance by day-of-week (0=Mon)

| dow | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| 0 | 934 |  33.6% | -0.066R | -61.789R | 0.89 |
| 1 | 1001 |  31.8% | -0.131R | -130.968R | 0.79 |
| 2 | 981 |  31.3% | -0.122R | -119.219R | 0.81 |
| 3 | 930 |  36.1% | -0.009R | -8.299R | 0.98 |
| 4 | 909 |  35.8% | -0.093R | -84.796R | 0.86 |
| 6 | 73 |   0.0% | -0.102R | -7.449R | 0.00 |

## Long vs short

| side | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| long | 2414 |  33.8% | -0.082R | -198.154R | 0.87 |
| short | 2414 |  32.4% | -0.089R | -214.366R | 0.86 |

## Performance by month

| month | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| 2024-05 | 134 |  24.6% | -0.357R | -47.796R | 0.52 |
| 2024-06 | 254 |  27.2% | -0.240R | -60.844R | 0.64 |
| 2024-07 | 271 |  35.8% | -0.093R | -25.329R | 0.86 |
| 2024-08 | 285 |  33.0% | -0.144R | -40.981R | 0.78 |
| 2024-09 | 276 |  36.6% | -0.049R | -13.519R | 0.92 |
| 2024-10 | 274 |  28.5% | -0.208R | -56.961R | 0.68 |
| 2024-11 | 247 |  34.8% | -0.074R | -18.377R | 0.88 |
| 2024-12 | 275 |  34.9% | -0.091R | -25.158R | 0.86 |
| 2025-01 | 275 |  30.5% | -0.166R | -45.670R | 0.74 |
| 2025-02 | 249 |  35.3% | -0.030R | -7.530R | 0.95 |
| 2025-03 | 269 |  36.4% | -0.002R | -0.609R | 1.00 |
| 2025-04 | 230 |  37.0% | +0.075R | +17.136R | 1.13 |
| 2025-05 | 256 |  34.4% | -0.072R | -18.531R | 0.89 |
| 2025-06 | 255 |  38.4% | +0.112R | +28.486R | 1.21 |
| 2025-07 | 283 |  29.7% | -0.203R | -57.417R | 0.69 |
| 2025-08 | 298 |  28.5% | -0.176R | -52.409R | 0.74 |
| 2025-09 | 275 |  30.2% | -0.075R | -20.588R | 0.87 |
| 2025-10 | 274 |  37.6% | +0.088R | +24.173R | 1.16 |
| 2025-11 | 148 |  33.8% | +0.064R | +9.404R | 1.11 |

## Coin-flip baseline

Random-direction baseline: keep the |R| outcomes from the strategy's actual trades, randomise the sign of each, sum total R. Repeat 1000 times. The probability that random direction matches or beats the strategy is reported below.

| metric | value |
|---|---|
| strategy total R | -412.520R |
| coin-flip mean total R | -0.891R |
| coin-flip std total R | 88.48 |
| P(coin flip >= strategy) | 1.000 |

P > 0.20 means the result is indistinguishable from coin-flip noise. P < 0.05 is the conventional 'real signal' threshold. Anything in between is gray.
