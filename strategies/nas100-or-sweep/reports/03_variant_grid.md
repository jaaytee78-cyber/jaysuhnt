# Variant Grid - Stop/Target/Entry ablations + costs + bootstrap CIs

Data: QQQ 1m, 439,877 bars, 2024-05-22 -> 2026-05-21
Bootstrap iterations: **5,000**, 95% CI percentile method.
Slippage applied (net columns): **$0.01/share each side** ($0.02/share round-trip).

**Reading guide:**
- `Exp R (95% CI)`: bootstrap mean R with lower/upper bounds.
- `Sig?`: "yes" if the 95% CI does not include 0 - i.e. we can reject "no edge" at 5%.
- `Avg Win` / `Avg Loss` are mean R-multiples within winners/losers.
- `Risk $` is the median dollar risk per share at entry - tells you how much slippage actually eats into the edge.

## Variants

- **v1_baseline** - Strict ICT: sweep close entry, 1c-tight stop, opposite OR target.
    entry=sweep_close, stop=wick_tight, target=opposite_or, buffer=$0.01
- **v2_buffer_5c** - Wider 5c stop above wick, opposite OR target.
    entry=sweep_close, stop=wick_buffer, target=opposite_or, buffer=$0.05
- **v3_fixed_1R** - Tight stop, target capped at 1R.
    entry=sweep_close, stop=wick_tight, target=fixed_R (1.0R), buffer=$0.01
- **v4_buffer_2R** - 5c-buffer stop, target 2R.
    entry=sweep_close, stop=wick_buffer, target=fixed_R (2.0R), buffer=$0.05
- **v5_pct_or_30_2R** - Stop = 30% of OR (volatility-scaled), target 2R.
    entry=sweep_close, stop=pct_or, target=fixed_R (2.0R), pct_or=30%
- **v6_confirm_or** - Confirmation entry, tight stop, opposite OR target.
    entry=confirm_close, stop=wick_tight, target=opposite_or, buffer=$0.01
- **v7_buffer_confirm_2R** - Confirmation entry, 5c stop, target 2R.
    entry=confirm_close, stop=wick_buffer, target=fixed_R (2.0R), buffer=$0.05
- **v8_pct_or_30_confirm_2R** - Confirmation entry, 30%-OR stop, target 2R.
    entry=confirm_close, stop=pct_or, target=fixed_R (2.0R), pct_or=30%

## Gross results (no costs)

| Variant | N | Win % | P(tgt) | P(stop) | Exp R (95% CI) | Sig? | Avg Win | Avg Loss | Median R | Risk $ |
|---|---|---|---|---|---|---|---|---|---|---|
| **v1_baseline** | 453 | 19.4% (15.9-23.4) | 16.8% | 80.1% | +0.132 (-0.129, +0.413) | no | +4.81R | -1.00R | -1.00R | $0.39 |
| **v2_buffer_5c** | 453 | 20.8% (17.2-24.5) | 18.1% | 78.8% | +0.160 (-0.089, +0.434) | no | +4.57R | -1.00R | -1.00R | $0.43 |
| **v3_fixed_1R** | 453 | 42.8% (38.2-47.5) | 42.8% | 57.0% | -0.142 (-0.235, -0.053) | yes | +1.00R | -1.00R | -1.00R | $0.39 |
| **v4_buffer_2R** | 453 | 33.6% (29.4-38.0) | 33.1% | 66.0% | +0.006 (-0.127, +0.139) | no | +1.99R | -1.00R | -1.00R | $0.43 |
| **v5_pct_or_30_2R** | 453 | 34.0% (29.8-38.4) | 31.8% | 63.8% | +0.006 (-0.119, +0.136) | no | +1.92R | -0.98R | -1.00R | $0.68 |
| **v6_confirm_or** | 413 | 29.1% (24.9-33.7) | 24.0% | 69.2% | -0.046 (-0.205, +0.124) | no | +2.25R | -0.99R | -1.00R | $0.63 |
| **v7_buffer_confirm_2R** | 413 | 35.8% (31.2-40.4) | 30.8% | 62.7% | +0.020 (-0.108, +0.151) | no | +1.82R | -0.99R | -1.00R | $0.67 |
| **v8_pct_or_30_confirm_2R** | 413 | 33.9% (29.3-38.5) | 30.5% | 63.9% | -0.018 (-0.149, +0.116) | no | +1.86R | -0.98R | -1.00R | $0.68 |

## Net results (slippage $0.01/share each side)

| Variant | N | Win % | P(tgt) | P(stop) | Exp R (95% CI) | Sig? | Avg Win | Avg Loss | Median R | Risk $ |
|---|---|---|---|---|---|---|---|---|---|---|
| **v1_baseline** | 453 | 19.4% (15.9-23.4) | 16.8% | 80.1% | +0.058 (-0.201, +0.338) | no | +4.75R | -1.08R | -1.04R | $0.39 |
| **v2_buffer_5c** | 453 | 20.8% (17.2-24.5) | 18.1% | 78.8% | +0.100 (-0.150, +0.374) | no | +4.52R | -1.06R | -1.04R | $0.43 |
| **v3_fixed_1R** | 453 | 42.8% (38.2-47.5) | 42.8% | 57.0% | -0.216 (-0.307, -0.126) | yes | +0.93R | -1.08R | -1.03R | $0.39 |
| **v4_buffer_2R** | 453 | 33.6% (29.4-38.0) | 33.1% | 66.0% | -0.054 (-0.185, +0.079) | no | +1.93R | -1.06R | -1.03R | $0.43 |
| **v5_pct_or_30_2R** | 453 | 34.0% (29.8-38.4) | 31.8% | 63.8% | -0.027 (-0.152, +0.104) | no | +1.88R | -1.01R | -1.02R | $0.68 |
| **v6_confirm_or** | 413 | 29.1% (24.9-33.7) | 24.0% | 69.2% | -0.088 (-0.248, +0.082) | no | +2.22R | -1.03R | -1.03R | $0.63 |
| **v7_buffer_confirm_2R** | 413 | 35.8% (31.2-40.4) | 30.8% | 62.7% | -0.017 (-0.145, +0.114) | no | +1.79R | -1.03R | -1.02R | $0.67 |
| **v8_pct_or_30_confirm_2R** | 413 | 33.9% (29.3-38.5) | 30.5% | 63.9% | -0.050 (-0.182, +0.084) | no | +1.83R | -1.01R | -1.02R | $0.68 |

## Ranked by net expectancy (lower bound of 95% CI)

| Rank | Variant | Net Exp R | 95% CI low | Win % | N |
|---|---|---|---|---|---|
| 1 | v7_buffer_confirm_2R | -0.017R | -0.145R | 35.8% | 413 |
| 2 | v2_buffer_5c | +0.100R | -0.150R | 20.8% | 453 |
| 3 | v5_pct_or_30_2R | -0.027R | -0.152R | 34.0% | 453 |
| 4 | v8_pct_or_30_confirm_2R | -0.050R | -0.182R | 33.9% | 413 |
| 5 | v4_buffer_2R | -0.054R | -0.185R | 33.6% | 453 |
| 6 | v1_baseline | +0.058R | -0.201R | 19.4% | 453 |
| 7 | v6_confirm_or | -0.088R | -0.248R | 29.1% | 413 |
| 8 | v3_fixed_1R | -0.216R | -0.307R | 42.8% | 453 |

## Verdict

**No variant survives costs at the 95% confidence level.**
Either the rules need a structural change (e.g. add HTF bias / liquidity filter), or the true edge is too small to overcome QQQ retail execution costs at this trade frequency.
