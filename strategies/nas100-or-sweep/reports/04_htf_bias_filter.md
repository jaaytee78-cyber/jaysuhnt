# HTF Bias Filter Test (Path 2)

Data: QQQ 1m, 2024-05-22 -> 2026-05-21
Slippage applied: $0.01/share each side. Bootstrap n=5,000.

**Hypothesis:** counter-trend OR sweeps fail more than with-trend sweeps. Filtering to **aligned** setups should lift expectancy above the unfiltered baseline.

**Bias methods tested:**
- `prev_close_dir`: bullish if prev RTH close > day-before RTH close
- `gap_dir`: bullish if today's RTH open > yesterday's RTH close (gap)
- `ema_20`: bullish if prev RTH close > 20-period EMA of RTH closes

**Reading guide:**
- `Sig?`: yes only if 95% CI strictly above 0R (real edge after costs)
- `aligned` rows are the *filtered* universe; `all` is the unfiltered baseline
- `against` rows are the *anti*-filter (should be worse than `aligned` if our hypothesis holds)

## v1_baseline
_Strict ICT: sweep close entry, 1c-tight stop, opposite OR target._

### bias = `prev_close_dir`

| Subset | N | Win % | P(tgt) | Net Exp R (95% CI) | Sig? |
|---|---|---|---|---|---|
| all | 453 | 19.4% | 16.8% | +0.058 (-0.201, +0.338) | no |
| aligned | 231 | 14.7% | 13.4% | -0.263 (-0.556, +0.057) | no |
| against | 220 | 24.5% | 20.5% | +0.406 (-0.022, +0.902) | no |

### bias = `gap_dir`

| Subset | N | Win % | P(tgt) | Net Exp R (95% CI) | Sig? |
|---|---|---|---|---|---|
| all | 453 | 19.4% | 16.8% | +0.058 (-0.201, +0.338) | no |
| aligned | 224 | 17.4% | 14.7% | +0.030 (-0.323, +0.426) | no |
| against | 228 | 21.5% | 18.9% | +0.089 (-0.289, +0.510) | no |

### bias = `ema_20`

| Subset | N | Win % | P(tgt) | Net Exp R (95% CI) | Sig? |
|---|---|---|---|---|---|
| all | 453 | 19.4% | 16.8% | +0.058 (-0.201, +0.338) | no |
| aligned | 239 | 18.0% | 15.5% | -0.133 (-0.420, +0.175) | no |
| against | 212 | 21.2% | 18.4% | +0.285 (-0.173, +0.783) | no |

## v2_buffer_5c
_Wider 5c stop above wick, opposite OR target._

### bias = `prev_close_dir`

| Subset | N | Win % | P(tgt) | Net Exp R (95% CI) | Sig? |
|---|---|---|---|---|---|
| all | 453 | 20.8% | 18.1% | +0.100 (-0.150, +0.374) | no |
| aligned | 231 | 16.0% | 14.7% | -0.221 (-0.504, +0.102) | no |
| against | 220 | 25.9% | 21.8% | +0.449 (+0.049, +0.905) | **yes** |

### bias = `gap_dir`

| Subset | N | Win % | P(tgt) | Net Exp R (95% CI) | Sig? |
|---|---|---|---|---|---|
| all | 453 | 20.8% | 18.1% | +0.100 (-0.150, +0.374) | no |
| aligned | 224 | 18.8% | 16.1% | +0.042 (-0.289, +0.399) | no |
| against | 228 | 22.8% | 20.2% | +0.162 (-0.215, +0.567) | no |

### bias = `ema_20`

| Subset | N | Win % | P(tgt) | Net Exp R (95% CI) | Sig? |
|---|---|---|---|---|---|
| all | 453 | 20.8% | 18.1% | +0.100 (-0.150, +0.374) | no |
| aligned | 239 | 18.8% | 16.3% | -0.178 (-0.428, +0.097) | no |
| against | 212 | 23.1% | 20.3% | +0.426 (-0.018, +0.913) | no |

## v3_fixed_1R
_Tight stop, target capped at 1R._

### bias = `prev_close_dir`

| Subset | N | Win % | P(tgt) | Net Exp R (95% CI) | Sig? |
|---|---|---|---|---|---|
| all | 453 | 42.8% | 42.8% | -0.216 (-0.307, -0.126) | no |
| aligned | 231 | 37.2% | 37.2% | -0.326 (-0.450, -0.199) | no |
| against | 220 | 49.1% | 49.1% | -0.092 (-0.228, +0.040) | no |

### bias = `gap_dir`

| Subset | N | Win % | P(tgt) | Net Exp R (95% CI) | Sig? |
|---|---|---|---|---|---|
| all | 453 | 42.8% | 42.8% | -0.216 (-0.307, -0.126) | no |
| aligned | 224 | 37.5% | 37.5% | -0.323 (-0.454, -0.195) | no |
| against | 228 | 48.2% | 48.2% | -0.107 (-0.235, +0.024) | no |

### bias = `ema_20`

