# ASW validation report — XAU/USD (oos)

_Generated 2026-05-21 21:49 UTC; strategy spec: backtests/specs/xau_asian_sweep.md._

## What this report is

Asian Sweep + Reversal logic, run on real 5-minute Polygon data with the parameters as written in `backtests/asw/params.py` and the spec. **No optimisation. No tuning.** The question: does the strategy show a measurable edge on this data window?

_Notes: Out-of-sample held-out window._

## Parameters used

| param | value |
|---|---|
| asia_start_utc | 22 |
| asia_end_utc | 6 |
| trade_cutoff_utc | 17 |
| hard_close_utc | 21 |
| displacement_atr | 0.25 |
| atr_period | 14 |
| stop_buffer_atr | 0.5 |
| rr_ratio | 1.5 |
| min_asian_range_atr | 1.0 |
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
| long signals fired | 71 |
| short signals fired | 49 |

## Headline performance

| metric | value |
|---|---|
| trades total | 120 |
| longs / shorts | 71 / 49 |
| win rate |  40.0% |
| expectancy per trade | -0.079R |
| avg R per trade | -0.079R |
| avg win | +1.404R |
| avg loss | -1.067R |
| profit factor | 0.88 |
| total R | -9.466R |
| max drawdown | -12.761R |
| longest loss streak | 10 |
| longest win streak | 5 |

## R-multiple distribution

| bucket | count | share |
|---|---|---|
| below -1R | 48 |  40.0% |
| -1.05R to -0.5R | 24 |  20.0% |
| -0.5R to -0.05R | 0 |   0.0% |
| -0.05R to +0.05R | 0 |   0.0% |
| +0.05R to +0.5R | 1 |   0.8% |
| +0.5R to +1.0R | 1 |   0.8% |
| +1.0R to +2.0R | 46 |  38.3% |
| +2.0R to +3.0R | 0 |   0.0% |
| above +3R | 0 |   0.0% |

## Exit reason breakdown

| exit reason | count | share |
|---|---|---|
| stop | 72 |  60.0% |
| target | 46 |  38.3% |
| mtm_hard_close | 2 |   1.7% |

## Performance by hour-of-day (UTC)

| hour | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| 6 | 31 |  35.5% | -0.186R | -5.755R | 0.73 |
| 7 | 12 |  50.0% | +0.174R | +2.087R | 1.32 |
| 8 | 12 |  16.7% | -0.650R | -7.799R | 0.27 |
| 9 | 5 |  40.0% | -0.100R | -0.500R | 0.85 |
| 10 | 7 |  42.9% | -0.009R | -0.065R | 0.99 |
| 12 | 6 |  66.7% | +0.600R | +3.599R | 2.68 |
| 13 | 12 |  58.3% | +0.411R | +4.935R | 1.94 |
| 14 | 12 |  41.7% | -0.054R | -0.647R | 0.91 |
| 15 | 12 |  50.0% | +0.208R | +2.491R | 1.40 |
| 16 | 9 |  22.2% | -0.628R | -5.652R | 0.24 |

## Performance by day-of-week (0=Mon)

| dow | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| 0 | 24 |  45.8% | +0.079R | +1.905R | 1.14 |
| 1 | 25 |  40.0% | -0.066R | -1.657R | 0.90 |
| 2 | 22 |  31.8% | -0.300R | -6.599R | 0.59 |
| 3 | 20 |  35.0% | -0.250R | -4.997R | 0.64 |
| 4 | 29 |  44.8% | +0.065R | +1.881R | 1.11 |

## Long vs short

| side | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| long | 71 |  49.3% | +0.154R | +10.937R | 1.28 |
| short | 49 |  26.5% | -0.416R | -20.403R | 0.46 |

## Performance by month

| month | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| 2025-11 | 6 |  33.3% | -0.243R | -1.459R | 0.66 |
| 2025-12 | 25 |  40.0% | -0.087R | -2.175R | 0.87 |
| 2026-01 | 20 |  35.0% | -0.184R | -3.682R | 0.73 |
| 2026-02 | 16 |  62.5% | +0.441R | +7.055R | 2.11 |
| 2026-03 | 20 |  35.0% | -0.174R | -3.473R | 0.75 |
| 2026-04 | 21 |  33.3% | -0.228R | -4.796R | 0.68 |
| 2026-05 | 12 |  41.7% | -0.078R | -0.936R | 0.88 |

## Coin-flip baseline

Random-direction baseline: keep the |R| outcomes from the strategy's actual trades, randomise the sign of each, sum total R. Repeat 1000 times. The probability that random direction matches or beats the strategy is reported below.

| metric | value |
|---|---|
| strategy total R | -9.466R |
| coin-flip mean total R | +0.266R |
| coin-flip std total R | 13.57 |
| P(coin flip >= strategy) | 0.776 |

P > 0.20 means the result is indistinguishable from coin-flip noise. P < 0.05 is the conventional 'real signal' threshold. Anything in between is gray.
