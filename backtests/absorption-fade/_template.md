# AF Instance — YYYY-MM-DD — ES — #NN

## Context
- **Date / time (ET):**
- **Instrument:** ES / NQ / MES / MNQ
- **Session window:** NY Open / Overlap / NY PM / (other — flag for review)
- **Phase:** 1 (manual replay) / 2 (indicator) / 3 (live)
- **Replay or live:** Replay / Live

## Condition checks (mark each)

| # | Condition | Pass? | Notes / values |
|---|---|---|---|
| 1 | Location — predefined HTF level | ☐ Y / ☐ N | Which level? (PDH, weekly H, VAH, etc.) Price: |
| 2 | Volume ≥ 1.5× 20-bar avg | ☐ Y / ☐ N | Bar vol: ___ / Avg: ___ |
| 3 | Delta ≥ ±70% AND (close ≤25% opp OR wick ≥60%) | ☐ Y / ☐ N | Delta: ___ / Close %: ___ / Wick %: ___ |
| 4 | CVD divergence vs prior 5–10 bars | ☐ Y / ☐ N | Price HH/LL: ___ / CVD level vs prior: ___ |
| 5 | Trigger bar closed back through midpoint | ☐ Y / ☐ N | Trigger close: ___ / Mid: ___ |

**Score: ___ / 5**
**Trade taken? ** ☐ Yes (5/5) / ☐ No (filtered, why: ____)

## Trade details (only if score = 5)

- **Direction:** Long / Short
- **Entry price:**
- **Stop price:**
- **Stop distance (ticks):**
- **Risk in $:**  (per micro: $1.25/tick on MES, $0.50/tick on MNQ)
- **TP1 price:** (1R)
- **TP2 price:** (target type: POC / VWAP band / HVN — specify: )

## Outcome

- **TP1 hit?** ☐ Y / ☐ N
- **TP2 hit?** ☐ Y / ☐ N
- **Time-stop exit?** ☐ Y / ☐ N (after 5 min)
- **Stopped out?** ☐ Y / ☐ N
- **Exit price (final):**
- **Result in R:**
- **Result in $:**
- **Hold time:**

## Screenshots
- Setup bar:
- Trigger bar:
- Exit:
- HTF context (5m + daily profile):

## Notes / lessons

- **What worked:**
- **What didn't:**
- **Did the level matter (was condition #1 correctly identified)?**
- **One thing to remember:**
