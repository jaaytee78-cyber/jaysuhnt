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
