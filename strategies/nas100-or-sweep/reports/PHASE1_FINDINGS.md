# Phase 1 Findings — NAS100 OR Sweep & Reversal (QQQ proxy)

**Data:** QQQ 1-minute bars, 2024-05-22 → 2026-05-21 (501 trading days, 439,877 bars)
**Setup definition:** Strict ICT-style — entry on close of bar that wicks beyond OR and closes back inside; stop 1¢ beyond sweep wick; target opposite OR side; time-stop at 11:00 ET.
**Costs:** None applied yet. This is the *raw pattern* edge measurement.

## Headline result

| Metric | Value |
|---|---|
| Days analysed | 501 |
| Days with a sweep | 453 (90.4%) |
| **Win rate** | **19.4%** |
| **Expectancy / setup** | **+0.132 R** |
| P(target hit) | 16.8% |
| P(stop hit) | **80.1%** |
| P(timed out) | 3.1% |
| Avg win | +4.81 R |
| Avg loss | -1.00 R |
| Median R | -1.00 R |

**Verdict:** the pattern has a **marginal positive expectancy**, driven by rare large winners — not by a high hit rate. Year-by-year stability is OK (2024: +0.08R, 2025: +0.16R, 2026: +0.14R) — same direction every year.

## What this actually means

This is a **lottery-ticket payoff**:
- 80% of trades hit a tight stop for -1R
- 15% of trades reach the opposite OR side, paying +2R to +16R
- Median outcome is a loss; the average is barely positive

Over 453 setups in 2 years, you'd average ~+60R total — about one setup per trading day, so ~$60 / day at $1 per R. That's real, but it requires:

