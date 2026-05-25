# Absorption Fade (AF) — Scalping Strategy

A mechanical order-flow scalping strategy for **NQ / ES futures** on the **ATAS** platform.

> **Heads up:** This strategy requires bid/ask split volume (footprint data) and a Cumulative Delta indicator. TradingView does **not** provide this for futures in a usable form. AF is a futures-only, ATAS-track strategy that runs in parallel to the ICT/SMC TradingView track in this repo.

---

## The mental model

Price runs into a known level. Aggressive market orders pile in expecting a breakout. Someone bigger is sitting there with limit orders, eating every print. The aggressors get filled but **price doesn't move**. They're now trapped. When they realize it and cover, the reversal you're trading is just *their* exit liquidity.

You are not predicting. You are reading a transaction.

---

## ATAS chart configuration

### Chart 1 — Execution (the chart you trade from)

- **Timeframe:** 1-minute footprint (or 30-second on NQ during high vol)
- **Footprint mode:** Bid x Ask (numbers visible on each cluster)
- **Imbalance threshold:** 300% (highlights diagonal imbalances)
- **Cluster colouring:** by Delta
- **Overlays:**
  - Session VWAP + 1σ and 2σ bands
  - Cumulative Delta (separate pane, anchored to session)
  - Volume Profile — Session (POC / VAH / VAL visible)

### Chart 2 — Context (do not trade from this, just confirm)

- **Timeframe:** 5-minute candles
- Session VWAP
- Daily Volume Profile (last 5 days, POC + value areas)
- Prior day H/L, weekly H/L plotted

### Chart 3 — DOM (optional but recommended)

- Watch for pulled liquidity at your level when you're about to enter.

---

## Mechanical entry — 5 conditions, all required

You do not take the trade unless **all five** print. No exceptions.

| # | Condition | What you're looking at |
|---|---|---|
| 1 | **Location** | Price tags a *predefined* level: prior day H/L, weekly H/L, session VAH/VAL, overnight H/L, or HVN on daily profile |
| 2 | **Volume spike** | Bar volume ≥ 1.5× the 20-bar average |
| 3 | **Heavy delta, no progress** | Bar delta ≥ ±70% of bar volume **AND** body closes in the opposite ≤25% of range, **OR** wick ≥ 60% of range |
| 4 | **CVD divergence** | Price prints a new HH/LL vs prior 5–10 bars; CVD does **not** confirm |
| 5 | **Trigger bar** | Next 1m bar closes *back through* the midpoint of the absorption bar |

### Entry / stop / targets

- **Entry:** Market on close of the trigger bar (condition 5)
- **Stop:** 1 tick beyond the wick of the absorption bar
- **TP1:** 1R → close 50%, move stop to breakeven
- **TP2:** Session POC, opposite VWAP band, or next HVN (whichever hits first)
- **Time stop:** If 5 minutes pass without TP1, exit at market

---

## Numbered example (ES)

```
Level: Prior day high @ 5482.25
1-min absorption bar prints:
  - Volume:   4,200 (avg 2,100)            ✓ 1.5x+
  - Delta:    +2,950 (70% of vol)          ✓ heavy buying
  - Range:    5482.25 → 5483.50 (5 ticks)
  - Close:    5482.50 (bottom 20%)         ✓ no progress
  - Upper wick: 4 ticks                     ✓ rejection
  - CVD:      prior swing high @ +8,400,
              this bar peaks at +7,900     ✓ divergence

Trigger bar (next 1m): closes 5481.75 (below absorption mid 5482.88) ✓

ENTRY: Short @ 5481.75
STOP:  5483.75 (1 tick above wick)  → 8 tick risk = $100/contract
TP1:   5479.75 (1R)                 → close half
TP2:   Session POC @ 5476.00        → ~24 tick gain on remainder = ~3R total
```

---

## Risk rules (non-negotiable)

- **Risk per trade:** 0.25% – 0.5% of account
- **Daily loss limit:** 2R or 1.5% — stop trading
- **Daily profit lock:** at +3R, reduce size 50% or stop
- **Max trades per session:** 3–5 A+ setups, not 30
- **Sessions only:**
  - NY Open (9:30 – 11:00 ET)
  - London / NY overlap (8:00 – 10:00 ET)
  - NY PM (1:30 – 3:00 ET)
  - **Skip lunch** (11:30 – 1:00 ET)
- **No trades** during FOMC, CPI, NFP for the first 5 minutes
- **One AF setup per level.** If it fails, the level failed. Move on.

---

## Common mistakes to avoid

1. **Trading absorption mid-range.** Only at predefined HTF levels. Mid-range absorption is noise.
2. **Front-running the trigger bar.** Wait for the close. The trigger bar IS the edge.
3. **Ignoring CVD on small ranges.** If session range < 20 ticks (ES), CVD signal is unreliable. Skip.
4. **Re-entering after a stop-out.** One AF setup per level, ever.
5. **Trading during news.** Absorption signatures lie during news prints.
6. **NQ on tight stops.** NQ wicks are violent. Use 12+ tick stops or stick to ES until consistent.

---

## Why this works (research basis)

- **Stacked imbalances** show diagonal aggression where market orders eat 3+ price levels in a row — a documented signature of institutional participation. Source: [ATAS — Trading by levels with the Big Trades, Stacked Imbalance and Speed of Tape indicators](https://atas.net/blog/trading-by-levels-with-the-big-trades-stacked-imbalance-and-speed-of-tape-indicators/).
- **Absorption + CVD divergence** is one of the more reliable reversal signals because aggressive market orders are being eaten by passive limit orders — i.e. a larger player is taking the other side. Sources: [TradingView CVD Pro: Absorption, Exhaustion & Divergence](https://www.tradingview.com/script/p0EgGtfv-CVD-Pro-Absorption-Exhaustion-Divergence/), [Damn Prop Firms — Fakeouts in futures: order flow strategies](https://damnpropfirms.com/blog/fakeouts-futures-order-flow-strategies).
- **VWAP + Volume Profile context** filters out a large share of bad setups by forcing trades only at meaningful levels.

*Content from external sources was rephrased for compliance with licensing restrictions.*

---

## Where this fits in the broader plan

- **Phase 1:** Manual replay in ATAS — log 30 instances by hand.
- **Phase 2:** Custom ATAS indicator (`AbsorptionFadeScout`) auto-detects setups so you can scale to 100+ instances.
- **Phase 3:** Forward-test live on micros (MES / MNQ).
- **Phase 4:** Databento + Python for multi-year robustness testing.

See [`absorption-fade-roadmap.md`](./absorption-fade-roadmap.md) for the full plan and decision gates.

## Related files

- [Pre-trade checklist](./absorption-fade-checklist.md) — single page, print and pin
- [Backtest log template](../../backtests/absorption-fade/_template.md)
- [ATAS indicator skeleton](../../indicators/atas-csharp/AbsorptionFadeScout/README.md)
