# PSS validation report — QQQ (NQ proxy, RTH only)

_Generated 2026-05-21 21:10 UTC; data source: Polygon `QQQ`._

## What this report is

PSS Phase-4 logic, ported bit-exactly from `indicators/pine-script/phase4_signals.pine`, run on real 5-minute Polygon data with the parameters as currently written in the .pine file. **No optimisation. No tuning.** The only question being answered: does the strategy as written show a measurable edge on this data?

_Notes: QQQ stands in for NQ futures because Polygon free tier does not include futures. RTH only (13:30-20:00 UTC). Overnight NQ behaviour is NOT validated._

## Parameters used

| param | value |
|---|---|
| sd_mult | 1.25 |
| atr_period | 14 |
| stop_mult | 1.25 |
| rr_ratio | 2.5 |
| cooldown | 8 |
| level_tol | 0.25 |
| compress_pct | 0.85 |
| min_score | 4 |
| hour_filter | True |
| hour_start_utc | 13 |
| hour_end_utc | 21 |
| half_spread (cost model) | 0.005 |
| stop_slippage (cost model) | 0.01 |

## Data window

| field | value |
|---|---|
| instrument | QQQ (NQ proxy, RTH only) |
| polygon ticker | QQQ |
| bars (5m) | 39413 |
| first bar | 2024-05-21T13:30:00+00:00 |
| last bar | 2026-05-20T20:00:00+00:00 |

## Signal frequency

| counter | value |
|---|---|
| long candidates (pre-cooldown) | 10 |
| short candidates (pre-cooldown) | 21 |
| long fires (post-cooldown) | 8 |
| short fires (post-cooldown) | 21 |

## Headline performance

| metric | value |
|---|---|
| trades total | 29 |
| longs / shorts | 8 / 21 |
| win rate |  41.4% |
| expectancy per trade | +0.430R |
| avg R per trade | +0.430R |
| avg win | +2.488R |
| avg loss | -1.022R |
| profit factor | 1.72 |
| total R | +12.476R |
| max drawdown | -3.657R |
| longest loss streak | 3 |
| longest win streak | 4 |

## R-multiple distribution

| bucket | count | share |
|---|---|---|
| below -1R (slippage worse than planned) | 0 |   0.0% |
| -1.05R to -0.5R | 17 |  58.6% |
| -0.5R to -0.05R | 0 |   0.0% |
| -0.05R to +0.05R (scratch) | 0 |   0.0% |
| +0.05R to +0.5R | 0 |   0.0% |
| +0.5R to +1.0R | 0 |   0.0% |
| +1.0R to +2.0R | 0 |   0.0% |
| +2.0R to +3.0R | 12 |  41.4% |
| above +3R | 0 |   0.0% |

## Exit reason breakdown

| exit reason | count | share |
|---|---|---|
| stop | 17 |  58.6% |
| target | 12 |  41.4% |

## Performance by hour-of-day (UTC)

| hour | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| 13 | 28 |  42.9% | +0.482R | +13.503R | 1.83 |

## Performance by signal score (3 vs 4)

| score | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| 4 | 29 |  41.4% | +0.430R | +12.476R | 1.72 |

## Long vs short

| side | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| long | 8 |  25.0% | -0.140R | -1.121R | 0.82 |
| short | 21 |  47.6% | +0.648R | +13.598R | 2.21 |

## Performance by month

| month | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| 2025-06 | 5 |  80.0% | +1.786R | +8.929R | 9.70 |

## Coin-flip baseline

If you had taken the same number of trades with random direction (same fixed stop, same fixed target, no costs), what total R would you have ended at?

| metric | value |
|---|---|
| strategy total R | +12.476R |
| coin-flip mean total R | +0.060R |
| coin-flip std total R | 8.30 |
| P(coin flip >= strategy) | 0.088 |

If `P(coin flip >= strategy)` is high (say > 0.20), the observed result is **not distinguishable from random direction with the same R:R**. If it is low (say < 0.05), the strategy is doing something a coin flip on the same trade structure would rarely match.

## Caveats

1. **Spot-FX volume is synthetic.** Polygon's volume for `C:XAUUSD` is contributed-bank tick count, not exchange volume. The CVD-driven D condition relies on this; treat any conclusion about CVD edge with extra scepticism on XAU.
2. **QQQ is a proxy for NQ futures.** Polygon free tier does not include futures. QQQ trades RTH only, so the overnight portion of NQ behaviour is not validated here.
3. **Costs are modelled, not measured.** The half-spread and stop-slippage values are reasonable retail-broker estimates. Real fills on a paper or live account will vary.
4. **No optimisation.** These are the parameters as currently written in `phase4_signals.pine`. If the .pine changes, this report becomes stale.
