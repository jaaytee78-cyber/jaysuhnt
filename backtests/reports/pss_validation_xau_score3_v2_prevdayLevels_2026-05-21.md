# PSS validation report — XAU/USD

_Generated 2026-05-21 21:10 UTC; data source: Polygon `C:XAUUSD`._

## What this report is

PSS Phase-4 logic, ported bit-exactly from `indicators/pine-script/phase4_signals.pine`, run on real 5-minute Polygon data with the parameters as currently written in the .pine file. **No optimisation. No tuning.** The only question being answered: does the strategy as written show a measurable edge on this data?

_Notes: Spot gold via Polygon forex. Volume is contributed-bank tick count, not exchange volume.

DIAGNOSTIC OVERRIDE: min_score forced to 3 (.pine value is 4). All other params unchanged._

## Parameters used

| param | value |
|---|---|
| sd_mult | 1.5 |
| atr_period | 14 |
| stop_mult | 2.0 |
| rr_ratio | 2.0 |
| cooldown | 12 |
| level_tol | 0.25 |
| compress_pct | 0.85 |
| min_score | 3 |
| hour_filter | True |
| hour_start_utc | 7 |
| hour_end_utc | 16 |
| half_spread (cost model) | 0.18 |
| stop_slippage (cost model) | 0.1 |

## Data window

| field | value |
|---|---|
| instrument | XAU/USD |
| polygon ticker | C:XAUUSD |
| bars (5m) | 140565 |
| first bar | 2024-05-21T00:00:00+00:00 |
| last bar | 2026-05-20T23:55:00+00:00 |

## Signal frequency

| counter | value |
|---|---|
| long candidates (pre-cooldown) | 50 |
| short candidates (pre-cooldown) | 51 |
| long fires (post-cooldown) | 31 |
| short fires (post-cooldown) | 38 |

## Headline performance

| metric | value |
|---|---|
| trades total | 69 |
| longs / shorts | 31 / 38 |
| win rate |  36.2% |
| expectancy per trade | -0.120R |
| avg R per trade | -0.120R |
| avg win | +1.524R |
| avg loss | -1.054R |
| profit factor | 0.82 |
| total R | -8.292R |
| max drawdown | -14.634R |
| longest loss streak | 12 |
| longest win streak | 4 |

## R-multiple distribution

| bucket | count | share |
|---|---|---|
| below -1R (slippage worse than planned) | 33 |  47.8% |
| -1.05R to -0.5R | 9 |  13.0% |
| -0.5R to -0.05R | 2 |   2.9% |
| -0.05R to +0.05R (scratch) | 0 |   0.0% |
| +0.05R to +0.5R | 2 |   2.9% |
| +0.5R to +1.0R | 3 |   4.3% |
| +1.0R to +2.0R | 20 |  29.0% |
| +2.0R to +3.0R | 0 |   0.0% |
| above +3R | 0 |   0.0% |

## Exit reason breakdown

| exit reason | count | share |
|---|---|---|
| stop | 42 |  60.9% |
| target | 14 |  20.3% |
| mtm_session_end | 13 |  18.8% |

## Performance by hour-of-day (UTC)

| hour | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| 8 | 5 |  20.0% | -0.505R | -2.523R | 0.43 |
| 11 | 6 |  16.7% | -0.623R | -3.737R | 0.33 |
| 12 | 5 |  20.0% | -0.481R | -2.403R | 0.44 |
| 13 | 8 |  25.0% | -0.234R | -1.876R | 0.67 |
| 14 | 8 |  62.5% | +0.415R | +3.317R | 2.03 |
| 15 | 14 |  35.7% | -0.232R | -3.243R | 0.64 |
| 16 | 14 |  50.0% | +0.228R | +3.186R | 1.42 |

## Performance by signal score (3 vs 4)

| score | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| 3 | 69 |  36.2% | -0.120R | -8.292R | 0.82 |

## Long vs short

| side | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| long | 31 |  41.9% | -0.013R | -0.415R | 0.98 |
| short | 38 |  31.6% | -0.207R | -7.877R | 0.72 |

## Performance by month

| month | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| 2024-06 | 9 |  33.3% | -0.034R | -0.309R | 0.95 |
| 2024-10 | 8 |  12.5% | -0.774R | -6.195R | 0.19 |
| 2025-01 | 5 |  60.0% | +0.686R | +3.432R | 2.52 |
| 2025-07 | 7 |  57.1% | +0.170R | +1.190R | 1.36 |
| 2025-08 | 5 |  20.0% | -0.658R | -3.291R | 0.26 |

## Coin-flip baseline

If you had taken the same number of trades with random direction (same fixed stop, same fixed target, no costs), what total R would you have ended at?

| metric | value |
|---|---|
| strategy total R | -8.292R |
| coin-flip mean total R | -0.123R |
| coin-flip std total R | 12.14 |
| P(coin flip >= strategy) | 0.724 |

If `P(coin flip >= strategy)` is high (say > 0.20), the observed result is **not distinguishable from random direction with the same R:R**. If it is low (say < 0.05), the strategy is doing something a coin flip on the same trade structure would rarely match.

## Caveats

1. **Spot-FX volume is synthetic.** Polygon's volume for `C:XAUUSD` is contributed-bank tick count, not exchange volume. The CVD-driven D condition relies on this; treat any conclusion about CVD edge with extra scepticism on XAU.
2. **QQQ is a proxy for NQ futures.** Polygon free tier does not include futures. QQQ trades RTH only, so the overnight portion of NQ behaviour is not validated here.
3. **Costs are modelled, not measured.** The half-spread and stop-slippage values are reasonable retail-broker estimates. Real fills on a paper or live account will vary.
4. **No optimisation.** These are the parameters as currently written in `phase4_signals.pine`. If the .pine changes, this report becomes stale.
