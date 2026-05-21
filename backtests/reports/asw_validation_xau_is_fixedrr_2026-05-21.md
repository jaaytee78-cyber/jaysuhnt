# ASW validation report — XAU/USD (is)

_Generated 2026-05-21 21:37 UTC; strategy spec: backtests/specs/xau_asian_sweep.md._

## What this report is

Asian Sweep + Reversal logic, run on real 5-minute Polygon data with the parameters as written in `backtests/asw/params.py` and the spec. **No optimisation. No tuning.** The question: does the strategy show a measurable edge on this data window?

_Notes: In-sample window. target_mode=fixed_rr. OOS window held out separately._

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
| target_mode | fixed_rr |
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
| win rate |  33.3% |
| expectancy per trade | -0.172R |
| avg R per trade | -0.172R |
| avg win | +1.635R |
| avg loss | -1.072R |
| profit factor | 0.76 |
| total R | -73.776R |
| max drawdown | -82.453R |
| longest loss streak | 13 |
| longest win streak | 4 |

## R-multiple distribution

| bucket | count | share |
|---|---|---|
| below -1R | 236 |  54.9% |
| -1.05R to -0.5R | 34 |   7.9% |
| -0.5R to -0.05R | 15 |   3.5% |
| -0.05R to +0.05R | 3 |   0.7% |
| +0.05R to +0.5R | 14 |   3.3% |
| +0.5R to +1.0R | 8 |   1.9% |
| +1.0R to +2.0R | 120 |  27.9% |
| +2.0R to +3.0R | 0 |   0.0% |
| above +3R | 0 |   0.0% |

## Exit reason breakdown

| exit reason | count | share |
|---|---|---|
| stop | 264 |  61.4% |
| target | 118 |  27.4% |
| mtm_hard_close | 48 |  11.2% |

## Performance by hour-of-day (UTC)

| hour | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| 6 | 138 |  30.4% | -0.254R | -35.020R | 0.68 |
| 7 | 70 |  28.6% | -0.296R | -20.720R | 0.63 |
| 8 | 35 |  37.1% | -0.004R | -0.132R | 0.99 |
| 9 | 26 |  46.2% | +0.166R | +4.308R | 1.29 |
| 10 | 21 |  28.6% | -0.336R | -7.060R | 0.59 |
| 11 | 24 |  29.2% | -0.239R | -5.746R | 0.69 |
| 12 | 26 |  42.3% | +0.042R | +1.104R | 1.07 |
| 13 | 33 |  30.3% | -0.124R | -4.083R | 0.80 |
| 14 | 26 |  42.3% | -0.094R | -2.452R | 0.81 |
| 15 | 17 |  29.4% | -0.233R | -3.966R | 0.53 |
| 16 | 14 |  42.9% | -0.001R | -0.009R | 1.00 |

## Performance by day-of-week (0=Mon)

| dow | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| 0 | 75 |  29.3% | -0.322R | -24.154R | 0.60 |
| 1 | 90 |  34.4% | -0.142R | -12.814R | 0.80 |
| 2 | 93 |  35.5% | -0.031R | -2.892R | 0.95 |
| 3 | 84 |  27.4% | -0.381R | -31.984R | 0.50 |
| 4 | 88 |  38.6% | -0.022R | -1.932R | 0.97 |

## Long vs short

| side | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| long | 190 |  35.3% | -0.108R | -20.461R | 0.84 |
| short | 240 |  31.7% | -0.222R | -53.315R | 0.70 |

## Performance by month

| month | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| 2024-05 | 10 |  50.0% | +0.216R | +2.163R | 1.38 |
| 2024-06 | 27 |  40.7% | +0.049R | +1.324R | 1.07 |
| 2024-07 | 29 |  24.1% | -0.557R | -16.139R | 0.38 |
| 2024-08 | 28 |  28.6% | -0.388R | -10.862R | 0.48 |
| 2024-09 | 27 |  44.4% | +0.198R | +5.337R | 1.37 |
| 2024-10 | 29 |  37.9% | +0.080R | +2.308R | 1.13 |
| 2024-11 | 23 |  30.4% | -0.269R | -6.183R | 0.65 |
| 2024-12 | 23 |  30.4% | -0.244R | -5.602R | 0.70 |
| 2025-01 | 26 |  30.8% | -0.240R | -6.234R | 0.70 |
| 2025-02 | 22 |  36.4% | -0.320R | -7.042R | 0.53 |
| 2025-03 | 24 |  25.0% | -0.496R | -11.911R | 0.42 |
| 2025-04 | 16 |  25.0% | -0.264R | -4.217R | 0.65 |
| 2025-05 | 18 |  38.9% | +0.092R | +1.655R | 1.14 |
| 2025-06 | 23 |  43.5% | +0.165R | +3.792R | 1.31 |
| 2025-07 | 30 |  36.7% | -0.076R | -2.272R | 0.89 |
| 2025-08 | 23 |  26.1% | -0.431R | -9.910R | 0.48 |
| 2025-09 | 21 |  33.3% | -0.246R | -5.159R | 0.66 |
| 2025-10 | 21 |  23.8% | -0.227R | -4.775R | 0.67 |
| 2025-11 | 10 |  30.0% | -0.005R | -0.046R | 0.99 |

## Coin-flip baseline

Random-direction baseline: keep the |R| outcomes from the strategy's actual trades, randomise the sign of each, sum total R. Repeat 1000 times. The probability that random direction matches or beats the strategy is reported below.

| metric | value |
|---|---|
| strategy total R | -73.776R |
| coin-flip mean total R | +0.258R |
| coin-flip std total R | 28.02 |
| P(coin flip >= strategy) | 0.995 |

P > 0.20 means the result is indistinguishable from coin-flip noise. P < 0.05 is the conventional 'real signal' threshold. Anything in between is gray.
