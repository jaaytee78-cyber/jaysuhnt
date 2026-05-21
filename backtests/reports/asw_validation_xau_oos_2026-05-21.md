# ASW validation report — XAU/USD (oos)

_Generated 2026-05-21 21:36 UTC; strategy spec: backtests/specs/xau_asian_sweep.md._

## What this report is

Asian Sweep + Reversal logic, run on real 5-minute Polygon data with the parameters as written in `backtests/asw/params.py` and the spec. **No optimisation. No tuning.** The question: does the strategy show a measurable edge on this data window?

_Notes: Out-of-sample held-out window. target_mode=asian_range. Strategy was NOT tuned on this window._

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
| bars (5m) | 34783 |
| first bar | 2025-11-18T23:55:00+00:00 |
| last bar | 2026-05-20T23:55:00+00:00 |

## Asian session diagnostics

| metric | value |
|---|---|
| trading days observed | 127 |
| Asian range (AH-AL)/ATR p25 | 9.46 |
| Asian range (AH-AL)/ATR median | 11.90 |
| Asian range (AH-AL)/ATR p75 | 16.10 |
| days where AL was swept | 62 ( 48.8%) |
| days where AH was swept | 83 ( 65.4%) |
| days where either was swept | 118 ( 92.9%) |
| days where both were swept | 27 ( 21.3%) |
| long signals fired | 55 |
| short signals fired | 65 |

## Headline performance

| metric | value |
|---|---|
| trades total | 119 |
| longs / shorts | 54 / 65 |
| win rate |  31.1% |
| expectancy per trade | -0.070R |
| avg R per trade | -0.070R |
| avg win | +2.057R |
| avg loss | -1.030R |
| profit factor | 0.90 |
| total R | -8.313R |
| max drawdown | -16.384R |
| longest loss streak | 9 |
| longest win streak | 4 |

## R-multiple distribution

| bucket | count | share |
|---|---|---|
| below -1R | 28 |  23.5% |
| -1.05R to -0.5R | 52 |  43.7% |
| -0.5R to -0.05R | 2 |   1.7% |
| -0.05R to +0.05R | 0 |   0.0% |
| +0.05R to +0.5R | 5 |   4.2% |
| +0.5R to +1.0R | 7 |   5.9% |
| +1.0R to +2.0R | 10 |   8.4% |
| +2.0R to +3.0R | 4 |   3.4% |
| above +3R | 11 |   9.2% |

## Exit reason breakdown

| exit reason | count | share |
|---|---|---|
| stop | 80 |  67.2% |
| target | 20 |  16.8% |
| mtm_hard_close | 19 |  16.0% |

## Performance by hour-of-day (UTC)

| hour | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| 6 | 32 |  34.4% | +0.287R | +9.187R | 1.42 |
| 7 | 17 |  17.6% | -0.085R | -1.452R | 0.90 |
| 8 | 11 |  18.2% | -0.401R | -4.415R | 0.53 |
| 9 | 5 |  60.0% | +0.743R | +3.717R | 2.78 |
| 10 | 5 |  20.0% | -0.216R | -1.078R | 0.74 |
| 11 | 6 |  33.3% | -0.491R | -2.945R | 0.29 |
| 12 | 7 |  28.6% | -0.515R | -3.604R | 0.31 |
| 13 | 9 |  22.2% | -0.492R | -4.427R | 0.39 |
| 14 | 14 |  21.4% | -0.423R | -5.922R | 0.45 |
| 15 | 8 |  50.0% | +0.073R | +0.585R | 1.17 |
| 16 | 5 |  80.0% | +0.408R | +2.042R | 2.96 |

## Performance by day-of-week (0=Mon)

| dow | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| 0 | 23 |  47.8% | +0.182R | +4.184R | 1.34 |
| 1 | 27 |  25.9% | -0.239R | -6.463R | 0.68 |
| 2 | 26 |  34.6% | +0.269R | +6.995R | 1.39 |
| 3 | 18 |  22.2% | -0.181R | -3.265R | 0.78 |
| 4 | 25 |  24.0% | -0.391R | -9.764R | 0.49 |

## Long vs short

| side | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| long | 54 |  33.3% | -0.125R | -6.729R | 0.82 |
| short | 65 |  29.2% | -0.024R | -1.585R | 0.97 |

## Performance by month

| month | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| 2025-11 | 5 |  40.0% | -0.188R | -0.942R | 0.71 |
| 2025-12 | 27 |  37.0% | +0.024R | +0.644R | 1.04 |
| 2026-01 | 20 |  35.0% | -0.024R | -0.484R | 0.96 |
| 2026-02 | 14 |  21.4% | -0.031R | -0.430R | 0.96 |
| 2026-03 | 19 |  31.6% | +0.087R | +1.658R | 1.13 |
| 2026-04 | 21 |  33.3% | -0.059R | -1.244R | 0.91 |
| 2026-05 | 13 |  15.4% | -0.578R | -7.517R | 0.34 |

## Coin-flip baseline

Random-direction baseline: keep the |R| outcomes from the strategy's actual trades, randomise the sign of each, sum total R. Repeat 1000 times. The probability that random direction matches or beats the strategy is reported below.

| metric | value |
|---|---|
| strategy total R | -8.313R |
| coin-flip mean total R | +0.673R |
| coin-flip std total R | 18.05 |
| P(coin flip >= strategy) | 0.705 |

P > 0.20 means the result is indistinguishable from coin-flip noise. P < 0.05 is the conventional 'real signal' threshold. Anything in between is gray.
