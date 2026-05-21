# ASW validation report — XAU/USD (is)

_Generated 2026-05-21 21:36 UTC; strategy spec: backtests/specs/xau_asian_sweep.md._

## What this report is

Asian Sweep + Reversal logic, run on real 5-minute Polygon data with the parameters as written in `backtests/asw/params.py` and the spec. **No optimisation. No tuning.** The question: does the strategy show a measurable edge on this data window?

_Notes: In-sample window. target_mode=asian_range. OOS window held out separately._

## Parameters used

| param | value |
|---|---|
| asia_start_utc | 22 |
| asia_end_utc | 6 |
| trade_cutoff_utc | 17 |
| hard_close_utc | 21 |
| sweep_buffer | 0.0 |
| reclaim_window_bars | 48 |
| atr_period | 14 |
| stop_buffer_atr | 0.5 |
| target_mode | asian_range |
| rr_ratio (if fixed_rr) | 2.0 |
| min_asian_range_atr | 1.0 |
| half_spread (cost model) | 0.18 |
| stop_slippage (cost model) | 0.1 |

## Data window

| field | value |
|---|---|
| instrument | XAU/USD (Polygon C:XAUUSD) |
| bars (5m) | 105782 |
| first bar | 2024-05-21T00:00:00+00:00 |
| last bar | 2025-11-18T23:50:00+00:00 |

## Asian session diagnostics

| metric | value |
|---|---|
| trading days observed | 386 |
| Asian range (AH-AL)/ATR p25 | 8.99 |
| Asian range (AH-AL)/ATR median | 10.81 |
| Asian range (AH-AL)/ATR p75 | 13.20 |
| days where AL was swept | 217 ( 56.2%) |
| days where AH was swept | 272 ( 70.5%) |
| days where either was swept | 376 ( 97.4%) |
| days where both were swept | 113 ( 29.3%) |
| long signals fired | 190 |
| short signals fired | 240 |

## Headline performance

| metric | value |
|---|---|
| trades total | 430 |
| longs / shorts | 190 / 240 |
| win rate |  24.2% |
| expectancy per trade | -0.243R |
| avg R per trade | -0.243R |
| avg win | +2.455R |
| avg loss | -1.103R |
| profit factor | 0.71 |
| total R | -104.399R |
| max drawdown | -121.772R |
| longest loss streak | 16 |
| longest win streak | 5 |

## R-multiple distribution

| bucket | count | share |
|---|---|---|
| below -1R | 279 |  64.9% |
| -1.05R to -0.5R | 34 |   7.9% |
| -0.5R to -0.05R | 11 |   2.6% |
| -0.05R to +0.05R | 4 |   0.9% |
| +0.05R to +0.5R | 16 |   3.7% |
| +0.5R to +1.0R | 14 |   3.3% |
| +1.0R to +2.0R | 27 |   6.3% |
| +2.0R to +3.0R | 20 |   4.7% |
| above +3R | 25 |   5.8% |

## Exit reason breakdown

| exit reason | count | share |
|---|---|---|
| stop | 307 |  71.4% |
| target | 78 |  18.1% |
| mtm_hard_close | 45 |  10.5% |

## Performance by hour-of-day (UTC)

| hour | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| 6 | 138 |  15.9% | -0.241R | -33.217R | 0.76 |
| 7 | 70 |  18.6% | -0.366R | -25.599R | 0.61 |
| 8 | 35 |  22.9% | -0.451R | -15.772R | 0.49 |
| 9 | 26 |  26.9% | -0.008R | -0.214R | 0.99 |
| 10 | 21 |  19.0% | -0.584R | -12.264R | 0.37 |
| 11 | 24 |  16.7% | -0.511R | -12.268R | 0.46 |
| 12 | 26 |  38.5% | -0.044R | -1.132R | 0.93 |
| 13 | 33 |  36.4% | -0.032R | -1.067R | 0.95 |
| 14 | 26 |  53.8% | +0.034R | +0.880R | 1.08 |
| 15 | 17 |  29.4% | -0.152R | -2.581R | 0.70 |
| 16 | 14 |  35.7% | -0.083R | -1.165R | 0.84 |

## Performance by day-of-week (0=Mon)

| dow | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| 0 | 75 |  17.3% | -0.349R | -26.161R | 0.63 |
| 1 | 90 |  25.6% | -0.141R | -12.659R | 0.83 |
| 2 | 93 |  25.8% | -0.192R | -17.846R | 0.76 |
| 3 | 84 |  22.6% | -0.265R | -22.266R | 0.68 |
| 4 | 88 |  28.4% | -0.289R | -25.468R | 0.64 |

## Long vs short

| side | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| long | 190 |  27.4% | -0.093R | -17.697R | 0.88 |
| short | 240 |  21.7% | -0.361R | -86.702R | 0.58 |

## Performance by month

| month | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| 2024-05 | 10 |  30.0% | -0.376R | -3.765R | 0.53 |
| 2024-06 | 27 |  37.0% | +0.210R | +5.674R | 1.29 |
| 2024-07 | 29 |  10.3% | -0.920R | -26.678R | 0.14 |
| 2024-08 | 28 |  25.0% | -0.359R | -10.040R | 0.55 |
| 2024-09 | 27 |  48.1% | +0.194R | +5.233R | 1.34 |
| 2024-10 | 29 |  24.1% | -0.265R | -7.693R | 0.68 |
| 2024-11 | 23 |  17.4% | -0.642R | -14.773R | 0.31 |
| 2024-12 | 23 |  21.7% | +0.132R | +3.033R | 1.14 |
| 2025-01 | 26 |  15.4% | -0.547R | -14.228R | 0.45 |
| 2025-02 | 22 |  27.3% | -0.646R | -14.212R | 0.23 |
| 2025-03 | 24 |  25.0% | -0.271R | -6.494R | 0.69 |
| 2025-04 | 16 |  12.5% | -0.744R | -11.898R | 0.16 |
| 2025-05 | 18 |  22.2% | -0.238R | -4.292R | 0.72 |
| 2025-06 | 23 |  30.4% | -0.204R | -4.703R | 0.70 |
| 2025-07 | 30 |  33.3% | +0.423R | +12.697R | 1.57 |
| 2025-08 | 23 |  13.0% | -0.508R | -11.673R | 0.49 |
| 2025-09 | 21 |  28.6% | +0.827R | +17.372R | 2.06 |
| 2025-10 | 21 |  14.3% | -0.525R | -11.016R | 0.34 |
| 2025-11 | 10 |  10.0% | -0.694R | -6.942R | 0.14 |

## Coin-flip baseline

Random-direction baseline: keep the |R| outcomes from the strategy's actual trades, randomise the sign of each, sum total R. Repeat 1000 times. The probability that random direction matches or beats the strategy is reported below.

| metric | value |
|---|---|
| strategy total R | -104.399R |
| coin-flip mean total R | -1.036R |
| coin-flip std total R | 43.11 |
| P(coin flip >= strategy) | 0.992 |

P > 0.20 means the result is indistinguishable from coin-flip noise. P < 0.05 is the conventional 'real signal' threshold. Anything in between is gray.
