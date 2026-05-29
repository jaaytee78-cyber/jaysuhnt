# Absorption Fade v2 — Pre-Trade Checklist

Print this. Pin it next to your screen. **If any box is unchecked, no trade.**

For full strategy spec see [`absorption-fade-v2.md`](./absorption-fade-v2.md).

---

## Before the session

- [ ] Mapped levels: prior day H/L, weekly H/L, overnight H/L, session VAH/VAL, daily POC, key HVNs, VWAP ±1σ/±2σ
- [ ] Within session window? (NY Open 09:30–11:00 / Overlap 08:00–10:00 / NY PM 13:30–15:00 ET)
- [ ] No high-impact news in next 5 min? (FOMC, CPI, NFP, PMI)
- [ ] Account daily loss limit not yet hit? (−2R / −1.5%)
- [ ] Account daily profit lock not yet hit? (+3R)
- [ ] Indicator calibrated for instrument? (NQ: imbalance 4.0 · ES: imbalance 3.0)

## Setup conditions (all 5 must print)

- [ ] **C1 Location** — price tagged a *predefined* HTF level (not mid-range). Level was on the chart **before** price got there.
- [ ] **C2 Cluster imbalance at extreme** — at bar low (long) or bar high (short): ratio ≥ **4.0** on NQ / **3.0** on ES
- [ ] **C3 Heavy delta, no progress** — bar volume ≥ 1.5× 20-bar avg AND |delta| ≥ 70% of vol AND (close in opposite ≤25% OR rejection wick ≥ 60% of range)
- [ ] **C4 CVD divergence** — *either* classic (price made new HH/LL, CVD did not) *or* hidden (CVD made new high/low, price did not)
- [ ] **C5 Trigger bar** — next 233-tick bar closes back through midpoint of absorption bar **AND** trigger bar's delta sign is opposite the absorption bar's

**Indicator score must read 5/5** before you click. 4/5 is *not* a trade.

## Execution

- [ ] Risk on this trade ≤ 0.5% of account?
- [ ] Stop placed 1 tick beyond the absorption wick?
- [ ] TP1 = 1R marked? (close 50%, move stop to BE)
- [ ] TP2 marked = session POC / opposite VWAP band / next HVN?
- [ ] Time-stop reminder set? (5 min without TP1 → exit market)
- [ ] Hard-exit rule remembered? (delta flips against position for 2+ bars on 233-tick → close 100%)

## After the trade (win or lose)

- [ ] Logged in `backtests/absorption-fade/` (replay) or `journal/trades/` (live)
- [ ] Screenshot saved (entry + exit + HTF context)
- [ ] Score recorded (1–5 conditions met) + which condition was weakest if you lost
- [ ] One thing to remember written down

---

## Hard stops — if true, walk away

- [ ] Already lost 2R today
- [ ] Already up 3R+ today (lock the win)
- [ ] Already taken 5 trades today
- [ ] Just got stopped out — don't re-enter the same level (one AF setup per level)
- [ ] Feeling tilted, frustrated, or "needing" a trade
- [ ] Price is mid-range with no nearby HTF level
- [ ] Indicator score is 4/5 or below — wait for the 5th, do not fudge it
- [ ] DOM spread abnormally wide / book pulled — feed quality unreliable
- [ ] Price action erratic, no clear levels (chop)
