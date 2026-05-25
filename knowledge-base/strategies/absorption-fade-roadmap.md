# Absorption Fade — Roadmap

The 4-phase plan from "interesting idea" to "live trading with confidence." **Do not skip phases.** Each phase has a decision gate — if the numbers don't pass, you go back, not forward.

---

## Phase 1 — Manual replay (start here)

**Goal:** Learn to *see* the setup. No code, no automation.

- **Tool:** ATAS Replay mode
- **Instrument:** ES only (cleaner than NQ)
- **Sample size:** 30 instances minimum
- **Method:**
  1. Pick the last 20 trading days
  2. Walk replay one bar at a time during NY Open / Overlap / NY PM windows
  3. Whenever conditions #1 (level) + #2 (volume) + #3 (delta/structure) appear, evaluate fully
  4. Log every instance — hits and misses — in [`backtests/absorption-fade/_template.md`](../../backtests/absorption-fade/_template.md)
- **Time:** ~1 week of evenings

### Phase 1 decision gate

| Metric | Required to advance |
|---|---|
| Win rate | ≥ 45% |
| Avg R | ≥ 1.3 |
| Expectancy | Positive (> 0.2R per trade) |
| Sample size | 30+ instances |

If you don't pass: refine the rules (tighten condition #3 thresholds, restrict to higher-quality levels), re-test. Do **not** advance.

---

## Phase 2 — Custom ATAS indicator

**Goal:** Scale sample size 5–10× by auto-detecting setups in replay.

- **Tool:** `AbsorptionFadeScout` indicator (C#, in this repo)
- **Build:** I write the code, you compile + load (see [indicator README](../../indicators/atas-csharp/AbsorptionFadeScout/README.md))
- **Use:**
  1. Run indicator on ATAS Replay across 60+ trading days
  2. Indicator marks every bar that satisfies conditions #2–#5
  3. You evaluate each flagged bar manually for condition #1 (location)
  4. Log 100+ instances in the backtest template

### Phase 2 decision gate

| Metric | Required to advance |
|---|---|
| Win rate | ≥ 50% |
| Avg R | ≥ 1.4 |
| Expectancy | ≥ 0.3R per trade |
| Sample size | 100+ instances |
| Robustness | Edge holds across at least 2 different market regimes (trend / chop) |

If you don't pass: rule refinement, possibly drop the strategy. Do **not** advance.

---

## Phase 3 — Live forward-test on micros

**Goal:** Find out what slippage, emotions, and fills do to the edge.

- **Tool:** ATAS live, **micros only** — MES (1/10 of ES) or MNQ (1/10 of NQ)
- **Size:** 1 contract per trade
- **Sample size:** 30+ live trades, minimum 4 weeks
- **Method:**
  1. Trade only A+ setups (5/5 conditions, no exceptions)
  2. Log every trade in `journal/trades/` using the trade template
  3. Compare live results to Phase 2 backtest
- **Why micros:** ~$1.25 per tick on MES vs $12.50 on ES. Cheap tuition.

### Phase 3 decision gate

| Metric | Required to advance |
|---|---|
| Live expectancy | ≥ 70% of Phase 2 expectancy |
| Adherence | Followed plan ≥ 90% of trades |
| Max drawdown | Within 1.5× backtest max DD |
| Psych | No tilted / impulsive trades |

If you don't pass: it's almost always execution / psych, not the strategy. Stay on micros until consistent.

---

## Phase 4 — Databento robustness testing

**Goal:** Stress-test the edge across years of data and multiple regimes before sizing up.

- **Tool:** Databento ([CME Globex MDP 3.0](https://databento.com/docs/venues-and-datasets/glbx-mdp3)) + Python
- **Scope:**
  - 5+ years of ES data (covers 2020 COVID, 2022 bear, 2023 chop, 2024+ trend)
  - Walk-forward parameter optimization
  - Slippage modelling
  - Regime-segmented stats (trend vs chop, high-vol vs low-vol)
- **Cost:** Databento is pay-as-you-go; budget ~$50–200 for the historical data pull
- **Build effort:** 2–4 weeks if Python comfortable. See [`databento-future-work.md`](../../backtests/absorption-fade/databento-future-work.md).

### Phase 4 decision gate

| Metric | Required to size up |
|---|---|
| Edge holds | Positive expectancy in all 4+ market regimes |
| Worst year | Still profitable (or break-even) |
| Max DD | < 15R or < 10% of account |
| Walk-forward | Out-of-sample expectancy ≥ 60% of in-sample |

If you don't pass: edge was probably curve-fit. Back to Phase 2 with stricter rules.

---

## Anti-patterns (things that kill traders at this stage)

- **Skipping straight to Phase 4** because "code feels productive." It isn't. You'll build a backtest of an edge you don't understand.
- **Skipping Phase 3** because backtest looked great. Slippage and emotions are *not* in your backtest.
- **Sizing up before Phase 4 passes.** Live edge on micros ≠ scalable edge on full contracts.
- **Tweaking rules after every losing trade.** Rules change at decision gates only, with sample size to support the change.
- **Trading other instruments** (CL, GC, RTY) before ES is profitable. One edge, one instrument, until it works.

---

## Status tracker

- [ ] Phase 1 started: __ / __ / ____
- [ ] Phase 1 decision gate passed: __ / __ / ____
- [ ] Phase 2 indicator built and installed
- [ ] Phase 2 decision gate passed: __ / __ / ____
- [ ] Phase 3 micros forward-test started: __ / __ / ____
- [ ] Phase 3 decision gate passed: __ / __ / ____
- [ ] Phase 4 Databento research complete
- [ ] Phase 4 decision gate passed: __ / __ / ____
- [ ] Sized up to full contracts: __ / __ / ____
