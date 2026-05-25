# Jaysuhnt — Trading Journey

My personal repository as I work toward becoming a full-time trader.

## What's in here

| Folder | Purpose |
|---|---|
| `knowledge-base/` | Notes on strategies, concepts, and lessons learned |
| `indicators/pine-script/` | Custom TradingView indicators (Pine Script v5) |
| `indicators/atas-csharp/` | Custom ATAS indicators (C#) for futures order-flow work |
| `journal/` | Trade log, weekly reviews, psychology notes |
| `backtests/` | Strategy test results and analysis |

## Trading profile

I'm running two parallel tracks:

### Track A — TradingView / ICT-SMC (primary, current)
- **Instruments:** XAU/USD (Gold), NAS100, EUR/USD, GBP/USD
- **Style:** Scalping
- **Timeframes:** 1m / 3m / 5m
- **Sessions:** London open + New York open
- **Platform:** TradingView
- **Account:** Demo (building consistency before going live)
- **Approach:** ICT / Smart Money Concepts foundation

### Track B — ATAS / Futures order flow (research)
- **Instruments:** ES, NQ (and micros MES, MNQ)
- **Style:** Mechanical scalping with discretion on level selection
- **Timeframes:** 30s / 1m footprint, 5m context
- **Platform:** ATAS
- **Stage:** Phase 1 manual replay — see [Absorption Fade roadmap](knowledge-base/strategies/absorption-fade-roadmap.md)
- **Approach:** Order-flow (footprint, delta, CVD divergence, absorption)

## Roadmap

### Track A (TradingView / ICT-SMC)
- [x] Set up repository structure
- [ ] Killzones / sessions indicator
- [ ] ICT/SMC core concepts reference
- [ ] Liquidity indicator (equal highs/lows, swept liquidity)
- [ ] Market structure (BOS / CHoCH) indicator
- [ ] Order block detector
- [ ] Fair Value Gap (FVG) detector
- [ ] Trade journal template
- [ ] First backtested strategy

### Track B (ATAS / Futures order flow)
- [x] Strategy spec: [Absorption Fade](knowledge-base/strategies/absorption-fade-scalp.md)
- [x] Pre-trade checklist
- [x] 4-phase roadmap with decision gates
- [x] Backtest template
- [x] ATAS indicator skeleton (`AbsorptionFadeScout`)
- [ ] Phase 1: 30 manual replay instances
- [ ] Phase 2: indicator tuned and 100+ instances
- [ ] Phase 3: live forward-test on micros
- [ ] Phase 4: Databento robustness backtest

## Rules I'm building habits around

1. **Demo until consistent.** No live capital until I have a documented edge.
2. **Risk per trade fixed.** Same R on every trade until I have data.
3. **One trade at a time.** No revenge trading, no overtrading.
4. **Journal every trade.** Win or lose. The journal is the edge.
5. **Test before trade.** New strategy = backtest first, then forward-test on demo, then size up.
