# Indicators changelog

## phase4_signals.pine

### 2026-05-21 — min_score raised 3 → 4 on both profiles

**Cause.** Real-data validation (`backtests/reports/pss_validation_*_2026-05-21.md`) showed PSS at `min_score=3` had no measurable edge on either instrument over 2 years of 5m Polygon data:

| Profile | Trades | Win rate | Expectancy | PF | P(coin flip ≥) |
|---|---|---|---|---|---|
| XAU @ score=3 | 508 | 35.0% | -0.07R | 0.90 | 0.876 |
| QQQ @ score=3 | 1165 | 28.3% | -0.08R | 0.89 | 0.962 |

The earlier "+0.44R / 48.1% WR" numbers in the file header came from a synthetic-data optimisation pipeline with look-ahead bugs (causal leak in `argrelextrema`-based divergence detection, whole-day POC/VAH/VAL stamped on every bar of the session, etc.). They did not survive the move to real data + bit-exact Python port + realistic costs. Details in the validation pipeline at `backtests/pss/`.

**At min_score=4:**

| Profile | Trades | Win rate | Expectancy | PF | P(coin flip ≥) |
|---|---|---|---|---|---|
| XAU @ score=4 | **0** | n/a | n/a | n/a | n/a |
| QQQ @ score=4 | 149 | 33.6% | +0.142R | 1.21 | 0.135 |

XAU produces zero score-4 signals because the L long condition (`close near lower1 OR close near vwap`) is automatically true whenever V long (`close <= lower1`) is true — V and L collapse into one effective bit on directional signals. This is a structural flaw in the indicator's L definition, not a tuning problem.

QQQ at score=4 cleared a coin-flip baseline by ~1σ but P=0.135 is not conclusive evidence of edge. 80% of the positive expectancy concentrated in shorts during hour 13 UTC (NY cash open), in a 2024-2026 NDX bull market. Worth tracking on demo before any scaling.

### Pending

- **L-condition redesign.** Define the L score bit independently of V — proximity to a real *prior* level (yesterday's high/low, Asian session range, prior-day POC). Without this, score=4 will continue to be unreachable on XAU and only achievable on QQQ when V, D, and C all align.
- **Indicator update should not happen in isolation from re-validation.** Any rewrite of L gets re-run through `backtests/run_validation.py` before changing the .pine file in production.



### 2026-05-21 (later) — L condition redesigned to prior-day H/L (option 1)

The structural redundancy noted above (V long implying L long automatically) is fixed by replacing the L definition. Now:

```
nearLevelL = abs(close - prevDayLow)  < tol*atr     // long near prior-day support
nearLevelS = abs(close - prevDayHigh) < tol*atr     // short near prior-day resistance
```

`prevDayHigh` / `prevDayLow` come from `request.security(syminfo.tickerid, "D", [high, low], lookahead=barmerge.lookahead_off)` — the most recently CONFIRMED daily H/L, never today's evolving values.

#### Re-validation (real Polygon 5m, 2024-05-21..2026-05-20):

| | XAU/USD | | | | QQQ (NQ proxy, RTH) | | | |
|---|---|---|---|---|---|---|---|---|
| Setting | Trades | Exp/trade | PF | Coin P | Trades | Exp/trade | PF | Coin P |
| Old L, score=3 | 508 | -0.07R | 0.90 | 0.876 | 1165 | -0.08R | 0.89 | 0.962 |
| Old L, score=4 | 0 | n/a | n/a | n/a | 149 | +0.142R | 1.21 | 0.135 |
| **New L, score=3** | 69 | -0.12R | 0.82 | 0.724 | **316** | **+0.096R** | **1.14** | **0.146** |
| **New L, score=4** | 0 | n/a | n/a | n/a | **29** | **+0.430R** | **1.72** | **0.088** |

#### Conclusions:

- **XAU stays unworkable.** The L redesign didn't save it; per-trade expectancy went from -0.07R to -0.12R at score=3, and score=4 still produces 0 signals. Spot XAU does not respect prior-day H/L the way stocks do (24-hour markets, no clear daily open/close anchor). Whatever PSS is detecting, it isn't an edge on this instrument. Keep `xau_minScore = 4` (PSS off for XAU) until the strategy itself is reconsidered.
- **QQQ went from no edge to suggestive edge.** The L-redesign turned both score thresholds from losing into winning systems on real data. Coin-flip P moved from 0.962 (score=3) to 0.146, and from 0.135 to 0.088 (score=4). Neither is below 0.05, so this is "promising, not proven."
- **Score=3 is now the canonical NQ profile setting.** 316 trades is a much larger sample to verify forward than 29; the per-trade edge is smaller but the total cumulative R over 2 years is similar (+30R vs +12R). Override to 4 manually if you prefer the higher-quality subset.
- **Hour 13 UTC (NY cash open) still concentrates the edge.** 75-95% of trades on QQQ come from this single hour across all configs. Effectively a NY-open mean-reversion strategy with extra confluence requirements.
- **Long bias problem dissolved.** Old L: longs +0.026R, shorts +0.195R (asymmetric). New L score=3: longs +0.085R, shorts +0.101R (symmetric). The L redesign removed the structural short bias.

#### Pending

- **Hour filter narrowing.** 13 UTC dominates so heavily that a `hour_start_utc=13, hour_end_utc=13` filter would amount to "only trade NY open". This is data-mined on the validation window and would need a held-out forward test before going into the .pine.
- **Forward-test on demo for at least 90 days.** The L redesign moved QQQ into "looks like an edge" territory. Verify it holds in real time before scaling up.
