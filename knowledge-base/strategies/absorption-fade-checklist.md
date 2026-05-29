# Absorption Fade v1 — Pre-Trade Checklist

> **⚠ Superseded by the [v2 checklist](./absorption-fade-v2-checklist.md).** Kept for reference. v2 uses 233-tick bars, instrument-calibrated imbalance, and an additional delta-flip filter on the trigger bar.

Print this. Pin it next to your screen. **If any box is unchecked, no trade.**

---

## Before the session

- [ ] Mapped levels: prior day H/L, weekly H/L, overnight H/L, session VAH/VAL, daily POC, key HVNs
- [ ] Within session window? (NY Open 9:30–11:00 / Overlap 8:00–10:00 / NY PM 13:30–15:00 ET)
- [ ] No high-impact news in next 5 min? (FOMC, CPI, NFP, PMI)
- [ ] Account daily loss limit not yet hit? (-2R / -1.5%)
- [ ] Account daily profit lock not yet hit? (+3R)

## Setup conditions (all 5 must print)

- [ ] **#1 Location** — price tagged a *predefined* HTF level (not mid-range)
- [ ] **#2 Volume spike** — bar volume ≥ 1.5× the 20-bar average
- [ ] **#3 Heavy delta, no progress** — delta ≥ ±70% of vol AND (close in opposite 25% OR wick ≥ 60% of range)
- [ ] **#4 CVD divergence** — price made new HH/LL vs prior 5–10 bars; CVD did not confirm
- [ ] **#5 Trigger bar** — next 1m bar closed back through midpoint of the absorption bar

## Execution

- [ ] Risk on this trade ≤ 0.5% of account?
- [ ] Stop placed 1 tick beyond the absorption wick?
- [ ] TP1 = 1R marked? (close 50% there, move stop to BE)
- [ ] TP2 marked = session POC / opposite VWAP band / next HVN?
- [ ] Time-stop reminder set? (5 min without TP1 → exit)

## After the trade (win or lose)

- [ ] Logged in `backtests/absorption-fade/` (if backtest) or `journal/trades/` (if live)
- [ ] Screenshot saved (entry + exit + HTF context)
- [ ] Score recorded (1–5 conditions met)
- [ ] One thing to remember written down

---

## Hard stops — if true, walk away

- [ ] Already lost 2R today
- [ ] Already up 3R+ today (lock the win)
- [ ] Already taken 5 trades today
- [ ] Just got stopped out — don't re-enter the same level
- [ ] Feeling tilted, frustrated, or "needing" a trade
- [ ] Price is mid-range with no nearby HTF level
- [ ] Session range < 20 ticks on ES (CVD signal unreliable)
