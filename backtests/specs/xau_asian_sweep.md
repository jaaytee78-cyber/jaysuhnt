# XAU Asian Sweep + Reversal — Strategy Spec

**Status:** draft, not yet implemented
**Last updated:** 2026-05-21
**Lineage:** picks up after PSS validation showed PSS doesn't fit XAU. See `indicators/pine-script/CHANGELOG.md` for that story. The infrastructure built there (`backtests/pss/`) is reused for this strategy as `backtests/asw/`.

---

## 1. Why this strategy specifically

PSS failed on XAU because it imported assumptions from equities trading: clear daily anchors, real exchange volume, mean reversion to session VWAP. None of those describe XAU's structure. This strategy is built on assumptions that **do** describe XAU:

| XAU trait | Strategy implication |
|---|---|
| 24-hour market with three liquidity centres (Asia, London, NY) | Use sessions explicitly; trade where flow is, not "always" |
| Stops accumulate at well-known levels (Asia high/low, prev-day H/L) | Define a level structurally important to XAU traders |
| Institutional flow concentrates at session opens | Time the entries, don't let them fire any minute |
| News and macro flow drive trend; ranges are mean-reverting | Specifically target intra-session range failures, not trend-following |

This is a **liquidity-sweep + reversal** strategy. ICT/SMC tradition calls it "Asia raid + London reversal" or "sweep + MSS". The setup is widely documented and structurally explainable, not a pattern that someone happened to find.

## 2. Hypothesis (what we are testing)

> During the Asian session (low liquidity, range-bound), price establishes a high (AH) and low (AL). When London opens (07:00 UTC), institutional flow targets one of these levels, sweeps it (price goes beyond, taking out resting stops), and reverses back into the range. Entering after the reclaim of the swept level offers an asymmetric risk:reward setup, because the stop is the sweep extreme (small distance) and the target is the opposite end of the Asian range or beyond.

### What would falsify this

| Falsifier | Verdict |
|---|---|
| Asia ranges get swept on >90% of days regardless of London bias | Pattern is too common to be a real signal |
| Reversals after sweep are <50% probable | The "smart money reversal" thesis is wrong on XAU |
| Expectancy is negative after costs | Even if directional bias exists, the structure can't capture it |
| Performance is identical regardless of which session sweeps | The session-anchoring assumption was decorative |

We will check each of these in the validation report. If any of the first three are true, this strategy gets killed, same way PSS was.

## 3. Sessions (UTC, no DST handling)

These windows are deliberately conservative and standard. Each is half-open `[start, end)`:

| Session | UTC range | Notes |
|---|---|---|
| Asia | `22:00` (prev day) → `06:00` | 8 hours. Dominated by Tokyo/Sydney; lowest XAU volatility window. |
| London | `07:00` → `12:00` | Reversal entries fire here. London open is `08:00` but pre-market is included for early sweeps. |
| NY | `12:00` → `17:00` | Late-window sweeps and reversal entries. |
| Trade window cutoff | `17:00` | After this, no new entries. Open positions ride to 21:00 hard close. |

If a sweep hasn't occurred by `17:00` UTC, no trade that day. If a sweep occurred but no reclaim by `17:00`, no trade.

### Definition of "Asia high" and "Asia low"

```
AH(today) = max(high) over bars timestamped 22:00 yesterday <= ts < 06:00 today (UTC)
AL(today) = min(low)  over the same window
```

Both are known and frozen at `06:00` UTC. They are causal: any rule executed after `06:00` may use them safely.

## 4. The setup — long (Asia low sweep + reclaim)

### Trigger sequence

1. **Range definition** — `AH(today)` and `AL(today)` known at `06:00` UTC.
2. **Sweep** — bar after `06:00` makes a `low < AL`. Specifically: `low < AL - sweep_buffer`, where `sweep_buffer` defaults to `0` (any wick below counts).
3. **Reclaim** — within `reclaim_window_bars` after the sweep, a 5m bar **closes** with `close > AL`.
4. **Entry** — at the close of the reclaim bar.
5. **Stop** — at `sweep_low - stop_buffer * ATR(14)`, where `sweep_low` is the lowest low seen between sweep start and reclaim.
6. **Target** — at `AH` (the Asian range high). Alternative variant: `entry + rr * (entry - stop)`. We test both.
7. **Time stop** — exit at the close of the bar at `21:00` UTC if neither stop nor target hit.
8. **Cooldown** — at most one long-side trade per day. After the first long fires, no more longs that day even if the price re-sweeps.

### Mirror — short (Asia high sweep + reclaim)

Same logic, mirrored:
- Sweep: `high > AH + sweep_buffer`
- Reclaim: 5m close `< AH`
- Stop: `sweep_high + stop_buffer * ATR(14)`
- Target: `AL`

One short per day cap, separate from the long cap.

### Trade direction limits

- Up to 2 trades per day total: one long-setup, one short-setup, in either order.
- If both setups complete on the same day, both fire (no priority rule).

## 5. Parameters (the values to fix BEFORE running)

These are the values written into the strategy. **They are not optimised; they are picked from defaults that are standard in the ICT literature and have face validity.** Optimization, if any, only happens on out-of-sample data after in-sample validation confirms the hypothesis works.

