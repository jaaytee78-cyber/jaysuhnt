# ASW validation report — XAU/USD (oos)

_Generated 2026-05-21 21:37 UTC; strategy spec: backtests/specs/xau_asian_sweep.md._

## What this report is

Asian Sweep + Reversal logic, run on real 5-minute Polygon data with the parameters as written in `backtests/asw/params.py` and the spec. **No optimisation. No tuning.** The question: does the strategy show a measurable edge on this data window?

_Notes: Out-of-sample held-out window. target_mode=fixed_rr. Strategy was NOT tuned on this window._

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
| trades total | 120 |
| longs / shorts | 55 / 65 |
| win rate |  40.8% |
| expectancy per trade | +0.057R |
| avg R per trade | +0.057R |
| avg win | +1.625R |
| avg loss | -1.026R |
| profit factor | 1.09 |
| total R | +6.787R |
| max drawdown | -12.938R |
| longest loss streak | 8 |
| longest win streak | 4 |

## R-multiple distribution

| bucket | count | share |
|---|---|---|
| below -1R | 23 |  19.2% |
| -1.05R to -0.5R | 46 |  38.3% |
| -0.5R to -0.05R | 2 |   1.7% |
| -0.05R to +0.05R | 0 |   0.0% |
| +0.05R to +0.5R | 4 |   3.3% |
| +0.5R to +1.0R | 6 |   5.0% |
| +1.0R to +2.0R | 39 |  32.5% |
| +2.0R to +3.0R | 0 |   0.0% |
| above +3R | 0 |   0.0% |

## Exit reason breakdown

| exit reason | count | share |
|---|---|---|
| stop | 69 |  57.5% |
| target | 36 |  30.0% |
| mtm_hard_close | 15 |  12.5% |

## Performance by hour-of-day (UTC)

| hour | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| 6 | 32 |  43.8% | +0.225R | +7.188R | 1.38 |
| 7 | 17 |  41.2% | +0.179R | +3.051R | 1.28 |
| 8 | 11 |  27.3% | -0.222R | -2.441R | 0.71 |
| 9 | 5 |  60.0% | +0.472R | +2.362R | 2.14 |
| 10 | 5 |  60.0% | +0.763R | +3.816R | 2.82 |
| 11 | 6 |  33.3% | -0.222R | -1.333R | 0.68 |
| 12 | 7 |  28.6% | -0.551R | -3.859R | 0.26 |
| 13 | 10 |  30.0% | -0.289R | -2.895R | 0.60 |
| 14 | 14 |  28.6% | -0.205R | -2.873R | 0.70 |
| 15 | 8 |  50.0% | +0.014R | +0.112R | 1.03 |
| 16 | 5 |  80.0% | +0.732R | +3.660R | 4.51 |

## Performance by day-of-week (0=Mon)

| dow | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| 0 | 23 |  52.2% | +0.129R | +2.973R | 1.26 |
| 1 | 27 |  37.0% | +0.051R | +1.378R | 1.08 |
| 2 | 27 |  48.1% | +0.301R | +8.114R | 1.55 |
| 3 | 18 |  33.3% | -0.045R | -0.817R | 0.94 |
| 4 | 25 |  32.0% | -0.194R | -4.860R | 0.72 |

## Long vs short

| side | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| long | 55 |  41.8% | +0.021R | +1.136R | 1.04 |
| short | 65 |  40.0% | +0.087R | +5.652R | 1.14 |

## Performance by month

| month | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| 2025-11 | 5 |  60.0% | +0.752R | +3.762R | 2.79 |
| 2025-12 | 27 |  48.1% | +0.204R | +5.495R | 1.37 |
| 2026-01 | 20 |  50.0% | +0.288R | +5.757R | 1.55 |
| 2026-02 | 15 |  33.3% | -0.095R | -1.418R | 0.85 |
| 2026-03 | 19 |  36.8% | -0.008R | -0.160R | 0.99 |
| 2026-04 | 21 |  33.3% | -0.154R | -3.234R | 0.78 |
| 2026-05 | 13 |  30.8% | -0.263R | -3.414R | 0.64 |

## Coin-flip baseline

Random-direction baseline: keep the |R| outcomes from the strategy's actual trades, randomise the sign of each, sum total R. Repeat 1000 times. The probability that random direction matches or beats the strategy is reported below.

| metric | value |
|---|---|
| strategy total R | +6.787R |
| coin-flip mean total R | +0.337R |
| coin-flip std total R | 15.03 |
| P(coin flip >= strategy) | 0.342 |

P > 0.20 means the result is indistinguishable from coin-flip noise. P < 0.05 is the conventional 'real signal' threshold. Anything in between is gray.