1. **Brutal psychological tolerance.** 80% loss rate means losing streaks of 7-10 are normal. Most retail traders quit before the math plays out.
2. **No execution costs eating the edge.** We haven't applied slippage yet. With QQQ tick size 1¢, a 5¢ stop, and ~1¢ slippage each side → 40% of risk lost to costs. That likely turns +0.13R into ~+0.05R or below.
3. **Discipline to take every setup.** Skip the "obvious losers" (you'll subjectively skip the winners) and the math collapses.

## Other findings worth noting

- **Sweep frequency is huge:** 90% of days produce a sweep. Almost no "no setup" days. This is good for trade frequency but means we shouldn't expect "selective" filters to add a lot — the universe is already small (453 setups/2yr).
- **No side bias:** upper sweeps (shorts) and lower sweeps (longs) perform almost identically (+0.14R vs +0.13R). The model is symmetric.
- **Tuesday is suspiciously good** (+0.67R, 28% win rate) and Monday is bad (-0.19R). With only ~100 days per weekday, this could easily be noise — needs a hypothesis test or it stays in the "be skeptical" pile.
- **OR size is highly variable:** median $2.28, but ranges from $0.72 to $8.80 (and as % of price, 0.14% to 2.07%). Volatility-regime filtering is probably the highest-value filter to test.

## Open questions before committing to Phase 2

1. **Stop width experiment.** The 1¢-beyond-wick stop is the textbook ICT version. What does the edge look like if we widen to:
   - Sweep candle range (high-low of the sweep bar)?
   - 50% of OR size?
   - 1× ATR(14)?
   - Each loosens win rate and lowers R-multiples — find the sweet spot.

2. **Target experiment.** What if target is fixed 1R, 1.5R, 2R, instead of "opposite OR side"? Likely much higher hit rate, smaller R per win.

3. **Confirmation entry.** Currently we enter on the close of the sweep bar itself. What if we wait for the next bar to close back inside the OR, then enter? Slower entry, fewer false signals — but you also miss some winners.

4. **Realistic costs.** Apply 1¢ + slippage and see if expectancy survives.

5. **Bootstrap confidence intervals.** With 453 trades and a fat-tailed R distribution, the 95% CI on +0.13R may very well include zero. Need to test before declaring victory.

## My recommendation

The pattern has **a real but fragile edge** in raw form. Before we invest more in this exact rule set, we should run **two quick experiments** (each ~30 lines of code):

- **Experiment A:** widen stop to "sweep candle range", fix target at 1R, see if expectancy improves and win rate becomes tolerable.
- **Experiment B:** add bootstrap CIs and apply realistic 1¢ slippage to the existing v1.

If A produces a more tradeable profile (e.g. 45% win rate, +0.2R expectancy) **and** B shows the raw edge survives costs, we move to Phase 2 (full backtest with equity curve, drawdowns, regime tests). If both look weak, we pivot rules — maybe to **NY AM PD-Liquidity Sweep** (Option C from the original menu) before more upgrades.

**Cost decision:** I would *not* upgrade Polygon yet. We have 2 years and 501 days — plenty for these experiments. Upgrade only if we hit a real edge and want walk-forward validation on 5+ years.



---

# Update — Experiments A & B (variant grid + costs + bootstrap CIs)

**See `reports/03_variant_grid.md` for the full table.** Summary below.

We tested **8 variants** of the strategy (different stop methods, target methods, entry timing) under two cost models (gross / net with $0.01/share each side) and ran 5,000-iter bootstrap 95% CIs on every expectancy.

## Headline result

**Zero variants reject the null hypothesis "no edge" at 95% confidence after costs.**

| Rank | Variant | Net Exp R | 95% CI | Win % | Verdict |
|---|---|---|---|---|---|
| 1 | v7_buffer_confirm_2R | -0.017R | (-0.145, +0.114) | 35.8% | CI straddles 0 |
| 2 | v2_buffer_5c | **+0.100R** | (-0.150, +0.374) | 20.8% | CI straddles 0 |
| 3 | v5_pct_or_30_2R | -0.027R | (-0.152, +0.104) | 34.0% | CI straddles 0 |
| ... | ... | ... | ... | ... | ... |
| 8 | v3_fixed_1R | **-0.216R** | (-0.307, -0.126) | 42.8% | **Confirmed loser** |

## What we learned

1. **The raw pattern probably has *some* edge but our sample (n=453) is too small to prove it.** v1 baseline and v2_buffer_5c have point estimates of +0.06R / +0.10R after costs — directionally positive — but the 95% CIs are gigantic ([-0.20, +0.34] for v1) because the R-distribution is fat-tailed. To halve the CI width we'd need ~4× the sample (≈1,800 setups, i.e. ~5+ years of data).

2. **A tight-stop / fixed-target combo is statistically a *losing* strategy.** v3_fixed_1R with a tight stop and 1R target has a 95% CI of (-0.31R, -0.13R), entirely below zero. So while the "lottery ticket" structure (huge wins, many small losses) might have edge, capping the wins demonstrably destroys it. **The fat tail is doing the work.**

3. **Wider stops help slippage survival but don't fix the small-sample problem.** The %-OR stops (v5, v8) reduce the % of risk lost to slippage from ~5% to ~3%, but the underlying edge is still too noisy to detect.

4. **Confirmation entry doesn't add value here.** v6/v7/v8 all use confirmation and trade ~10% fewer days (413 vs 453); their net expectancies are no better than the equivalent sweep-close variants. Confirmation appears to filter *roughly proportionally* — not selectively against losers.

5. **Win-rate and expectancy are nearly orthogonal.** v3 has the highest win rate (42.8%) and the worst expectancy. v1 has the lowest win rate (19.4%) and one of the highest expectancies. Don't optimise for win rate — optimise for expectancy.

## What this means strategically

The honest read is:

- This strategy as a *standalone, mechanical* edge **isn't proven** on QQQ within our 2-year, 501-day sample. It's not falsified either — the point estimates are positive and consistent year-over-year (2024: +0.08R, 2025: +0.16R, 2026: +0.14R). It's *plausibly real but unproven*.
- To resolve, we need either **more data** (5+ years to shrink the CI) or **better setup quality** (filter to a subset where the edge is bigger).

## Three forward paths

### Path 1 — More data
Upgrade Polygon to Stocks Starter (~$29/mo for 1-2 months), pull 5+ years, re-run the same grid. With ~1,250 days the CIs roughly halve, which would clearly distinguish "real but small edge" from "no edge".

### Path 2 — Add a confluence filter on existing data
Test whether a filter concentrates the edge into a smaller, higher-quality subset. Candidates that have a hypothesis behind them (not data-mined):
- **HTF bias filter:** only take longs when 1H/4H trend is up, vice versa
- **Liquidity context:** only take sweeps that occur near PDH/PDL or pre-market high/low
- **Volatility regime:** only take when ATR(14d) is in the top half (more room to run to target)
- **No major news on tap:** skip CPI/FOMC/NFP days

If any single filter lifts net expectancy CI lower bound above zero, we have something. If none do, the pattern probably isn't tradable as a primary edge.

### Path 3 — Pivot
Strategy doesn't exist in isolation — it could still be a *confluence* in a larger system (e.g. ICT model where this is one of three required ingredients). Or pivot to PDH/PDL liquidity sweep (Option C from the original menu).

## My recommendation

**Path 2 first**, then Path 1 if Path 2 looks promising. The reasoning:

- Path 2 costs nothing and uses existing data. If a sensible filter (e.g. HTF bias) lifts the lower CI bound above zero, that's *direct evidence* the pattern has a real edge inside a higher-quality subset.
- If no filter helps, then more data alone (Path 1) probably won't either — the pattern is too weak. We'd pivot.
- If a filter helps, *then* upgrade Polygon and validate on 5 years. That's where rigorous walk-forward starts to matter.

I'd start with **HTF bias** because it's the most ICT-classical and has the strongest a-priori case. One filter at a time, no kitchen-sink.



---

# Update — HTF Bias Filter (Path 2 result)

**Surprise finding:** the strategy is **counter-trend / mean-reverting**, not trend-following. My original "aligned with bias = better" hypothesis was wrong.

## The headline result

The single combination with a 95% CI strictly above zero after costs:

| Variant | Bias | Subset | N | Win % | Net Exp R | 95% CI | Sig? |
|---|---|---|---|---|---|---|---|
| `v2_buffer_5c` | `prev_close_dir` | **against** | 220 | 25.9% | **+0.449R** | **(+0.049, +0.905)** | **yes** |

**Reading this row:** when the previous day's RTH close was higher than the day before (bullish bias), and we take an **upper-OR sweep short** (i.e. counter-trend) with a 5¢-buffer stop and opposite-OR target — net expectancy is +0.45R per setup with a 95% CI that does not include zero, even after $0.02/share round-trip costs.

## The directional pattern is consistent across the whole grid

Across all 8 variants × 3 bias methods, the **against** subset has higher expectancy than the **aligned** subset in nearly every cell. Examples:

| Variant | Bias | aligned E | against E | Δ |
|---|---|---|---|---|
| v1_baseline | prev_close_dir | -0.263R | +0.406R | **+0.67R** |
| v1_baseline | ema_20 | -0.133R | +0.285R | +0.42R |
| v2_buffer_5c | prev_close_dir | -0.221R | **+0.449R** | +0.67R |
| v2_buffer_5c | ema_20 | -0.178R | +0.426R | +0.60R |
| v4_buffer_2R | prev_close_dir | -0.188R | +0.097R | +0.29R |
| v6_confirm_or | prev_close_dir | -0.303R | +0.138R | +0.44R |

That's a **systematic** effect, not a single lucky cell — and it makes economic sense.

## Why counter-trend?

An OR sweep is a **liquidity grab event**. Two interpretations:

- *With-trend interpretation* (was my hypothesis): "The trend continues. Sweep is just a noise event before the trend resumes." — Implies aligned setups should win.
- *Counter-trend interpretation* (what the data says): "The sweep represents *exhaustion* of late-arriving trend followers. In a bull day, an upper-OR sweep is bullish euphoria getting punished by sellers. In a bear day, a lower-OR sweep is bearish capitulation getting bought." — Implies against setups should win.

The data strongly favours the second interpretation on QQQ 2024-2026.

## Caveats — don't pop champagne yet

1. **Multiple-testing penalty.** We ran 48 tests (8 variants × 3 biases × 2 subsets). At nominal p=0.05, we expected ~2 false positives by chance. We got 1 significant result — barely above what pure noise would produce. **Treat this as a candidate, not a discovery.**

2. **Single regime.** Two years (2024-2026) is one macro regime — predominantly bullish. The contrarian pattern may not hold in a 2008/2020-style crash regime where trend continuation dominates.

3. **The narrowest 95% CI lower bound is +0.05R.** That's a real but small edge. At ~110 against-setups per year per side, that's an expected annual return of ~50R/year. Tradeable, but not large.

4. **The alignment definition matters.** Switching what we call "aligned" entirely flips the verdict. We need to lock in our hypothesis BEFORE testing on new data.

## Strategic recommendation: now upgrade Polygon

We finally have something specific to validate:

> **Hypothesis (locked in):** *On QQQ 1m, an upper-OR sweep on a day where the previous RTH close was above the day-before's RTH close, traded short with stop = sweep wick + 5¢ and target = opposite OR side, has positive net expectancy.*  
> *(And symmetric for lower sweeps on bearish-bias days.)*

This is a clean, falsifiable statement. The right next step:

1. **Upgrade Polygon to Stocks Starter (~$29/mo) for one billing cycle.**
2. **Pull 5+ years of QQQ 1m bars** (2020-01 → today).
3. **Re-run the variant grid + bias filter on out-of-sample data only** (e.g. 2020-2023, holding 2024-2026 as in-sample).
4. **Pass criterion:** counter-trend (`against`) subset of v2_buffer_5c × prev_close_dir has 95% CI lower bound > 0R on the out-of-sample years.

If it passes → we have a real, validated edge → move to Phase 2 (full backtest with equity curve, drawdown, position sizing).
If it fails → the 2024-2026 result was period-specific or a multiple-testing artefact → we go back to Path 3.

**Total cost of validation: ~$29.** Compared to the value of knowing whether the strategy is real, that's a no-brainer.
