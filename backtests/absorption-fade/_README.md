# Absorption Fade — Backtest Log

Manual replay log for the [Absorption Fade strategy](../../knowledge-base/strategies/absorption-fade-scalp.md).

## How to use

1. Copy `_template.md` for each instance you find in ATAS Replay.
2. Name the file: `YYYY-MM-DD-ES-NN.md` (e.g. `2026-05-12-ES-03.md` for the 3rd ES instance on May 12, 2026).
3. Fill in **every field**, including instances where the trigger bar (#5) didn't fire — they're still data.
4. Once you have 30+ instances, fill in the stats table below.

## Sample size required per phase

| Phase | Min instances | What to record |
|---|---|---|
| Phase 1 (manual replay) | 30 | All 5 conditions evaluated by hand |
| Phase 2 (indicator) | 100 | Indicator-flagged setups + your manual condition #1 check |
| Phase 3 (live micros) | 30 | Real fills, real slippage |

## Stats roll-up (fill in after each batch)

```
Batch:           Phase 1 manual replay
Date range:      ____ to ____
Total instances: ____
Trades taken (5/5): ____
Wins:            ____
Losses:          ____
Breakevens:      ____
Time-stop exits: ____

Win rate:        ____%
Avg win (R):     ____R
Avg loss (R):    ____R   (should be ~ -1R if stops obeyed)
Expectancy:      ____R per trade
Max consecutive losses: ____
Max drawdown (R): ____

Decision:        [ ] Pass gate → advance
                 [ ] Fail gate → refine rules + re-test
                 [ ] Fail gate → drop strategy
```

## Expectancy formula

```
Expectancy (R) = (Win% × Avg Win R) − (Loss% × |Avg Loss R|)
```

Pass thresholds (per [roadmap](../../knowledge-base/strategies/absorption-fade-roadmap.md)):

- **Phase 1 gate:** Expectancy ≥ 0.2R, Win% ≥ 45%, Avg Win ≥ 1.3R, n ≥ 30
- **Phase 2 gate:** Expectancy ≥ 0.3R, Win% ≥ 50%, Avg Win ≥ 1.4R, n ≥ 100

## Honesty rules

- Log losses **even when you wouldn't have taken the trade live.** A 5/5 setup that lost is data.
- Do **not** retroactively decide "I would have skipped that one." That's hindsight cheating.
- If you scored a setup 4/5 and it ran 3R — **do not** count it as a win. Rules are rules.
- If the indicator (Phase 2) flags a setup and condition #1 (location) is missing — log it as a "filtered" instance, not a trade. Tracks indicator false-positive rate.

## Index of instances

(Update this list as you add files, or run `ls` in this folder.)

- _template.md
