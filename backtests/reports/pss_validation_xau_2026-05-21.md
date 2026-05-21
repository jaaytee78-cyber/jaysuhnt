# PSS validation report — XAU/USD

_Generated 2026-05-21 20:43 UTC; data source: Polygon `C:XAUUSD`._

## What this report is

PSS Phase-4 logic, ported bit-exactly from `indicators/pine-script/phase4_signals.pine`, run on real 5-minute Polygon data with the parameters as currently written in the .pine file. **No optimisation. No tuning.** The only question being answered: does the strategy as written show a measurable edge on this data?

_Notes: Spot gold via Polygon forex. Volume is contributed-bank tick count, not exchange volume._

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
| long candidates (pre-cooldown) | 305 |
| short candidates (pre-cooldown) | 327 |
| long fires (post-cooldown) | 239 |
| short fires (post-cooldown) | 270 |

## Headline performance

| metric | value |
|---|---|
| trades total | 508 |
| longs / shorts | 239 / 269 |
| win rate |  35.0% |
| expectancy per trade | -0.070R |
| avg R per trade | -0.070R |
| avg win | +1.775R |
| avg loss | -1.066R |
| profit factor | 0.90 |
| total R | -35.795R |
| max drawdown | -37.693R |
| longest loss streak | 13 |
| longest win streak | 6 |

## R-multiple distribution

| bucket | count | share |
|---|---|---|
| below -1R (slippage worse than planned) | 230 |  45.3% |
| -1.05R to -0.5R | 93 |  18.3% |
| -0.5R to -0.05R | 5 |   1.0% |
| -0.05R to +0.05R (scratch) | 3 |   0.6% |
| +0.05R to +0.5R | 5 |   1.0% |
| +0.5R to +1.0R | 8 |   1.6% |
| +1.0R to +2.0R | 164 |  32.3% |
| +2.0R to +3.0R | 0 |   0.0% |
| above +3R | 0 |   0.0% |

## Exit reason breakdown

| exit reason | count | share |
|---|---|---|
| stop | 316 |  62.2% |
| target | 153 |  30.1% |
| mtm_session_end | 39 |   7.7% |

## Performance by hour-of-day (UTC)

| hour | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| 7 | 64 |  37.5% | +0.021R | +1.328R | 1.03 |
| 8 | 38 |  26.3% | -0.300R | -11.411R | 0.63 |
| 9 | 57 |  38.6% | +0.062R | +3.540R | 1.09 |
| 10 | 44 |  31.8% | -0.151R | -6.626R | 0.80 |
| 11 | 34 |  47.1% | +0.292R | +9.942R | 1.49 |
| 12 | 50 |  32.0% | -0.112R | -5.604R | 0.85 |
| 13 | 52 |  30.8% | -0.143R | -7.442R | 0.81 |
| 14 | 66 |  40.9% | +0.055R | +3.661R | 1.09 |
| 15 | 49 |  28.6% | -0.258R | -12.662R | 0.63 |
| 16 | 54 |  35.2% | -0.195R | -10.520R | 0.69 |

## Performance by signal score (3 vs 4)

| score | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| 3 | 508 |  35.0% | -0.070R | -35.795R | 0.90 |

## Long vs short

| side | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| long | 239 |  34.3% | -0.109R | -26.139R | 0.84 |
| short | 269 |  35.7% | -0.036R | -9.656R | 0.95 |

## Performance by month

| month | n | win% | expectancy | total R | PF |
|---|---|---|---|---|---|
| 2024-05 | 9 |   0.0% | -0.937R | -8.434R | 0.00 |
| 2024-06 | 19 |  31.6% | -0.214R | -4.060R | 0.72 |
| 2024-07 | 21 |  52.4% | +0.440R | +9.241R | 1.81 |
| 2024-08 | 22 |  18.2% | -0.594R | -13.076R | 0.34 |
| 2024-09 | 19 |  57.9% | +0.484R | +9.190R | 2.00 |
| 2024-10 | 25 |  20.0% | -0.491R | -12.281R | 0.44 |
| 2024-11 | 19 |  31.6% | -0.157R | -2.979R | 0.79 |
| 2024-12 | 27 |  29.6% | -0.379R | -10.241R | 0.53 |
| 2025-01 | 29 |  44.8% | +0.208R | +6.034R | 1.33 |
| 2025-02 | 16 |  37.5% | +0.080R | +1.273R | 1.13 |
| 2025-03 | 23 |  60.9% | +0.616R | +14.179R | 2.41 |
| 2025-04 | 20 |  35.0% | -0.087R | -1.746R | 0.87 |
| 2025-05 | 11 |  36.4% | -0.099R | -1.092R | 0.85 |
| 2025-06 | 25 |  40.0% | +0.028R | +0.710R | 1.05 |
| 2025-07 | 30 |  33.3% | -0.124R | -3.719R | 0.82 |
| 2025-08 | 23 |  34.8% | -0.065R | -1.505R | 0.91 |
| 2025-09 | 16 |  50.0% | +0.431R | +6.899R | 1.80 |
| 2025-10 | 21 |  28.6% | -0.246R | -5.161R | 0.67 |
| 2025-11 | 23 |  30.4% | -0.133R | -3.064R | 0.82 |
| 2025-12 | 27 |  40.7% | +0.098R | +2.635R | 1.17 |
| 2026-01 | 15 |  33.3% | -0.038R | -0.571R | 0.94 |
| 2026-02 | 18 |  33.3% | -0.088R | -1.584R | 0.87 |
| 2026-03 | 19 |  21.1% | -0.480R | -9.124R | 0.41 |
| 2026-04 | 17 |  23.5% | -0.268R | -4.554R | 0.63 |
| 2026-05 | 14 |  28.6% | -0.198R | -2.766R | 0.73 |

## Coin-flip baseline

If you had taken the same number of trades with random direction (same fixed stop, same fixed target, no costs), what total R would you have ended at?

| metric | value |
|---|---|
| strategy total R | -35.795R |
| coin-flip mean total R | +0.989R |
| coin-flip std total R | 30.92 |
| P(coin flip >= strategy) | 0.876 |

If `P(coin flip >= strategy)` is high (say > 0.20), the observed result is **not distinguishable from random direction with the same R:R**. If it is low (say < 0.05), the strategy is doing something a coin flip on the same trade structure would rarely match.

## Caveats

1. **Spot-FX volume is synthetic.** Polygon's volume for `C:XAUUSD` is contributed-bank tick count, not exchange volume. The CVD-driven D condition relies on this; treat any conclusion about CVD edge with extra scepticism on XAU.
2. **QQQ is a proxy for NQ futures.** Polygon free tier does not include futures. QQQ trades RTH only, so the overnight portion of NQ behaviour is not validated here.
3. **Costs are modelled, not measured.** The half-spread and stop-slippage values are reasonable retail-broker estimates. Real fills on a paper or live account will vary.
4. **No optimisation.** These are the parameters as currently written in `phase4_signals.pine`. If the .pine changes, this report becomes stale.
