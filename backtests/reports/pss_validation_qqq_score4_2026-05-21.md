# PSS validation report — QQQ (NQ proxy, RTH only)

_Generated 2026-05-21 21:00 UTC; data source: Polygon `QQQ`._

## What this report is

PSS Phase-4 logic, ported bit-exactly from `indicators/pine-script/phase4_signals.pine`, run on real 5-minute Polygon data with the parameters as currently written in the .pine file. **No optimisation. No tuning.** The only question being answered: does the strategy as written show a measurable edge on this data?

_Notes: QQQ stands in for NQ futures because Polygon free tier does not include futures. RTH only (13:30-20:00 UTC). Overnight NQ behaviour is NOT validated.

DIAGNOSTIC OVERRIDE: min_score forced to 4 (.pine value is 3). All other params unchanged._

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
| long candidates (pre-cooldown) | 73 |
| short candidates (pre-cooldown) | 167 |
| long fires (post-cooldown) | 47 |
| short fires (post-cooldown) | 102 |

## Headline performance

| metric | value |
|---|---|
| trades total | 149 |
| longs / shorts | 47 / 102 |
| win rate |  33.6% |
| expectancy per trade | +0.142R |
| avg R per trade | +0.142R |
| avg win | +2.446R |
| avg loss | -1.022R |
| profit factor | 1.21 |
| total R | +21.142R |
| max drawdown | -18.353R |
| longest loss streak | 17 |
| longest win streak | 5 |

## R-multiple distribution

| bucket | count | share |
|---|---|---|
| below -1R (slippage worse than planned) | 3 |   2.0% |
| -1.05R to -0.5R | 96 |  64.4% |
| -0.5R to -0.05R | 0 |   0.0% |
| -0.05R to +0.05R (scratch) | 0 |   0.0% |
| +0.05R to +0.5R | 1 |   0.7% |
| +0.5R to +1.0R | 0 |   0.0% |
| +1.0R to +2.0R | 0 |   0.0% |
| +2.0R to +3.0R | 49 |  32.9% |
| above +3R | 0 |   0.0% |

## Exit reason breakdown

| exit reason | count | share |
|---|---|---|
| stop | 99 |  66.4% |
| target | 49 |  32.9% |
| mtm_session_end | 1 |   0.7% |

## Performance by hour-of-day (UTC)

| hour | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| 13 | 127 |  35.4% | +0.206R | +26.116R | 1.31 |
| 14 | 22 |  22.7% | -0.226R | -4.974R | 0.71 |

## Performance by signal score (3 vs 4)

| score | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| 4 | 149 |  33.6% | +0.142R | +21.142R | 1.21 |

## Long vs short

| side | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| long | 47 |  29.8% | +0.026R | +1.240R | 1.04 |
| short | 102 |  35.3% | +0.195R | +19.901R | 1.29 |

## Performance by month

| month | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| 2024-06 | 7 |  42.9% | +0.483R | +3.381R | 1.83 |
| 2024-07 | 6 |  16.7% | -0.437R | -2.621R | 0.49 |
| 2024-08 | 5 |  60.0% | +1.090R | +5.451R | 3.69 |
| 2024-09 | 5 |   0.0% | -1.020R | -5.101R | 0.00 |
| 2024-10 | 5 |   0.0% | -1.024R | -5.119R | 0.00 |
| 2024-11 | 6 |   0.0% | -1.028R | -6.170R | 0.00 |
| 2024-12 | 11 |  27.3% | -0.072R | -0.791R | 0.90 |
| 2025-01 | 5 |  40.0% | +0.382R | +1.910R | 1.62 |
| 2025-02 | 12 |  50.0% | +0.730R | +8.765R | 2.42 |
| 2025-03 | 5 |  60.0% | +1.092R | +5.458R | 3.70 |
| 2025-06 | 7 |  42.9% | +0.183R | +1.284R | 1.31 |
| 2025-09 | 5 |   0.0% | -1.021R | -5.105R | 0.00 |
| 2025-11 | 11 |  45.5% | +0.579R | +6.365R | 2.04 |
| 2025-12 | 11 |  54.5% | +0.885R | +9.734R | 2.88 |
| 2026-01 | 10 |  60.0% | +1.085R | +10.846R | 3.65 |
| 2026-02 | 8 |  50.0% | +0.733R | +5.861R | 2.43 |
| 2026-03 | 5 |  40.0% | +0.388R | +1.942R | 1.64 |
| 2026-04 | 7 |  14.3% | -0.518R | -3.623R | 0.41 |
| 2026-05 | 5 |   0.0% | -1.016R | -5.082R | 0.00 |

## Coin-flip baseline

If you had taken the same number of trades with random direction (same fixed stop, same fixed target, no costs), what total R would you have ended at?

| metric | value |
|---|---|
| strategy total R | +21.142R |
| coin-flip mean total R | +0.236R |
| coin-flip std total R | 19.18 |
| P(coin flip >= strategy) | 0.135 |

If `P(coin flip >= strategy)` is high (say > 0.20), the observed result is **not distinguishable from random direction with the same R:R**. If it is low (say < 0.05), the strategy is doing something a coin flip on the same trade structure would rarely match.

## Caveats

1. **Spot-FX volume is synthetic.** Polygon's volume for `C:XAUUSD` is contributed-bank tick count, not exchange volume. The CVD-driven D condition relies on this; treat any conclusion about CVD edge with extra scepticism on XAU.
2. **QQQ is a proxy for NQ futures.** Polygon free tier does not include futures. QQQ trades RTH only, so the overnight portion of NQ behaviour is not validated here.
3. **Costs are modelled, not measured.** The half-spread and stop-slippage values are reasonable retail-broker estimates. Real fills on a paper or live account will vary.
4. **No optimisation.** These are the parameters as currently written in `phase4_signals.pine`. If the .pine changes, this report becomes stale.
