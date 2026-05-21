# ASW validation report — XAU/USD (is)

_Generated 2026-05-21 21:49 UTC; strategy spec: backtests/specs/xau_asian_sweep.md._

## What this report is

Asian Sweep + Reversal logic, run on real 5-minute Polygon data with the parameters as written in `backtests/asw/params.py` and the spec. **No optimisation. No tuning.** The question: does the strategy show a measurable edge on this data window?

_Notes: In-sample window. 5m XAU momentum continuation._

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
| long signals fired | 249 |
| short signals fired | 189 |

## Headline performance

| metric | value |
|---|---|
| trades total | 438 |
| longs / shorts | 249 / 189 |
| win rate |  41.6% |
| expectancy per trade | -0.157R |
| avg R per trade | -0.157R |
| avg win | +1.331R |
| avg loss | -1.214R |
| profit factor | 0.78 |
| total R | -68.601R |
| max drawdown | -83.837R |
| longest loss streak | 12 |
| longest win streak | 10 |

## R-multiple distribution

| bucket | count | share |
|---|---|---|
| below -1R | 247 |  56.4% |
| -1.05R to -0.5R | 9 |   2.1% |
| -0.5R to -0.05R | 0 |   0.0% |
| -0.05R to +0.05R | 0 |   0.0% |
| +0.05R to +0.5R | 2 |   0.5% |
| +0.5R to +1.0R | 0 |   0.0% |
| +1.0R to +2.0R | 180 |  41.1% |
| +2.0R to +3.0R | 0 |   0.0% |
| above +3R | 0 |   0.0% |

## Exit reason breakdown

| exit reason | count | share |
|---|---|---|
| stop | 256 |  58.4% |
| target | 180 |  41.1% |
| mtm_hard_close | 2 |   0.5% |

## Performance by hour-of-day (UTC)

| hour | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| 6 | 150 |  38.7% | -0.263R | -39.462R | 0.66 |
| 7 | 60 |  50.0% | +0.055R | +3.315R | 1.09 |
| 8 | 44 |  50.0% | +0.068R | +3.012R | 1.11 |
| 9 | 23 |  43.5% | -0.100R | -2.294R | 0.85 |
| 10 | 23 |  39.1% | -0.233R | -5.351R | 0.69 |
| 11 | 22 |  18.2% | -0.738R | -16.244R | 0.26 |
| 12 | 30 |  40.0% | -0.238R | -7.148R | 0.67 |
| 13 | 36 |  33.3% | -0.294R | -10.571R | 0.61 |
| 14 | 31 |  51.6% | +0.165R | +5.102R | 1.29 |
| 15 | 9 |  55.6% | +0.274R | +2.469R | 1.53 |
| 16 | 10 |  40.0% | -0.143R | -1.429R | 0.79 |

## Performance by day-of-week (0=Mon)

| dow | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| 0 | 79 |  36.7% | -0.292R | -23.103R | 0.63 |
| 1 | 93 |  40.9% | -0.168R | -15.642R | 0.77 |
| 2 | 89 |  40.4% | -0.178R | -15.833R | 0.75 |
| 3 | 85 |  56.5% | +0.224R | +19.046R | 1.43 |
| 4 | 92 |  33.7% | -0.359R | -33.069R | 0.55 |

## Long vs short

| side | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| long | 249 |  39.4% | -0.222R | -55.356R | 0.70 |
| short | 189 |  44.4% | -0.070R | -13.245R | 0.90 |

## Performance by month

| month | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| 2024-05 | 11 |  27.3% | -0.552R | -6.069R | 0.40 |
| 2024-06 | 26 |  38.5% | -0.299R | -7.784R | 0.62 |
| 2024-07 | 29 |  34.5% | -0.392R | -11.356R | 0.52 |
| 2024-08 | 26 |  30.8% | -0.434R | -11.294R | 0.49 |
| 2024-09 | 26 |  42.3% | -0.171R | -4.455R | 0.76 |
| 2024-10 | 28 |  35.7% | -0.324R | -9.077R | 0.58 |
| 2024-11 | 23 |  30.4% | -0.459R | -10.546R | 0.47 |
| 2024-12 | 24 |  37.5% | -0.294R | -7.066R | 0.62 |
| 2025-01 | 25 |  32.0% | -0.471R | -11.777R | 0.45 |
| 2025-02 | 22 |  54.5% | +0.194R | +4.258R | 1.36 |
| 2025-03 | 24 |  50.0% | +0.032R | +0.757R | 1.05 |
| 2025-04 | 19 |  42.1% | -0.031R | -0.596R | 0.95 |
| 2025-05 | 22 |  59.1% | +0.358R | +7.884R | 1.77 |
| 2025-06 | 23 |  56.5% | +0.289R | +6.655R | 1.58 |
| 2025-07 | 28 |  25.0% | -0.603R | -16.881R | 0.33 |
| 2025-08 | 21 |  38.1% | -0.259R | -5.446R | 0.67 |
| 2025-09 | 23 |  52.2% | +0.123R | +2.832R | 1.22 |
| 2025-10 | 26 |  65.4% | +0.547R | +14.215R | 2.40 |
| 2025-11 | 12 |  33.3% | -0.238R | -2.855R | 0.67 |

## Coin-flip baseline

Random-direction baseline: keep the |R| outcomes from the strategy's actual trades, randomise the sign of each, sum total R. Repeat 1000 times. The probability that random direction matches or beats the strategy is reported below.

| metric | value |
|---|---|
| strategy total R | -68.601R |
| coin-flip mean total R | +0.256R |
| coin-flip std total R | 25.83 |
| P(coin flip >= strategy) | 0.995 |

P > 0.20 means the result is indistinguishable from coin-flip noise. P < 0.05 is the conventional 'real signal' threshold. Anything in between is gray.
