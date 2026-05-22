# 5-Minute Opening Range Breakout (ORB) on NASDAQ

> **Why this strategy first?** Of every "scalping" idea I've looked at, this is the only one I can find with **peer-reviewed academic evidence** of edge on NASDAQ-linked instruments, fully mechanical rules, and a multi-year out-of-sample track record. Everything else I'm studying (ICT silver bullet, VWAP mean-reversion, etc.) is either discretionary, under-tested, or both. So I'm starting here.

**TL;DR** — At 9:30 a.m. New York, the NASDAQ open prints a 5-minute candle. If the next candle breaks above its high, I go long. If it breaks below its low, I go short. Stop at the opposite end of the 5-minute candle. Targets are scaled, with the rest closed at the bell. That's it. The edge is in the discipline, the timing window, and the instrument selection — not in any indicator.

---

## 1. Why this strategy is "proven"

Three peer-reviewed working papers by Carlo Zarattini, Andrew Aziz and co-authors, hosted on SSRN, document the edge:

- **Zarattini & Aziz (2023)** — *Can Day Trading Really Be Profitable?* Backtests a 5-minute ORB on QQQ from 2016 to early 2023 with realistic commissions. The active portfolio produced an annualized alpha of ~33% net of costs versus a passive QQQ benchmark. ([SSRN paper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4416622))
- **Zarattini, Barbon & Aziz (2024)** — *A Profitable Day Trading Strategy For The U.S. Equity Market.* Extends the ORB to a daily-curated universe of "Stocks in Play" (today's most volatile, gapping, news-driven names). The top-20 portfolio reported ~1,600% net return and Sharpe ~2.81. ([SSRN paper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4729284))
- **Aziz & Zarattini (2024)** — Follow-up applying the same mechanics on **TQQQ** (the 3x leveraged NASDAQ-100 ETF). Reported a ~1,484% return versus ~169% for buy-and-hold QQQ over the test window. ([SSRN paper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4898296))

A rebuttal that I take seriously: *Backtests Not Signals* re-ran the math and got a more modest ~35% win rate, profitable but with smaller edge once realistic friction is layered on. ([Substack](https://backtestsnotsignals.substack.com/p/improving-the-opening-range-breakout)) That's actually fine — a 35% win rate with a >2R average winner is still a positive-expectancy system.

What this body of work tells me:

- The edge is **real but not magical**. It compounds because it trades often, sizes properly, and gets out of the way when it's wrong.
- Performance is **path-dependent on volatility**. The strategy did poorly in low-volatility 2017 and 2024 H1; it did extremely well in 2020, 2022, and 2023.
- **Leverage scales the edge but also the drawdowns.** TQQQ amplified returns and amplified the worst day too.

> Compliance note: figures in this section are paraphrased from the cited papers. Numbers will not match dollar-for-dollar across summaries because the papers test slightly different windows, costs, and universes. Always read the source PDF before quoting in a journal entry.

---

## 2. Pick your instrument

The original papers test **QQQ** (the NASDAQ-100 ETF) and **TQQQ** (3x leveraged). I don't trade US-listed ETFs, so I need an equivalent. The mapping I'm using:

| Vehicle | What it is | Why I'd pick it | Why I might not |
|---|---|---|---|
| **NAS100 CFD** | Broker-quoted NASDAQ-100 index | Tradable from my account, decimal pricing, runs 23h | Spread is wider than NQ; broker-dependent execution |
| **NQ futures** (CME) | E-mini NASDAQ-100 futures | Tightest spread, real depth, used in most public ORB backtests | Contract size is large; needs a futures-enabled broker |
| **MNQ futures** | Micro E-mini, 1/10th of NQ | Right-sized for a small/funded account | Slightly worse fill quality than NQ |
| **QQQ** | Cash ETF | The instrument the papers actually test | US equity account required; only trades 9:30–16:00 ET |
| **TQQQ** | 3x leveraged QQQ | Where the paper's headline numbers come from | Decay risk over multi-day holds (not relevant intraday); margin rules |

**My choice for now:** NAS100 on demo for journal entries, while I learn the mechanics. When I move to a funded prop account, the same ruleset transfers to **MNQ** with no logical changes — only the tick value changes.

---

## 3. The mechanical ruleset

This is the version I will trade, written so that a script could execute it without me. I'm going to call this **"ORB-5"** in my journal.

### 3.1. Session and time

- **Reference timezone:** America/New_York (ET).
- **Opening Range (OR):** the high and low of the candle from **09:30:00 to 09:34:59 ET**. This is the cash-equity open. NQ trades 23h but the 9:30 ET open is the only one that matters for this strategy because that's when QQQ liquidity arrives.
- **Trade window:** entries allowed from **09:35 ET to 11:30 ET**. After 11:30, no new entries.
- **Hard close:** all positions flat by **15:55 ET** regardless of P&L.

### 3.2. Direction

I trade only the **first** breakout of the OR per day:

- If the 09:35 candle (or any subsequent candle inside the trade window) **closes above** the OR high → **long**.
- If it **closes below** the OR low → **short**.
- If it does neither, I do nothing and the day is a no-trade.

Some published variants enter on the *touch* of the OR boundary rather than waiting for a close. I'll only trade the close-confirmation version because:

1. It eliminates one source of noise (false wicks).
2. It's the version most consistent with the Zarattini/Aziz rules I can verify.

### 3.3. Stop loss

- **Long:** stop at the **OR low minus 1 tick** (or 1 pip on NAS100 CFD).
- **Short:** stop at the **OR high plus 1 tick**.

This stop is also my risk unit (= 1R). I size the position so that the dollar distance from entry to stop equals my fixed risk per trade (see §5).

### 3.4. Targets and scaling

The papers test multiple exit schemes. The one I'm going to start with — because it best matches a "scalping" expectation while still letting winners run — is a **two-piece exit**:

| Piece | Size | Exit rule |
|---|---|---|
| TP1 | 50% of position | Limit at **+1R** |
| TP2 (runner) | 50% of position | Trail behind the **9-period EMA on the 5-min chart**, exit on EMA close-against, or hard-close at 15:55 ET, whichever first |

Once TP1 is hit, I move the runner's stop to **breakeven minus 1 tick** so the trade cannot become a loser.

The original paper uses a 10× ATR target as the TP and an end-of-day exit. I'll log both schemes in parallel during backtesting (see §7).

### 3.5. The "no-second-chance" rule

If the OR is broken, taken, and the trade hits the stop, **I do not re-enter on a second breakout in the same direction**. Reversal entries (the opposite side breaking later in the day) are also off-limits in version 1.0 of the ruleset. Why: every reversal rule I've added in spec form has nuked the win rate in informal tests, and I want to keep this clean for my first 200 logged trades.

### 3.6. Hard filters that override entries

- **No-trade days:** FOMC release days, NFP, CPI — skip the morning entirely. The OR is contaminated by the announcement.
- **OR too wide:** if the OR height is greater than **1.5× the 14-day average OR height**, skip. The stop is too wide for the day's expected range.
- **OR too narrow:** if the OR height is less than **0.4× the 14-day average OR height**, skip. The market is too compressed; breakouts in low-vol conditions have the worst hit rate per the papers.

---

## 4. Why this works (the mechanics, not the magic)

I want to be honest with myself: this is not a "secret". It works because of three structural features of the NASDAQ open, not because of any indicator setting.

1. **Concentrated overnight information.** Earnings, macro data and Asia/Europe price action all clear into a 30-second auction at 09:30 ET. The first 5 minutes of QQQ contains a disproportionate share of the day's information; once the imbalance breaks the OR, follow-through is more likely than mean-reversion. This is the same observation behind the academic literature on the "opening auction effect."
2. **Asymmetric payoff structure.** The stop is the *full width* of the OR, but the runner can capture a multi-R move on a trend day. Even at a 35–40% hit rate, a 2R+ average winner is positive expectancy.
3. **Filtering of dead days.** The OR-too-narrow filter and the no-news filter remove most of the days where the strategy historically bleeds. This is the unsexy work that turns a marginal edge into a real one.

---

## 5. Risk and position sizing

The papers assume you size to a fixed dollar risk per trade. I'm going to do the same.

- **Risk per trade:** 0.5% of account equity. I will not exceed 1% even on A+ setups.
- **Daily loss limit:** 2R. After two full stops, I'm done for the day. This is non-negotiable and matches the prop-firm risk culture I'm preparing for.
- **Weekly loss limit:** 5R. After a -5R week I take Friday off and review the journal before Monday.
- **Position sizing formula on NAS100 CFD:**
  - `Lot size = (Equity × 0.005) / (StopDistanceInPoints × $/point)`
  - On NAS100 with most CFD brokers, $1/point per 0.1 lot. So a 50-point OR on a $5,000 account: `$25 risk / (50 × $1) = 0.5 lots` ... which is too big. I'd reduce to micro-lot if my broker supports it, or skip the day.
- **Position sizing formula on MNQ:**
  - 1 MNQ tick = $0.50, 1 MNQ point = $2.
  - On a $50k funded MNQ account, 0.5% = $250 risk. Stop = 60 points → max **2 MNQ contracts** (`$240 risk`).

I'll add a sizing calculator spreadsheet to the repo when I move to live.

---

## 6. Performance expectations (what to actually expect)

These are the rough ranges I should expect month to month, drawn from the cited papers and my own preliminary look. I'm writing them down so future-me doesn't blow up the strategy after a normal losing streak.

| Metric | Realistic range | Notes |
|---|---|---|
| Win rate | 35% – 45% | Below the 50% mark — most days are losers or no-trades |
| Avg winner / Avg loser (R) | 1.8 – 2.5 | The edge is in the size of winners, not their frequency |
| Trades per month | 12 – 18 | After all filters; some weeks have zero trades |
| Worst losing streak (in 1y) | 6 – 8 trades | This *will* happen, plan for it |
| Annual return on a properly sized account | 25% – 60% | Highly volatility-regime dependent |
| Worst monthly drawdown | -8% – -12% | At 0.5% risk per trade |

If my live numbers fall **outside** these bands after 50+ trades, the strategy is being executed wrong, or the regime has changed enough to require a re-test. Either way: stop, journal, fix, then continue.

---

## 7. How I'll backtest before risking money

I cannot trust someone else's backtest. I'm going to reproduce the result on my own data, my own platform, with my own costs.

### 7.1. Data

- **Source:** TradingView 5-minute NQ continuous contract, plus NAS100 from my broker for spread/cost calibration.
- **Window:** 2018-01-01 to today. That gives me low-vol (2018–2019), crisis (2020), trend (2021), bear (2022), recovery (2023–2024), and the current regime.
- **Sample size goal:** 800+ trading days, expecting roughly 250–400 actual trades after filters.

### 7.2. Tooling

- **Phase 1 — manual sim:** Pine Script strategy on TradingView with the rules from §3, "use bar magnifier" enabled, and broker fees set to 1 NQ tick round-trip + 1 tick slippage. (See `indicators/pine-script/` for in-progress scripts.)
- **Phase 2 — Python:** if Phase 1 looks good, I port to Python with `pandas` + `vectorbt` for parameter sweeps over OR length (3/5/15/30 min), risk per trade (0.25% / 0.5% / 1%), and TP1 multiples (0.5R / 1R / 1.5R).
- **Phase 3 — forward test:** 60 trading days on demo with the chosen parameters, journaled in `journal/` using the existing template.

### 7.3. What I'm looking for in the backtest output

- **Net of costs Sharpe ≥ 1.0** on the full window.
- **No single 6-month period with a profit factor below 1.0.** If one period collapses, the strategy is fragile.
- **Trade count ≥ 200** so the result is not a fluke.
- **Reasonable parameter stability** — the win rate should not crater when I shift the OR length from 5 to 15 minutes. If it does, I've curve-fitted.

---

## 8. Variants I'll explore *after* the base version is profitable on paper

Order of priority, only one change at a time.

1. **Stocks in Play overlay (Zarattini 2024).** Each morning, screen for stocks with: (a) gap > 2%, (b) pre-market volume > 5× average, (c) catalyst (earnings, news). Apply ORB-5 to the top 5. This is where the published returns explode.
2. **TQQQ leverage equivalent.** On NAS100, this maps to running 3× the position size with a 3× wider stop in account-equity terms — *not* literally trading a leveraged product. The math has to be done carefully so the stop in points stays the same; only the dollar risk scales.
3. **15-minute OR.** Less noisy, fewer entries, supposedly more robust on NQ in 2024–2025. I'll test 5 vs 15 head-to-head.
4. **VWAP filter.** Only take longs above session VWAP, only take shorts below. The Pine Script community claims this lifts win rate by 3–5 points; I want to verify on my own data.

Anything outside this list goes back to the ICT/SMC notes until I have enough data to upgrade it.

---

## 9. How this fits with the ICT/SMC concepts I'm studying

I'm not abandoning the ICT framework — I'm using it as **a lens, not a rulebook**. The ORB and ICT views of the open are surprisingly compatible:

- The **9:30 OR high/low** in ORB is structurally a liquidity pool. The first move out of the OR that fails and reverses is, in ICT vocabulary, a **liquidity sweep** that often precedes a Silver Bullet entry between 10:00 and 11:00 ET.
- The **Silver Bullet model (10:00–11:00 ET)** can be viewed as the "second chance" trade I explicitly disallow in ORB-5. I'll keep ORB-5 mechanical and trade the Silver Bullet only on a separate journaled experiment, never on the same day as an ORB stop-out.
- A clean ORB-5 long that runs to TP2 will, in most cases, leave a **fair value gap** below it. That FVG becomes the level where future-me looks for re-entry on a pullback — but only if I've built a separate, equally rigorous ruleset for that.

The discipline here: **don't mix two strategies on the same trade.** Each setup has its own rule, its own R-target, its own journal tag.

---

## 10. The honest list of ways this can fail

I'm writing these down now so I can't pretend later that I didn't see them coming.

1. **Regime change.** If implied volatility on QQQ collapses for 6+ months (think 2017), trade frequency drops to almost zero and the strategy looks "broken". It isn't — it's just waiting.
2. **Slippage on retail brokers.** The papers assume institutional fills. NAS100 CFDs from a retail broker can slip 2–3 points on a fast breakout, which eats meaningfully into the edge.
3. **Curve fitting.** It's tempting to optimize OR length, TP, EMA period until the equity curve is gorgeous. That's how you build a strategy that loses money live. Lock parameters before forward-testing.
4. **Discipline drift.** The "no second chance" rule will feel stupid on a day where the second breakout would have been the winner. Trade it anyway. If I cherry-pick, I'm no longer running a mechanical strategy — I'm gambling with extra steps.
5. **Catalysts I didn't filter.** A surprise FOMC speaker, an unscheduled tariff headline, an outage at a top-5 NASDAQ name — the OR is meaningless on those days. When in doubt, skip.

---

## 11. Sources and further reading

Primary academic sources (paraphrased; read the PDFs before citing in a trade journal):

- Zarattini, C., & Aziz, A. (2023). *Can Day Trading Really Be Profitable?* SSRN. — [paper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4416622)
- Zarattini, C., Barbon, A., & Aziz, A. (2024). *A Profitable Day Trading Strategy For The U.S. Equity Market.* SSRN. — [paper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4729284)
- Aziz, A., & Zarattini, C. (2024). *Can Day Trading Really Be Profitable? (TQQQ extension).* SSRN. — [paper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4898296)

Practitioner write-ups and replications:

- Concretum Group summary of the Zarattini/Aziz paper — [post](https://concretumgroup.com/can-day-trading-really-be-profitable/)
- The Robust Trader replication notes — [post](https://therobusttrader.com/can-day-trading-really-be-profitable-rules-backtest-statistics-performance-analysis/)
- CXO Advisory independent test of the QQQ 5-min ORB — [post](https://cxoadvisory.com/technical-trading/day-trading-with-an-opening-range-breakout-strategy)
- *Backtests Not Signals* critical replication — [post](https://backtestsnotsignals.substack.com/p/improving-the-opening-range-breakout)
- QuantConnect open-source implementation of "ORB for Stocks in Play" — [research](https://www.quantconnect.com/research/18444/opening-range-breakout-for-stocks-in-play/)

> *Content was rephrased for compliance with licensing restrictions. All numbers and rules above are my best-faith summary of what the papers and replications report; verify against the original sources before trading real money.*

---

## 12. Next actions for me

- [x] Build the Pine Script version of ORB-5 in [`indicators/pine-script/orb-5.pine`](../../indicators/pine-script/orb-5.pine). Apply to a 5-min NQ chart and confirm that the OR box, breakout entries, SL, TP1 and EMA trail line up with this document's ruleset.
- [ ] Run a manual backtest on 2024 NQ data (~250 days) and record win rate / avg R / max drawdown in a new file under `backtests/`.
- [ ] Paper-trade ORB-5 for 30 sessions, journaling each one with the existing `journal/_template.md`.
- [ ] If the 30-session paper test holds together, draft `02-orb-5-stocks-in-play.md` with the multi-stock variant.
- [ ] Only after all of the above: consider live, micro-size, on MNQ.