| Subset | N | Win % | P(tgt) | Net Exp R (95% CI) | Sig? |
|---|---|---|---|---|---|
| all | 453 | 42.8% | 42.8% | -0.216 (-0.307, -0.126) | no |
| aligned | 239 | 42.7% | 42.7% | -0.216 (-0.339, -0.089) | no |
| against | 212 | 43.4% | 43.4% | -0.208 (-0.342, -0.071) | no |

## v4_buffer_2R
_5c-buffer stop, target 2R._

### bias = `prev_close_dir`

| Subset | N | Win % | P(tgt) | Net Exp R (95% CI) | Sig? |
|---|---|---|---|---|---|
| all | 453 | 33.6% | 33.1% | -0.054 (-0.185, +0.079) | no |
| aligned | 231 | 29.0% | 29.0% | -0.188 (-0.356, -0.010) | no |
| against | 220 | 38.6% | 37.7% | +0.097 (-0.095, +0.286) | no |

### bias = `gap_dir`

| Subset | N | Win % | P(tgt) | Net Exp R (95% CI) | Sig? |
|---|---|---|---|---|---|
| all | 453 | 33.6% | 33.1% | -0.054 (-0.185, +0.079) | no |
| aligned | 224 | 30.8% | 30.4% | -0.136 (-0.314, +0.049) | no |
| against | 228 | 36.4% | 36.0% | +0.032 (-0.154, +0.223) | no |

### bias = `ema_20`

| Subset | N | Win % | P(tgt) | Net Exp R (95% CI) | Sig? |
|---|---|---|---|---|---|
| all | 453 | 33.6% | 33.1% | -0.054 (-0.185, +0.079) | no |
| aligned | 239 | 32.6% | 32.2% | -0.078 (-0.256, +0.104) | no |
| against | 212 | 34.9% | 34.4% | -0.016 (-0.213, +0.176) | no |

## v5_pct_or_30_2R
_Stop = 30% of OR (volatility-scaled), target 2R._

### bias = `prev_close_dir`

| Subset | N | Win % | P(tgt) | Net Exp R (95% CI) | Sig? |
|---|---|---|---|---|---|
| all | 453 | 34.0% | 31.8% | -0.027 (-0.152, +0.104) | no |
| aligned | 231 | 31.2% | 29.4% | -0.109 (-0.284, +0.074) | no |
| against | 220 | 37.3% | 34.5% | +0.069 (-0.117, +0.256) | no |

### bias = `gap_dir`

| Subset | N | Win % | P(tgt) | Net Exp R (95% CI) | Sig? |
|---|---|---|---|---|---|
| all | 453 | 34.0% | 31.8% | -0.027 (-0.152, +0.104) | no |
| aligned | 224 | 30.8% | 28.6% | -0.117 (-0.295, +0.061) | no |
| against | 228 | 37.3% | 35.1% | +0.066 (-0.119, +0.260) | no |

### bias = `ema_20`

| Subset | N | Win % | P(tgt) | Net Exp R (95% CI) | Sig? |
|---|---|---|---|---|---|
| all | 453 | 34.0% | 31.8% | -0.027 (-0.152, +0.104) | no |
| aligned | 239 | 33.9% | 30.5% | -0.047 (-0.219, +0.130) | no |
| against | 212 | 34.4% | 33.5% | +0.006 (-0.188, +0.199) | no |

## v6_confirm_or
_Confirmation entry, tight stop, opposite OR target._

### bias = `prev_close_dir`

| Subset | N | Win % | P(tgt) | Net Exp R (95% CI) | Sig? |
|---|---|---|---|---|---|
| all | 413 | 29.1% | 24.0% | -0.088 (-0.248, +0.082) | no |
| aligned | 206 | 25.2% | 20.4% | -0.303 (-0.493, -0.101) | no |
| against | 205 | 33.2% | 27.8% | +0.138 (-0.129, +0.408) | no |

### bias = `gap_dir`

| Subset | N | Win % | P(tgt) | Net Exp R (95% CI) | Sig? |
|---|---|---|---|---|---|
| all | 413 | 29.1% | 24.0% | -0.088 (-0.248, +0.082) | no |
| aligned | 203 | 30.0% | 23.6% | -0.038 (-0.275, +0.220) | no |
| against | 209 | 28.2% | 24.4% | -0.132 (-0.347, +0.112) | no |

### bias = `ema_20`

| Subset | N | Win % | P(tgt) | Net Exp R (95% CI) | Sig? |
|---|---|---|---|---|---|
| all | 413 | 29.1% | 24.0% | -0.088 (-0.248, +0.082) | no |
| aligned | 220 | 28.6% | 22.3% | -0.171 (-0.372, +0.042) | no |
| against | 191 | 29.8% | 26.2% | +0.017 (-0.243, +0.294) | no |

## v7_buffer_confirm_2R
_Confirmation entry, 5c stop, target 2R._

### bias = `prev_close_dir`

