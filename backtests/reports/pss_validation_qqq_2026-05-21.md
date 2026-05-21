# PSS validation report — QQQ (NQ proxy, RTH only)

_Generated 2026-05-21 20:45 UTC; data source: Polygon `QQQ`._

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
| long candidates (pre-cooldown) | 1102 |
| short candidates (pre-cooldown) | 1446 |
| long fires (post-cooldown) | 533 |
| short fires (post-cooldown) | 682 |

## Headline performance

| metric | value |
|---|---|
| trades total | 1165 |
| longs / shorts | 533 / 632 |
| win rate |  28.3% |
| expectancy per trade | -0.080R |
| avg R per trade | -0.079R |
| avg win | +2.253R |
| avg loss | -1.002R |
| profit factor | 0.89 |
| total R | -92.286R |
| max drawdown | -113.697R |
| longest loss streak | 18 |
| longest win streak | 4 |

## R-multiple distribution

| bucket | count | share |
|---|---|---|
| below -1R (slippage worse than planned) | 13 |   1.1% |
| -1.05R to -0.5R | 805 |  69.1% |
| -0.5R to -0.05R | 8 |   0.7% |
| -0.05R to +0.05R (scratch) | 11 |   0.9% |
| +0.05R to +0.5R | 12 |   1.0% |
| +0.5R to +1.0R | 11 |   0.9% |
| +1.0R to +2.0R | 24 |   2.1% |
| +2.0R to +3.0R | 281 |  24.1% |
| above +3R | 0 |   0.0% |

## Exit reason breakdown

| exit reason | count | share |
|---|---|---|
| stop | 811 |  69.6% |
| target | 280 |  24.0% |
| mtm_session_end | 74 |   6.4% |

## Performance by hour-of-day (UTC)

| hour | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| 13 | 639 |  28.8% | -0.031R | -19.761R | 0.96 |
| 14 | 159 |  28.3% | -0.058R | -9.244R | 0.92 |
| 15 | 78 |  20.5% | -0.399R | -31.088R | 0.50 |
| 16 | 93 |  29.0% | -0.062R | -5.796R | 0.91 |
| 17 | 72 |  22.2% | -0.419R | -30.191R | 0.47 |
| 18 | 64 |  34.4% | -0.033R | -2.090R | 0.95 |
| 19 | 55 |  36.4% | +0.094R | +5.929R | 1.23 |
| 20 | 5 |   0.0% | -0.009R | -0.045R | 0.00 |

## Performance by signal score (3 vs 4)

| score | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| 3 | 1090 |  27.9% | -0.097R | -104.770R | 0.87 |
| 4 | 75 |  34.7% | +0.166R | +12.484R | 1.25 |

## Long vs short

| side | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| long | 533 |  28.5% | -0.084R | -43.793R | 0.88 |
| short | 632 |  28.2% | -0.077R | -48.493R | 0.89 |

## Performance by month

| month | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| 2024-05 | 13 |  46.2% | +0.591R | +7.680R | 2.06 |
| 2024-06 | 40 |  22.5% | -0.185R | -7.407R | 0.75 |
| 2024-07 | 48 |  27.1% | -0.126R | -6.072R | 0.83 |
| 2024-08 | 42 |  28.6% | -0.015R | -0.611R | 0.98 |
| 2024-09 | 37 |  37.8% | +0.218R | +8.073R | 1.34 |
| 2024-10 | 47 |  36.2% | +0.109R | +5.106R | 1.17 |
| 2024-11 | 45 |  22.2% | -0.398R | -17.895R | 0.50 |
| 2024-12 | 57 |  33.3% | +0.104R | +5.934R | 1.15 |
| 2025-01 | 64 |  28.1% | -0.110R | -7.009R | 0.85 |
| 2025-02 | 49 |  22.4% | -0.304R | -14.882R | 0.61 |
| 2025-03 | 48 |  31.2% | +0.078R | +3.730R | 1.11 |
| 2025-04 | 47 |  27.7% | -0.083R | -3.885R | 0.88 |
| 2025-05 | 41 |  24.4% | -0.206R | -8.440R | 0.73 |
| 2025-06 | 48 |  33.3% | +0.012R | +0.569R | 1.02 |
| 2025-07 | 43 |  30.2% | +0.033R | +2.434R | 1.08 |
| 2025-08 | 47 |  31.9% | -0.026R | -1.226R | 0.96 |
| 2025-09 | 52 |  28.8% | -0.110R | -5.734R | 0.85 |
| 2025-10 | 55 |  25.5% | -0.203R | -11.161R | 0.73 |
| 2025-11 | 59 |  18.6% | -0.374R | -22.057R | 0.53 |
| 2025-12 | 60 |  28.3% | -0.002R | -0.117R | 1.00 |
| 2026-01 | 56 |  37.5% | +0.237R | +13.274R | 1.38 |
| 2026-02 | 48 |  25.0% | -0.160R | -7.688R | 0.78 |
| 2026-03 | 47 |  31.9% | -0.016R | -0.751R | 0.98 |
| 2026-04 | 41 |  14.6% | -0.505R | -20.692R | 0.42 |
| 2026-05 | 31 |  25.8% | -0.112R | -3.459R | 0.85 |

## Coin-flip baseline

If you had taken the same number of trades with random direction (same fixed stop, same fixed target, no costs), what total R would you have ended at?

| metric | value |
|---|---|
| strategy total R | -92.286R |
| coin-flip mean total R | -0.494R |
| coin-flip std total R | 51.39 |
| P(coin flip >= strategy) | 0.962 |

If `P(coin flip >= strategy)` is high (say > 0.20), the observed result is **not distinguishable from random direction with the same R:R**. If it is low (say < 0.05), the strategy is doing something a coin flip on the same trade structure would rarely match.

## Caveats

1. **Spot-FX volume is synthetic.** Polygon's volume for `C:XAUUSD` is contributed-bank tick count, not exchange volume. The CVD-driven D condition relies on this; treat any conclusion about CVD edge with extra scepticism on XAU.
2. **QQQ is a proxy for NQ futures.** Polygon free tier does not include futures. QQQ trades RTH only, so the overnight portion of NQ behaviour is not validated here.
3. **Costs are modelled, not measured.** The half-spread and stop-slippage values are reasonable retail-broker estimates. Real fills on a paper or live account will vary.
4. **No optimisation.** These are the parameters as currently written in `phase4_signals.pine`. If the .pine changes, this report becomes stale.
