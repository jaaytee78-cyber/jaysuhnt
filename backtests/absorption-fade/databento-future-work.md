# Databento — Phase 4 Future Work

This is a **planning stub** for the Phase 4 robustness backtest using [Databento](https://databento.com/). **Do not start work here until Phase 3 (live micros forward-test) is passed.** See [roadmap](../../knowledge-base/strategies/absorption-fade-roadmap.md).

> Why we're noting this now: so when you reach Phase 4, the research is already half-done and you don't waste a weekend re-figuring out the dataset IDs, schemas, and costs.

---

## Why Databento (and not ATAS Replay)

ATAS Replay is fine for visual review of a single day, but to test edge across **years** of data and multiple regimes you need:

- Programmatic access (so you can run thousands of simulated trades without sitting in front of the screen)
- Tick-level fidelity (to reconstruct footprint bars accurately)
- Coverage of historical periods you can't replay one-by-one (5+ years)

Databento is the most cost-effective way to get this for CME futures.

---

## Dataset of interest

- **Dataset ID:** `GLBX.MDP3` — CME Globex MDP 3.0 ([docs](https://databento.com/docs/venues-and-datasets/glbx-mdp3))
- **Covers:** CME, CBOT, NYMEX, COMEX → includes ES, NQ, MES, MNQ
- **Schemas you'll need:**
  - `trades` — every print (price, size, aggressor side)
  - `mbp-1` (top of book quotes) — to classify each trade as bid-side or ask-side aggression for delta/footprint reconstruction
  - Optionally `mbp-10` — full depth-of-book if you want to model absorption from the order book itself

*Content rephrased for compliance with licensing restrictions.*

---

## Cost estimate (rough, confirm at signup)

Databento is pay-as-you-go. For a Phase 4 backtest:

| Item | Estimate |
|---|---|
| ES trades, 5 years | ~$30–80 |
| ES mbp-1 quotes, 5 years | ~$50–150 |
| NQ trades + mbp-1, 5 years | ~$80–200 |
| **Total budget** | **~$150–500** |

This is a one-time historical pull. You can store the parquet/dbn files locally and re-run backtests offline indefinitely.

> **Verify before paying.** Pricing changes. Pull a 1-day sample first, look at the quoted cost in the API response, then extrapolate.

---

## Build outline (Python)

When the time comes, here's what the backtest project will look like. **You will not write this — Kiro will.** This is just so you can see the shape.

```
backtests/absorption-fade/databento/
├── README.md
├── pyproject.toml          # Python package config
├── requirements.txt        # databento, pandas, numpy, pyarrow
├── src/
│   ├── data_pull.py        # Pull trades + mbp-1 from Databento, save as parquet
│   ├── footprint.py        # Reconstruct footprint bars (per-price bid/ask volume)
│   ├── candles.py          # Aggregate to 1m / 30s candles with delta, max delta, CVD
│   ├── conditions.py       # Implement the 5 AF conditions
│   ├── backtest.py         # Walk through history, simulate trades with slippage
│   ├── stats.py            # Win%, expectancy, max DD, per-regime breakdown
│   └── plot.py             # Equity curve, signal markers, regime annotations
├── notebooks/
│   ├── 01-data-explore.ipynb
│   ├── 02-condition-tuning.ipynb
│   └── 03-walk-forward.ipynb
└── results/
    └── (generated: equity curves, stats CSVs, per-regime reports)
```

### Key engineering challenges

1. **Footprint reconstruction.** Databento gives you trades and quotes separately. You have to match each trade to the prevailing best bid / best ask at the trade's nanosecond timestamp to classify it as bid-side or ask-side aggression. This is the foundation of delta. Get this wrong → entire backtest is garbage.
2. **Session handling.** CME trades nearly 24h. You need clean session boundaries (RTH start 9:30 ET, etc.) for VWAP and Volume Profile computations.
3. **Continuous contract joining.** Front-month rolls every quarter. You need a roll method (Volume / OI / calendar) to stitch contracts into a continuous backtest series.
4. **Slippage model.** Don't assume fills at the close price. Use at minimum: 1 tick adverse slippage on entry + 1 tick on exit (more on NQ).
5. **Walk-forward, not single backtest.** Optimize parameters on years 1–3, test on year 4. Re-optimize on years 1–4, test on year 5. Etc. This catches curve-fitting.

---

## Decision criteria (Phase 4 gate)

Per [roadmap](../../knowledge-base/strategies/absorption-fade-roadmap.md):

| Metric | Required to size up |
|---|---|
| Edge holds in all 4+ market regimes (trend up, trend down, chop, high-vol) | ☐ |
| Worst calendar year still profitable or break-even | ☐ |
| Max DD < 15R or < 10% of account | ☐ |
| Walk-forward out-of-sample expectancy ≥ 60% of in-sample | ☐ |

If any fail → strategy is curve-fit. Back to Phase 2 with stricter rules.

---

## Reading list (when you get here)

- [Databento futures introduction](https://databento.com/docs/examples/futures/futures-introduction)
- [Databento tick sizes & notional values in Python](https://databento.com/blog/tick-sizes-and-values)
- [GLBX.MDP3 dataset spec](https://databento.com/docs/venues-and-datasets/glbx-mdp3)

*Content from external sources was rephrased for compliance with licensing restrictions.*