| Subset | N | Win % | P(tgt) | Net Exp R (95% CI) | Sig? |
|---|---|---|---|---|---|
| all | 413 | 35.8% | 30.8% | -0.017 (-0.145, +0.114) | no |
| aligned | 206 | 34.0% | 26.7% | -0.098 (-0.279, +0.085) | no |
| against | 205 | 38.0% | 35.1% | +0.075 (-0.119, +0.267) | no |

### bias = `gap_dir`

| Subset | N | Win % | P(tgt) | Net Exp R (95% CI) | Sig? |
|---|---|---|---|---|---|
| all | 413 | 35.8% | 30.8% | -0.017 (-0.145, +0.114) | no |
| aligned | 203 | 35.5% | 30.0% | -0.028 (-0.215, +0.166) | no |
| against | 209 | 36.4% | 31.6% | -0.001 (-0.188, +0.186) | no |

### bias = `ema_20`

| Subset | N | Win % | P(tgt) | Net Exp R (95% CI) | Sig? |
|---|---|---|---|---|---|
| all | 413 | 35.8% | 30.8% | -0.017 (-0.145, +0.114) | no |
| aligned | 220 | 36.8% | 30.0% | -0.005 (-0.186, +0.174) | no |
| against | 191 | 35.1% | 31.9% | -0.020 (-0.216, +0.182) | no |

## v8_pct_or_30_confirm_2R
_Confirmation entry, 30%-OR stop, target 2R._

### bias = `prev_close_dir`

| Subset | N | Win % | P(tgt) | Net Exp R (95% CI) | Sig? |
|---|---|---|---|---|---|
| all | 413 | 33.9% | 30.5% | -0.050 (-0.182, +0.084) | no |
| aligned | 206 | 31.6% | 27.2% | -0.136 (-0.315, +0.046) | no |
| against | 205 | 36.6% | 34.1% | +0.046 (-0.148, +0.244) | no |

### bias = `gap_dir`

| Subset | N | Win % | P(tgt) | Net Exp R (95% CI) | Sig? |
|---|---|---|---|---|---|
| all | 413 | 33.9% | 30.5% | -0.050 (-0.182, +0.084) | no |
| aligned | 203 | 34.0% | 30.0% | -0.053 (-0.243, +0.140) | no |
| against | 209 | 34.0% | 31.1% | -0.043 (-0.229, +0.145) | no |

### bias = `ema_20`

| Subset | N | Win % | P(tgt) | Net Exp R (95% CI) | Sig? |
|---|---|---|---|---|---|
| all | 413 | 33.9% | 30.5% | -0.050 (-0.182, +0.084) | no |
| aligned | 220 | 34.1% | 29.1% | -0.066 (-0.239, +0.110) | no |
| against | 191 | 34.0% | 32.5% | -0.021 (-0.220, +0.183) | no |

---

## Top aligned subsets ranked by net expectancy lower 95% CI

| Rank | Variant | Bias | N | Win % | Net Exp R | 95% CI low | Sig? |
|---|---|---|---|---|---|---|---|
| 1 | v7_buffer_confirm_2R | ema_20 | 220 | 36.8% | -0.005R | -0.186R | no |
| 2 | v7_buffer_confirm_2R | gap_dir | 203 | 35.5% | -0.028R | -0.215R | no |
| 3 | v5_pct_or_30_2R | ema_20 | 239 | 33.9% | -0.047R | -0.219R | no |
| 4 | v8_pct_or_30_confirm_2R | ema_20 | 220 | 34.1% | -0.066R | -0.239R | no |
| 5 | v8_pct_or_30_confirm_2R | gap_dir | 203 | 34.0% | -0.053R | -0.243R | no |
| 6 | v4_buffer_2R | ema_20 | 239 | 32.6% | -0.078R | -0.256R | no |
| 7 | v6_confirm_or | gap_dir | 203 | 30.0% | -0.038R | -0.275R | no |
| 8 | v7_buffer_confirm_2R | prev_close_dir | 206 | 34.0% | -0.098R | -0.279R | no |
| 9 | v5_pct_or_30_2R | prev_close_dir | 231 | 31.2% | -0.109R | -0.284R | no |
| 10 | v2_buffer_5c | gap_dir | 224 | 18.8% | +0.042R | -0.289R | no |
| 11 | v5_pct_or_30_2R | gap_dir | 224 | 30.8% | -0.117R | -0.295R | no |
| 12 | v4_buffer_2R | gap_dir | 224 | 30.8% | -0.136R | -0.314R | no |
| 13 | v8_pct_or_30_confirm_2R | prev_close_dir | 206 | 31.6% | -0.136R | -0.315R | no |
| 14 | v1_baseline | gap_dir | 224 | 17.4% | +0.030R | -0.323R | no |
| 15 | v3_fixed_1R | ema_20 | 239 | 42.7% | -0.216R | -0.339R | no |

## Verdict

**No (variant, bias) combination's aligned-subset 95% CI is strictly above 0R after costs.**
HTF bias filtering does not unambiguously surface a real edge in our 2-year sample. 
Look at the ranked table above - if any rows show a clear *direction* (aligned >> against), 
that's still useful information even without statistical significance.
