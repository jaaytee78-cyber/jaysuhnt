# PSS validation report — QQQ (NQ proxy, RTH only)

_Generated 2026-05-21 21:10 UTC; data source: Polygon `QQQ`._

## What this report is

PSS Phase-4 logic, ported bit-exactly from `indicators/pine-script/phase4_signals.pine`, run on real 5-minute Polygon data with the parameters as currently written in the .pine file. **No optimisation. No tuning.** The only question being answered: does the strategy as written show a measurable edge on this data?

_Notes: QQQ stands in for NQ futures because Polygon free tier does not include futures. RTH only (13:30-20:00 UTC). Overnight NQ behaviour is NOT validated.

DIAGNOSTIC OVERRIDE: min_score forced to 3 (.pine value is 4). All other params unchanged._

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
| min_score | 3 |
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
| long candidates (pre-cooldown) | 187 |
| short candidates (pre-cooldown) | 440 |
| long fires (post-cooldown) | 98 |
| short fires (post-cooldown) | 218 |

## Headline performance

| metric | value |
|---|---|
| trades total | 316 |
| longs / shorts | 98 / 218 |
| win rate |  32.9% |
| expectancy per trade | +0.096R |
| avg R per trade | +0.096R |
| avg win | +2.362R |
| avg loss | -1.015R |
| profit factor | 1.14 |
| total R | +30.443R |
| max drawdown | -28.409R |
| longest loss streak | 16 |
| longest win streak | 5 |

## R-multiple distribution

| bucket | count | share |
|---|---|---|
| below -1R (slippage worse than planned) | 3 |   0.9% |
| -1.05R to -0.5R | 208 |  65.8% |
| -0.5R to -0.05R | 0 |   0.0% |
| -0.05R to +0.05R (scratch) | 1 |   0.3% |
| +0.05R to +0.5R | 2 |   0.6% |
| +0.5R to +1.0R | 3 |   0.9% |
| +1.0R to +2.0R | 3 |   0.9% |
| +2.0R to +3.0R | 96 |  30.4% |
| above +3R | 0 |   0.0% |

## Exit reason breakdown

| exit reason | count | share |
|---|---|---|
| stop | 209 |  66.1% |
| target | 96 |  30.4% |
| mtm_session_end | 11 |   3.5% |

## Performance by hour-of-day (UTC)

| hour | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| 13 | 236 |  33.9% | +0.151R | +35.688R | 1.22 |
| 14 | 46 |  30.4% | +0.046R | +2.106R | 1.06 |
| 15 | 9 |  33.3% | +0.148R | +1.332R | 1.22 |
| 16 | 5 |   0.0% | -1.028R | -5.139R | 0.00 |
| 17 | 7 |   0.0% | -1.009R | -7.060R | 0.00 |
| 18 | 6 |  50.0% | -0.011R | -0.067R | 0.98 |
| 19 | 6 |  66.7% | +0.602R | +3.612R | 3.19 |

## Performance by signal score (3 vs 4)

| score | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| 3 | 293 |  31.7% | +0.052R | +15.339R | 1.08 |
| 4 | 23 |  47.8% | +0.657R | +15.104R | 2.23 |

## Long vs short

| side | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| long | 98 |  33.7% | +0.085R | +8.372R | 1.13 |
| short | 218 |  32.6% | +0.101R | +22.072R | 1.15 |

## Performance by month

| month | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| 2024-06 | 18 |  33.3% | +0.145R | +2.606R | 1.21 |
| 2024-07 | 15 |  33.3% | +0.149R | +2.230R | 1.22 |
| 2024-08 | 15 |  40.0% | +0.385R | +5.780R | 1.63 |
| 2024-09 | 10 |  30.0% | -0.383R | -3.830R | 0.46 |
| 2024-10 | 11 |  18.2% | -0.530R | -5.827R | 0.37 |
| 2024-11 | 13 |   0.0% | -1.027R | -13.356R | 0.00 |
| 2024-12 | 15 |  20.0% | -0.254R | -3.809R | 0.66 |
| 2025-01 | 13 |  46.2% | +0.597R | +7.763R | 2.08 |
| 2025-02 | 13 |  46.2% | +0.596R | +7.749R | 2.08 |
| 2025-03 | 14 |  21.4% | -0.233R | -3.260R | 0.70 |
| 2025-04 | 8 |  25.0% | -0.133R | -1.067R | 0.82 |
| 2025-05 | 9 |  55.6% | +0.933R | +8.393R | 3.07 |
| 2025-06 | 16 |  43.8% | +0.384R | +6.140R | 1.67 |
| 2025-07 | 13 |  23.1% | -0.221R | -2.869R | 0.72 |
| 2025-08 | 13 |  38.5% | +0.327R | +4.246R | 1.52 |
| 2025-09 | 14 |  28.6% | -0.195R | -2.724R | 0.73 |
| 2025-10 | 8 |  37.5% | +0.295R | +2.361R | 1.46 |
| 2025-11 | 15 |  33.3% | +0.154R | +2.304R | 1.23 |
| 2025-12 | 17 |  35.3% | +0.210R | +3.571R | 1.32 |
| 2026-01 | 13 |  61.5% | +1.138R | +14.791R | 3.89 |
| 2026-02 | 13 |  38.5% | +0.330R | +4.291R | 1.53 |
| 2026-03 | 14 |  42.9% | +0.281R | +3.937R | 1.49 |
| 2026-04 | 14 |  14.3% | -0.517R | -7.236R | 0.41 |
| 2026-05 | 8 |  12.5% | -0.579R | -4.635R | 0.35 |

## Coin-flip baseline

If you had taken the same number of trades with random direction (same fixed stop, same fixed target, no costs), what total R would you have ended at?

| metric | value |
|---|---|
| strategy total R | +30.443R |
| coin-flip mean total R | +0.305R |
| coin-flip std total R | 28.10 |
| P(coin flip >= strategy) | 0.146 |

If `P(coin flip >= strategy)` is high (say > 0.20), the observed result is **not distinguishable from random direction with the same R:R**. If it is low (say < 0.05), the strategy is doing something a coin flip on the same trade structure would rarely match.

## Caveats

1. **Spot-FX volume is synthetic.** Polygon's volume for `C:XAUUSD` is contributed-bank tick count, not exchange volume. The CVD-driven D condition relies on this; treat any conclusion about CVD edge with extra scepticism on XAU.
2. **QQQ is a proxy for NQ futures.** Polygon free tier does not include futures. QQQ trades RTH only, so the overnight portion of NQ behaviour is not validated here.
3. **Costs are modelled, not measured.** The half-spread and stop-slippage values are reasonable retail-broker estimates. Real fills on a paper or live account will vary.
4. **No optimisation.** These are the parameters as currently written in `phase4_signals.pine`. If the .pine changes, this report becomes stale.
