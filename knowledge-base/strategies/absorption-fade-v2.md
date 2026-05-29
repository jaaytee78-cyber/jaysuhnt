# Absorption Fade v2 — Delta Confluence Edition

A mechanical order-flow scalping strategy for **NQ / ES futures** on **ATAS**.

> **Status:** Merged best-of-both spec. Combines the validated discipline of [AF v1](./absorption-fade-scalp.md) (% risk sizing, time stop, structural targets, 4-phase validation roadmap) with the microstructure tuning of the DAC research draft (233-tick footprint, NQ-calibrated 4:1 imbalance threshold, hidden-buying CVD framing, 0–5 confluence score). This is a **new hypothesis, not a validated strategy.** The [4-phase roadmap](./absorption-fade-roadmap.md) applies to v2 from scratch.

---

## What changed from v1, and why

| Slot | v1 | v2 | Why |
|---|---|---|---|
| Chart | 1m footprint (30s on NQ) | **233-tick footprint** | Time bars distort absorption reads on slow tape. Tick bars print evenly across volume, not time |
| Imbalance threshold | 300% (3:1) | **4:1 NQ / 3:1 ES** (instrument-calibrated) | NQ is materially noisier than ES — 3:1 fires constantly |
| C2/C3 structure | Volume + delta-no-progress as separate conditions | **Imbalance + heavy-delta-no-progress as one bar character condition** (C3) — separate cluster imbalance C2 | Cleaner separation: C2 = footprint signature, C3 = bar character |
| CVD divergence | Classic only (price extends, CVD doesn't) | **Either classic OR hidden** (price extends w/o CVD, OR CVD extends w/o price) | Hidden divergence catches stealth accumulation v1 misses |
| Trigger (C5) | Midpoint reclaim | **Midpoint reclaim AND delta flip on trigger bar** | Midpoint reclaim alone can happen on weak retraces; delta flip filters them |
| Scoring | 5/5 binary | **0–5 confluence score, arrow at 5/5** | Lets you watch conditions build pre-entry; better feedback |
| Indicator | Scout: auto 4/4 + your manual location call | **Confluence: auto-score 0–4 (C2–C5) + manual level toggle = final score 0–5** | Same human-in-the-loop discipline, better visibility |

What did **not** change: 5-condition gate, % risk sizing, time stop, TP1=1R+structural TP2, daily loss/profit limits, session windows, [4-phase roadmap](./absorption-fade-roadmap.md).

---

## The mental model (unchanged)

Price runs into a known level. Aggressive market orders pile in expecting a breakout. Someone bigger is sitting there with limit orders, eating every print. The aggressors get filled but **price doesn't move**. They're now trapped. When they realize it and cover, the reversal you're trading is just *their* exit liquidity.

You are not predicting. You are reading a transaction.

---

## ATAS chart configuration

### Chart 1 — Execution

- **Bars:** **233-tick footprint** (replaces v1's 1m / 30s time bars)
- **Footprint mode:** Bid × Ask (numbers visible on each cluster)
- **Imbalance threshold:** **4.0 on NQ, 3.0 on ES** (configure per instrument)
- **Cluster colouring:** by Delta
- **Overlays on the same panel:**
  - Session VWAP + 1σ and 2σ bands
  - Volume Profile — Session (POC / VAH / VAL visible)
- **Subgraph:**
  - Cumulative Delta (session-anchored)

### Chart 2 — Context (do not trade from this)

- **Timeframe:** 1-minute candles
- Session VWAP
- Daily Volume Profile (last 5 days, POC + value areas)
- Prior day H/L, weekly H/L, overnight H/L plotted

### Chart 3 — DOM + Smart Tape (optional but recommended)

- DOM: watch for pulled liquidity at your level when about to enter
- Smart Tape: min size 25–50 contracts; reconstructs split institutional orders

---

## Mechanical entry — 5 conditions, all required

You do not take the trade unless **all five** print. No exceptions. The indicator will auto-score C2–C5 and give you a 0–4 reading; C1 is your manual call.

### C1 — Location (manual)

Price tags a **predefined HTF level** marked at session start:

- Prior day H/L, weekly H/L, overnight H/L
- Session VAH / VAL / POC (today or prior)
- Daily HVN
- VWAP, VWAP ±1σ, VWAP ±2σ band

> **"Predefined" matters.** The level was on the chart before price got there. You did not draw it after the fact. Mid-range absorption is noise.

### C2 — Cluster imbalance at the extreme

The footprint cluster at bar high or bar low shows institutional-scale absorption:

- **Long setup:** at bar **low**, ask volume / bid volume ≥ **4.0** (NQ) or **3.0** (ES)
- **Short setup:** at bar **high**, bid volume / ask volume ≥ **4.0** (NQ) or **3.0** (ES)

This is the footprint signature of passive size sitting at the level eating aggressive flow.

### C3 — Heavy delta, no progress (the absorption bar)

The bar itself shows aggression that failed to move price:

- **Volume:** bar volume ≥ 1.5× the 20-bar rolling average (regime-adaptive)
- **Delta:** |bar delta| ≥ 70% of bar volume (one-sided aggression)
- **Structure:** body closes in the **opposite** ≤25% of range, **OR** rejection wick ≥ 60% of range on the aggression side

Buyers / sellers came hard and couldn't lift / drop price. This is the classic absorption signature.

### C4 — CVD divergence (either form qualifies)

Order-flow disagreement between price and cumulative delta:

- **Classic divergence:** price prints a new HH/LL vs prior 5–10 bars; CVD does **not** confirm
- **Hidden divergence:** CVD prints a new high/low; price does **not** confirm

Either is valid. Hidden divergence catches stealth accumulation that classic divergence misses (CVD pushing while price holds = passive absorbers winning quietly).

### C5 — Trigger bar (sequential confirmation)

The bar **after** the absorption bar must:

- Close back through the **midpoint** of the absorption bar in the fade direction, **AND**
- Show a delta flip: trigger bar's delta sign is opposite the absorption bar's delta sign

Midpoint reclaim alone can happen on weak retraces. Adding the delta flip ensures initiative has actually changed hands. Both must be true.

---

## Entry / stop / targets

| Element | Rule |
|---|---|
| **Entry** | Market on close of the trigger bar (C5) |
| **Stop** | 1 tick beyond the wick of the absorption bar |
| **TP1** | **1R** → close 50%, move stop to breakeven |
| **TP2** | Session POC / opposite VWAP band / next HVN — whichever hits first |
| **Time stop** | If 5 minutes pass without TP1, exit at market |
| **Hard exit** | Delta flips against position on the 233-tick chart for 2+ consecutive bars → close 100% |

---

## Risk rules (non-negotiable)

| Rule | Value |
|---|---|
| Risk per trade | 0.25% – 0.5% of account |
| Daily loss limit | −2R or −1.5% account → stop trading |
| Daily profit lock | +3R → reduce size 50% or stop |
| Max trades per session | 3–5 A+ setups (5/5), not 30 |
| Min R:R | 1:2 always |
| Sessions | NY Open 09:30–11:00 ET · London/NY Overlap 08:00–10:00 ET · NY PM 13:30–15:00 ET |
| Skip windows | Lunch 11:30–13:30 ET (hard block) · First 5 min of FOMC / CPI / NFP / PMI |
| One per level | One AF setup per level, ever. If it fails, the level failed. Move on. |

---

## Numbered example (NQ)

```
Level: Prior day low @ 21,082.25
233-tick absorption bar prints:
  - Range:   21,082.25 → 21,084.50 (9 ticks)
  - Volume:  3,800 (avg 2,400)             ✓ 1.5x+
  - Delta:   −2,750 (72% of vol)           ✓ heavy selling
  - Close:   21,084.00 (top 22% of range)  ✓ no progress
  - Lower wick: 6 ticks                     ✓ rejection
  - Cluster at 21,082.25 low:
     ask vol 1,420 / bid vol 320           ✓ 4.4:1 ask absorption
  - CVD:     prior swing low @ −12,400,
             this bar dips to −12,650      ✓ classic divergence
                                            (price held, CVD extended — hidden form)

Trigger bar (next 233-tick bar):
  - Close: 21,083.75 (above absorption mid 21,083.38)  ✓ midpoint reclaim
  - Delta: +1,250                                       ✓ flip vs absorption's −2,750

ENTRY: Long @ 21,083.75
STOP:  21,082.00 (1 tick below absorption low) → 7 tick risk = $35/contract on MNQ
TP1:   21,085.50 (1R) → close half
TP2:   Session VWAP @ 21,094.00 → ~25 tick gain on remainder = ~3.5R total
```

---

## Common mistakes to avoid

1. **Treating the score as the strategy.** The 0–5 score is feedback. The strategy is the 5 rules. A score of 5 with C1 forced (the level wasn't really there) is still a no-trade.
2. **Front-running the trigger bar.** The trigger bar IS the edge. Wait for the close. Anticipating C5 destroys the win rate.
3. **Trading at every VWAP touch.** VWAP proximity counts as a level only when it's the *only* nearby reference. If price is mid-range between PDH and PDL, "near VWAP" doesn't save it.
4. **Ignoring the 4:1 / 3:1 instrument calibration.** Running 3:1 on NQ produces noise. Running 4:1 on ES misses real setups. Check your indicator settings per instrument.
5. **Skipping the time stop.** The 5-minute exit is a real edge contributor. Trades that haven't worked in 5 minutes usually aren't going to.
6. **One bad bar = thesis change.** If the absorption wick gets violated, your read was wrong. Take the loss clean. Do not move the stop.
7. **Re-entering after a stop-out at the same level.** One AF setup per level. The level failed. Move on.

---

## Why this works (research basis)

- **Stacked imbalances** show diagonal aggression where market orders eat 3+ price levels in a row — a documented signature of institutional participation. Source: [ATAS — Trading by levels with the Big Trades, Stacked Imbalance and Speed of Tape indicators](https://atas.net/blog/trading-by-levels-with-the-big-trades-stacked-imbalance-and-speed-of-tape-indicators/).
- **Absorption + CVD divergence** is one of the more reliable reversal signals because aggressive market orders are being eaten by passive limit orders — a larger player is taking the other side. Sources: [TradingView CVD Pro: Absorption, Exhaustion & Divergence](https://www.tradingview.com/script/p0EgGtfv-CVD-Pro-Absorption-Exhaustion-Divergence/), [Damn Prop Firms — Fakeouts in futures: order flow strategies](https://damnpropfirms.com/blog/fakeouts-futures-order-flow-strategies).
- **VWAP + Volume Profile context** filters out a large share of bad setups by forcing trades only at meaningful institutional reference points.
- **Tick-based bars** capture microstructure without time-bar distortion; widely used by professional order-flow traders for footprint reading.

*Content from external sources was rephrased for compliance with licensing restrictions.*

---

## Honest assessment

What is **backed** by evidence:

- Order flow / footprint reading is genuinely used by prop firms and market makers
- CVD divergence at turning points is empirically observable in tick data
- VWAP is genuinely how buy-side desks benchmark execution
- Absorption at levels is a documented microstructure phenomenon

What is **not** validated:

- The specific 5-condition combination has no published backtest with statistical significance
- The 4:1 / 1.5× / 70% / 5σ thresholds are reasonable starting points, not optimised
- Win-rate numbers from order-flow blogs are marketing figures, not peer-reviewed
- v2 inherits zero validation from v1 — they are different strategies

Treat v2 as a **hypothesis to validate**. Run the [4-phase roadmap](./absorption-fade-roadmap.md) from scratch. Paper trade 30+ instances minimum. Only commit real capital after the Phase 3 micro forward-test passes.

---

## Where v2 fits in the broader plan

- **Phase 1:** Manual replay in ATAS — log 30 instances by hand on 233-tick NQ. Use the [v2 checklist](./absorption-fade-v2-checklist.md).
- **Phase 2:** [`AbsorptionFadeConfluence`](../../indicators/atas-csharp/AbsorptionFadeConfluence/README.md) indicator auto-scores C2–C5. You confirm location. Scale to 100+ instances.
- **Phase 3:** Forward-test live on micros (MNQ / MES).
- **Phase 4:** Databento + Python for multi-year robustness testing.

See the [roadmap](./absorption-fade-roadmap.md) for decision gates per phase.

## Related files

- [v2 pre-trade checklist](./absorption-fade-v2-checklist.md) — print and pin
- [4-phase validation roadmap](./absorption-fade-roadmap.md) — same gates as v1, applied fresh to v2
- [v2 ATAS indicator](../../indicators/atas-csharp/AbsorptionFadeConfluence/README.md)
- [v1 strategy](./absorption-fade-scalp.md) — superseded but kept for reference
- [v1 indicator (Scout)](../../indicators/atas-csharp/AbsorptionFadeScout/README.md) — superseded