| Param | Value | Reasoning |
|---|---|---|
| `asia_start_utc` | 22:00 | Standard Asia open in retail trading literature |
| `asia_end_utc` | 06:00 | Hour before London pre-market |
| `trade_cutoff_utc` | 17:00 | After NY power hour, flow concentration drops |
| `hard_close_utc` | 21:00 | NY cash close; positions exit regardless |
| `sweep_buffer` | 0.0 | Any wick beyond AL/AH counts as a sweep |
| `reclaim_window_bars` | 48 | 4 hours on 5m. Sweep must reclaim within this many bars or void |
| `stop_buffer` (× ATR) | 0.5 | Stop is 0.5×ATR below sweep low |
| `target_mode` | `"asian_range"` | Target = AH (long) / AL (short). We also test `"fixed_rr"` with `rr = 2.0` |
| `atr_period` | 14 | Standard. Same as PSS. |
| `min_asian_range_atr` | 1.0 | Skip days where AH-AL < 1×ATR(14) — range too small to be meaningful |

### Realistic execution costs (carry over from PSS validation)

| | Value (USD) |
|---|---|
| `half_spread` | 0.18 |
| `stop_slippage` | 0.10 |

## 6. What we explicitly do NOT do

| Will not | Why |
|---|---|
| Use CVD or any volume-derived signal | Polygon spot XAU volume is contributed-bank tick count, not real |
| Use VWAP bands | XAU does not mean-revert to session VWAP on intraday timescales |
| Use a confluence-score system | Single rule = transparent. If it doesn't work as one rule, it doesn't work |
| Optimize parameters before OOS validation | This is the trap PSS fell into. We don't repeat it |
| Run on synthetic data | Same trap |
| Trust the `target = AH` choice without comparing to fixed RR | We test both target modes side-by-side and pick |

## 7. Validation plan

### Reuse from PSS validation

Same harness, same realism, same report shape. Concretely:

```
backtests/asw/                     # new package, parallel to backtests/pss/
  __init__.py
  params.py                        # AswParams dataclass, mirrors PSSParams
  indicators.py                    # session_id, asia_session_levels, pine_atr (re-import OK)
  signals.py                       # sweep + reclaim detection
  backtest.py                      # NEW: needs different exit logic (target=AH, not RR-fixed)
                                   # but spread/slippage/no-drop is identical
  report.py                        # mostly reused from PSS report.py
backtests/run_asw_validation.py    # entry point
backtests/reports/asw_validation_xau_<date>.md
```

### Splits

- **Total window:** 2024-05-21 to 2026-05-20 (2 years, 5m, Polygon `C:XAUUSD`, already cached)
- **In-sample window:** 2024-05-21 to 2025-11-20 (18 months)
- **Out-of-sample (held out, never peeked):** 2025-11-21 to 2026-05-20 (6 months)

### Stage 1 — In-sample only

Run the strategy as specified above on the 18-month IS window. Generate the report. **Do not change parameters based on what we see.** Just observe.

### Stage 2 — Run on OOS untouched

Run the same parameters on the held-out 6 months. Generate a separate report.

### Stage 3 — Compare

Side-by-side IS vs OOS report. Specifically, the strategy passes if:

- IS has `coin_flip_p < 0.20` (some signal at all)
- OOS has `coin_flip_p < 0.20` AND OOS expectancy ≥ 70% of IS expectancy
- Sample size ≥ 50 trades on each window
- No single month dominates total R by >40%

If OOS performance collapses, the strategy is curve-fit and dies here.

If OOS holds up, we have a candidate worth forward-testing on demo. Optimization (if any) gets done with rolling walk-forward in a Stage 4 we don't even plan yet.

## 8. What "good" looks like at the end of validation

| Metric | Threshold |
|---|---|
| Trade count over 2y | ≥ 100 |
| Win rate (target = AH) | ≥ 40% (because 1:1.5 average RR is geometric typical) |
| Expectancy per trade | ≥ +0.20R |
| Profit factor | ≥ 1.30 |
| Max drawdown | ≤ 15R |
| Longest losing streak | ≤ 8 |
| OOS / IS expectancy ratio | ≥ 0.70 |
| Coin-flip P(≥ strategy) | < 0.10 on both IS and OOS |

If we get there, this strategy is worth taking to demo. If we don't, this is another data point and we move on without regret — same way we did with PSS.

## 9. What "kill it" looks like

Any of these and we close out the experiment:

- IS expectancy < 0 → strategy doesn't even work where we built it
- OOS expectancy < IS expectancy × 0.5 → curve-fit
- < 50 trades over 2 years → too rare to be useful
- Drawdown > 25R → unsurvivable for retail position sizing
- Win-rate-by-month is wildly inconsistent (e.g. 4 months at 0%, 4 at 70%) → market-regime dependent in a way we can't filter for

## 10. Open questions to resolve before coding

1. **Asia session start: 22:00 UTC or 23:00 UTC?** Some sources use 23:00 because Sydney close to Tokyo open is the "real" Asia. We default to 22:00 here for inclusivity, but worth a sensitivity ablation.
2. **Reclaim definition: close-only, or include break of 5m high after sweep low?** Default is close-only (cleaner, fewer false reclaims).
3. **Same-day re-sweep:** if AL is swept, reclaimed, trade fires, then later AL is swept again — do we take a second long? Default: NO, one per direction per day.
4. **Pre-news filter:** scheduled releases (NFP, FOMC, CPI) move XAU dramatically. Do we skip days with high-impact events? Default: NO for now (adding it would require a calendar source and could be a later refinement). Validation will tell us if news days are toxic.

These all have defaults above. If anything looks wrong, we change it before code is written.
