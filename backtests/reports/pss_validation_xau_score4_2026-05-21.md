# PSS validation report — XAU/USD

_Generated 2026-05-21 21:00 UTC; data source: Polygon `C:XAUUSD`._

## What this report is

PSS Phase-4 logic, ported bit-exactly from `indicators/pine-script/phase4_signals.pine`, run on real 5-minute Polygon data with the parameters as currently written in the .pine file. **No optimisation. No tuning.** The only question being answered: does the strategy as written show a measurable edge on this data?

_Notes: Spot gold via Polygon forex. Volume is contributed-bank tick count, not exchange volume.

DIAGNOSTIC OVERRIDE: min_score forced to 4 (.pine value is 3). All other params unchanged._

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
| min_score | 4 |
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
| long candidates (pre-cooldown) | 0 |
| short candidates (pre-cooldown) | 0 |
| long fires (post-cooldown) | 0 |
| short fires (post-cooldown) | 0 |

## Headline performance

| metric | value |
|---|---|
| trades total | 0 |
| longs / shorts | 0 / 0 |
| win rate |   0.0% |
| expectancy per trade | +0.000R |
| avg R per trade | +0.000R |
| avg win | +0.000R |
| avg loss | +0.000R |
| profit factor | 0.00 |
| total R | +0.000R |
| max drawdown | +0.000R |
| longest loss streak | 0 |
| longest win streak | 0 |

## R-multiple distribution

_(no trades)_

## Exit reason breakdown

_(no trades)_

## Performance by hour-of-day (UTC)

_(no segments with enough trades)_

## Performance by signal score (3 vs 4)

_(no segments with enough trades)_

## Long vs short

_(no segments with enough trades)_

## Performance by month

_(no segments with enough trades)_

## Coin-flip baseline

If you had taken the same number of trades with random direction (same fixed stop, same fixed target, no costs), what total R would you have ended at?

| metric | value |
|---|---|
| strategy total R | +0.000R |
| coin-flip mean total R | +0.000R |
| coin-flip std total R | 0.00 |
| P(coin flip >= strategy) | 1.000 |

If `P(coin flip >= strategy)` is high (say > 0.20), the observed result is **not distinguishable from random direction with the same R:R**. If it is low (say < 0.05), the strategy is doing something a coin flip on the same trade structure would rarely match.

## Caveats

1. **Spot-FX volume is synthetic.** Polygon's volume for `C:XAUUSD` is contributed-bank tick count, not exchange volume. The CVD-driven D condition relies on this; treat any conclusion about CVD edge with extra scepticism on XAU.
2. **QQQ is a proxy for NQ futures.** Polygon free tier does not include futures. QQQ trades RTH only, so the overnight portion of NQ behaviour is not validated here.
3. **Costs are modelled, not measured.** The half-spread and stop-slippage values are reasonable retail-broker estimates. Real fills on a paper or live account will vary.
4. **No optimisation.** These are the parameters as currently written in `phase4_signals.pine`. If the .pine changes, this report becomes stale.
