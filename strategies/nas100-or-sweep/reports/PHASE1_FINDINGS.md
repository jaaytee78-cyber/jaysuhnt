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
