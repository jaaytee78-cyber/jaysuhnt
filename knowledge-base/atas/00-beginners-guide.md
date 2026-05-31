# ATAS for NQ / ES Scalping — Beginner's Guide

A plain-English, zero-jargon walkthrough from installing the software to placing your first informed trade. No experience required.

> **Scope:** This is a *platform + concepts* primer for the ATAS order-flow track (Track B). It teaches the tools. For the actual mechanical setup I'm validating, see [Absorption Fade v2](../strategies/absorption-fade-v2.md). Where this guide gives generic beginner defaults, I've flagged where my own v2 research has already improved on them — look for the **v2 upgrade** callouts.

> **Reality check, up front:** ATAS is a professional tool. It does not make you profitable by itself. The software shows you information; what you do with it depends on your understanding and discipline. Treat the first months as education, not income. Futures trading carries substantial risk of loss and is not suitable for everyone.

---

## Contents

1. [What ATAS is and why it matters](#01--what-atas-is-and-why-it-matters)
2. [Understanding the market first](#02--understanding-the-market-first)
3. [Installing and setting up](#03--installing-and-setting-up)
4. [The interface](#04--the-interface)
5. [Volume Profile — your core tool](#05--volume-profile--your-core-tool)
6. [The footprint chart](#06--the-footprint-chart)
7. [Delta — the hidden signal](#07--delta--the-hidden-signal)
8. [Configuring ATAS for ES/NQ scalping](#08--configuring-atas-for-esnq-scalping)
9. [Your first setup](#09--your-first-setup)
10. [Reading the market step by step](#10--reading-the-market-step-by-step)
11. [Common beginner mistakes](#11--common-beginner-mistakes)
12. [Learning roadmap](#12--learning-roadmap)

---

## 01 · What ATAS is and why it matters

Most traders look at a price chart and ask *"where is price going?"* ATAS lets you ask a better question: *"what are other traders actually doing right now?"*

ATAS is order-flow analysis software. A standard chart shows you a candle — a block summarising price over a period. ATAS shows you the individual trades that built that candle: who bought, who sold, at what price, in what size.

> **On the name:** Per ATAS's own about page, the product grew out of their first tool, **"Advanced Time And Sales"** — an enhanced tape that aggregated and highlighted large exchange trades. You'll also see third-party sites expand it as "Advanced Trading Analytical Software." Either way, the point is the same: it's a microscope for the tape. Source: [About ATAS](https://atas.net/about-us/).

**Simple analogy.** A regular chart is the closing fish price at the end of the market day. ATAS is every transaction — who haggled, which stall had the queue, where the bulk buyers showed up.

### Why ES and NQ specifically

- **Centralised exchange.** All trades clear on the CME. Every transaction is recorded and visible — no fragmented dark-pool prints to hide the picture.
- **Deep liquidity.** Thousands of contracts a minute produce statistically meaningful data. Thin markets produce noise.
- **Consistent hours.** Regular Trading Hours (RTH) are 09:30–16:00 **ET**, a predictable rhythm you can learn.
- **Institutional participation.** The big funds, banks, and algos all operate here, and their footprints show up in the volume.

---

## 02 · Understanding the market first

Skipping this is the number-one reason beginners fail. Learn the game before you open the tool.

### The auction

Every futures market is an auction. Price rises until sellers overwhelm buyers, falls until buyers overwhelm sellers, and consolidates when the two are balanced. Everything else is a variation of that.

**Mental model.** Two eBay auctions running at once — buyers trying to pay less, sellers trying to receive more. The price you see is the last point they agreed. When one side gets aggressive, price moves. When both are comfortable, price stalls.

### Vocabulary you must know

| Term | Meaning |
|---|---|
| **Bid** | Highest price a buyer will currently pay. Sell at market → you hit the bid. |
| **Ask (Offer)** | Lowest price a seller will currently accept. Buy at market → you lift the ask. |
| **Spread** | Gap between bid and ask. ES/NQ are typically 1 tick. Every tick you cross is a cost. |
| **Liquidity** | How many orders sit at each price. High = easy fills; low = price moves fast. |
| **HVN** (High Volume Node) | A price where huge volume traded historically. Acts as a magnet; price slows or returns. |
| **LVN** (Low Volume Node) | A price where little traded. Price tends to move through it quickly. |
| **POC** (Point of Control) | The single price with the most volume in a period — the "fairest" price. A key reference. |
| **Value Area** | The range holding ~70% of a session's volume. Inside = "fair"; outside = expect a return or a breakout. |
| **RTH / ETH** | Regular Trading Hours (09:30–16:00 ET) vs Extended (overnight). RTH matters most for profiles. |
| **Tick** | Smallest price increment (0.25 pts on ES/NQ). |

### Contract values

| Instrument | Per point | Per tick (0.25) |
|---|---|---|
| **ES** (E-mini S&P 500) | $50 | $12.50 |
| **NQ** (E-mini Nasdaq-100) | $20 | $5.00 |
| **MES** (Micro S&P) | $5 | $1.25 |
| **MNQ** (Micro Nasdaq) | $2 | $0.50 |

---

## 03 · Installing and setting up

The ATAS desktop app is **Windows-only** (it's a .NET application). There are web and mobile offerings, but serious order-flow work happens on the desktop — Mac users will need Windows via Boot Camp, a VM, or a cloud machine.

1. **Download.** Get the installer from [atas.net](https://atas.net). There's a free trial — use it before subscribing.
2. **Create an account.** Your licence ties to the account, not the machine, so you can install on more than one PC.
3. **Connect a data feed.** ATAS needs a live source. For ES/NQ, **Rithmic** and **CQG** are the common feeds, usually supplied by your futures broker (e.g. AMP Futures). *Feed and broker compatibility changes over time — verify the current supported list on atas.net rather than trusting any guide.*
4. **Add instruments.** Search for ES and NQ. Load the **front-month** contract (nearest expiry) — that's where the volume is.
5. **Open a chart.** Right-click the instrument → New Chart. Start with a plain 5-minute candle chart to confirm data is flowing.
6. **Set session times.** In chart settings, set the session to **RTH (09:30–16:00 ET)** so your profiles build on liquid data, not thin overnight moves.

> **Contract rollover.** ES/NQ expire quarterly (Mar/Jun/Sep/Dec). Volume migrates to the next contract roughly a week before expiry (around the second Thursday of the expiry month). Always trade the contract with the highest volume — ATAS shows volume on the contract picker. Poor fills or low activity? Check whether you need to roll forward.

---

## 04 · The interface

It looks overwhelming at first. It isn't, once you know what each area does.

| Area | What it is | Think of it as |
|---|---|---|
| **Chart window** | Main price chart (candles, bars, or footprints) | The movie of price action |
| **Volume Profile** | Horizontal bars showing volume at each price | A map of where trading happened |
| **Footprint** | Each candle broken into price levels with buy/sell volume inside | X-ray vision inside each candle |
| **DOM** (Depth of Market) | Live order book of pending orders at each price | The queue of orders waiting |
| **Delta panel** | Running buying-minus-selling volume | A tug-of-war score |
| **Tape / Time & Sales** | Scrolling list of every trade as it happens | The raw transaction log |
| **Indicator panel** | Add-ons: cumulative delta, VWAP, MAs | Optional overlays for context |

> **First-week advice.** Open ATAS during market hours and just *watch*. No indicators, no trading. See where price slows, where it accelerates. Let the data become familiar before you analyse it.

---

## 05 · Volume Profile — your core tool

The profile is the foundation of everything else. Master it before footprints or delta.

On the side of the chart you'll see a horizontal histogram: longer bar = more volume traded at that price, shorter bar = less. That's the whole concept.

**Analogy.** A 100-floor hotel after a busy week. Floor 47 was always full — that's your HVN. Floors 80–90 were empty — LVN. The single busiest floor is the POC. A volume profile is exactly this, for price levels.

### The three profile types

- **Session profile** — one RTH day. Shows where today's or yesterday's market found acceptance. Your most important daily reference.
- **Composite profile** — multiple sessions (5-day, 10-day). Reveals longer-term value areas and major HVNs/LVNs that act as support/resistance over weeks.
- **Visible-range profile** — built from whatever is on screen. Quick read of the area you're focused on.

### Adding one in ATAS

1. Right-click the chart → **Add Indicator**.
2. Search **"Cluster Profile"** (ATAS's feature-rich profile tool) or Volume Profile.
3. Set the period to **Session** for daily profiles — it rebuilds each new RTH session.
4. Enable the **POC line** and **Value Area High/Low** lines.
5. Turn on **previous sessions** (prior 3–5). Old POCs and value areas often interact with current price.

### Using it for scalping

**At the open, note:** yesterday's POC (price often revisits early), yesterday's VAH/VAL (first S/R levels), obvious composite HVNs (magnets), and LVNs between price and nearby HVNs (fast-move zones).

**During the session, watch for:**
- Price approaching an HVN from below → expect slowdown/rejection. Don't chase into a big HVN.
- Price clearing an LVN → often accelerates through it (breakout zones).
- Price returning to POC → extremely common; the POC is the session's gravity.
- Price testing VAH/VAL → decision points (accept and hold, or reject?). One of the cleaner scalp contexts.

> Never assume a level holds just because it's on the profile. Confirm with delta and footprint before acting.

---

## 06 · The footprint chart

ATAS's signature feature: what happened *inside* every candle.

A regular candle gives open/high/low/close and total volume. A footprint candle shows, at every price level inside it, how many contracts traded **on the bid** (aggressive sellers) vs **on the ask** (aggressive buyers).

**Plain English.** Each row shows two numbers: left = selling volume, right = buying volume. `120 × 45` means 120 sold aggressively, only 45 bought — sellers in control. `12 × 890` means buyers overwhelmed sellers — likely strong institutional buying.

> **Important caveat the original guide omits:** bid/ask volume is **inferred**, not ground truth. Platforms reconstruct which side was the aggressor from trade direction logic, and in fast tape that classification can be wrong. Treat footprint and delta numbers as a high-quality *estimate*, not gospel — which is exactly why we demand *confluence* rather than trading a single read.

### Four things to look for

| Pattern | What it looks like | What it means |
|---|---|---|
| **Imbalance** | One side ≥ 3× the other at the same price | Aggressive one-sided activity; often starts a move |
| **Absorption** | Heavy selling but price won't fall (or heavy buying but price won't rise) | The other side is absorbing the aggression — reversal risk |
| **Exhaustion** | Delta keeps pushing but price stops making new highs/lows | The aggressive side is running out of fuel |
| **Stacked imbalances** | Several consecutive rows dominated by the same side | Strong directional conviction; can signal continuation |

### Setting up the footprint

1. Right-click → Chart Type → **Cluster** (this is the footprint display).
2. Start in **Bid × Ask** mode (raw buy/sell at each row). Try Delta mode later.
3. Enable **imbalance highlighting**. The original guide says 300% (3:1) universally — see the upgrade below.
4. Start with **1-tick rows** (0.25 pts) for max granularity; move to 2-tick if cluttered.

> **v2 upgrade — calibrate the imbalance ratio per instrument.** A flat 3:1 fires constantly on NQ because NQ is materially noisier than ES. My [v2 spec](../strategies/absorption-fade-v2.md#c2--cluster-imbalance-at-the-extreme) uses **4:1 on NQ, 3:1 on ES**. Set this per-instrument from day one or you'll drown in false imbalances on NQ.

> **v2 upgrade — prefer tick bars over time bars for footprint reading.** Time bars distort absorption reads on slow tape (a quiet 5-minute bar and a frantic one look the same size). v2 uses a **233-tick footprint** so every bar represents the same amount of *activity*, not the same amount of *clock*. Section 08 below keeps the time-bar default for orientation, but know that the tick-bar version is the better tool.

> **Patience required.** Footprint reading takes weeks to develop. Don't trade from it on day one — spend your first two weeks identifying patterns and watching what price does next.

---

## 07 · Delta — the hidden signal

**Delta = total buying volume − total selling volume.** That's the maths. What it tells you is the *net aggression* in the market.

**Example.** A 5-min candle trades 10,000 contracts: 6,500 market buys, 3,500 market sells → delta +3,000. Buyers were more aggressive. If that candle closed up, the move is confirmed. If it closed **down** despite +3,000 delta, that's **delta divergence** — a warning that aggressive buyers were *absorbed*.

### The three delta reads scalpers use

- **Confirming delta** — price up with positive delta (or down with negative). The move has conviction; you can participate with it.
- **Delta divergence** — price and delta disagree (new price high, lower delta high). One of the strongest reversal cues — the move is running on fumes.
- **Cumulative delta trend** — the running session total. When it trends one way all session, that's a strong trending day; fading it is high-risk.

### Adding delta in ATAS

1. Right-click → Add Indicator → **Delta** (as a sub-panel).
2. Add **Cumulative Delta** (session score) as an overlay or second panel.
3. In Cluster Profile settings, enable **Delta Profile** colouring — were the HVNs built by buyers or sellers? Adds a conviction dimension.

> **v2 upgrade — watch for *hidden* divergence too.** Classic divergence is "price makes a new extreme, CVD doesn't." The hidden form is the reverse: **CVD makes a new extreme while price holds** — stealth absorption where passive players are quietly winning. [v2 condition C4](../strategies/absorption-fade-v2.md#c4--cvd-divergence-either-form-qualifies) accepts either form, which catches accumulation the classic-only read misses.

> **Key insight.** The strongest setups are *confluence*: price at a key level **and** delta divergence **and** a footprint showing absorption. Any single signal alone is weak. Delta tells you *who was aggressive, not who wins* — always ask what price did as a result.

---

## 08 · Configuring ATAS for ES/NQ scalping

A sensible, uncluttered starting layout. Not the only valid one.

### Chart 1 — Execution (primary)

| Setting | Value | Why |
|---|---|---|
| Chart type | Cluster (footprint) | Order-flow detail inside each bar |
| Bars | 3-min to start → **233-tick (v2)** | Tick bars avoid time-bar distortion; see note below |
| Display mode | Bid × Ask | Raw buying/selling at each row |
| Imbalance threshold | **4:1 NQ / 3:1 ES** | Instrument-calibrated; flat 3:1 is too noisy on NQ |
| Volume Profile | Session + 3 previous | Context of current and recent days |
| POC line | On, bright colour | Immediate session-gravity reference |
| Value Area | On, subtle shading | Fair-value range at a glance |
| Delta panel | Below chart | Confirm or question every move |
| VWAP | Overlay | Institutional benchmark; above VWAP = above intraday fair value |

> The original guide recommends a flat 3-min time footprint with a 300% imbalance for everything. Both defaults are fine for *learning the interface*, but for live setups use the calibrated values above — they're the result of my own v2 tuning, not arbitrary.

### Chart 2 — Context (reference, don't trade from it)

| Setting | Value |
|---|---|
| Chart type | Standard candlestick (or 1-min per v2 context chart) |
| Timeframe | 30-min for the big picture |
| Volume Profile | Composite, 10 sessions |
| Cumulative Delta | Overlay or sub-panel |
| Purpose | Where are the major HVNs/LVNs across the past two weeks? |

> **Pro tip.** Once configured, save it: File → Save Workspace. Load your exact setup each morning instead of rebuilding.

---

## 09 · Your first setup

A concrete, beginner-friendly framework for building pattern recognition. **Not** a complete strategy — for the mechanical version I'm validating, see [Absorption Fade v2](../strategies/absorption-fade-v2.md).

### The Value-Area Fade

> **Heads-up: this is a *counter-trend* setup.** Fading an extreme is genuinely harder than trading with the flow. A gentler first pattern is a *with-trend* one — e.g. a pullback into value in the direction of a trending cumulative delta. I'm putting the fade first because it's well-documented, but go in knowing it's one of the harder archetypes for a beginner.

**The real statistic (stated correctly).** This setup leans on the Market Profile **"80% Rule"** (Dalton). The rule is *not* "price returns to value 80% of days." It is: **if** price opens **outside** the prior value area, then trades **back inside** it and **accepts** there for **two consecutive 30-minute periods**, **then** there's roughly an 80% chance it traverses the full value area. The preconditions are the whole point — without the re-entry and acceptance, the edge isn't there. Read as "fade the open 80% of the time" (as the original guide implies) it will get you run over on trend days.

**Setup conditions:**
- Price opens **outside** yesterday's value area (above VAH or below VAL).
- In the first 15–30 min, price stalls or reverses **back toward** value (and ideally re-enters and accepts — that's the 80% rule firing).
- Delta on those early candles shows **divergence** (price pushing the extreme, delta not confirming).
- Footprint shows **absorption** at the extreme (big one-sided volume, price not continuing).

**Entry:** wait for price to turn back toward value; enter on the first footprint candle showing a clear **delta flip** and imbalances in your direction. A limit near the reversal candle's extreme gets a better fill.

**Targets and stop:**
- TP1: the value-area boundary (VAH/VAL). TP2: yesterday's POC if running a partial.
- Stop: beyond the session extreme made before the reversal.
- Example: a 4–8 tick stop with an 8–16 tick target = 1:2 minimum. Never risk more than you're targeting.

> **Mind the costs (the original guide ignores this).** For a scalper, commissions and slippage are a *first-order* variable, not a footnote. On an 8-tick NQ scalp (~$40 gross), a round-turn commission plus exchange/NFA fees plus one tick of slippage can eat a meaningful slice of the gross — proportionally even more on micros. Pull your broker's actual fee schedule and bake round-turn cost + realistic slippage into every R:R calculation. A "1:2" that ignores costs may really be 1:1.5 or worse.

> **When it fails.** The 80% figure is across hundreds of sessions; any single day can break. The clean failure mode is an **open-drive** that keeps making new extremes with *confirming* delta. If you see that, stand aside — the market wants to go further, not return.

---

## 10 · Reading the market step by step

A daily routine to build into a habit.

### Pre-market (08:00–09:25 ET)

1. **Mark prior-session levels.** Yesterday's POC, VAH, VAL; obvious composite HVNs/LVNs. This is your map.
2. **Note the overnight range.** Where did it trade overnight, where is it at 09:00, above or below yesterday's value? Frames your early bias.
3. **Check the economic calendar.** Never trade the first minutes after major releases (CPI, NFP, FOMC, GDP) — extreme volatility stops you out regardless of analysis.
4. **Set a thesis.** Mean-reversion day (return to value) or trending day (value expansion)? You can't be certain, but a primary thesis stops random trading.

### First 30 minutes (09:30–10:00 ET) — observe, don't trade

This is the **discovery** phase: price is finding its level, volume spikes, sharp reversals. Watch for:
- Is price accepting above/below yesterday's value? (holding above VAH is bullish)
- Is cumulative delta trending or choppy?
- Any large footprint imbalances forming at key levels?
- Is the opening profile building balance (bell shape) or elongating (trend)?

### Mid-session (10:00–14:00 ET) — most tradeable

Institutional activity is high, patterns are cleaner, the initial range is set.
- Trade reactions at the levels you marked pre-market.
- Confirm or cancel each setup with footprint and delta before entering.
- Watch the developing session POC — price oscillates around it in balance.
- If cumulative delta trends consistently, trade pullbacks *with* it rather than fading.

### Late session (14:00–15:30 ET)

Activity picks up into the close; position-squaring creates sharp moves. Useful for momentum scalps, but widen stops for the higher volatility.

---

## 11 · Common beginner mistakes

1. **Trading every signal.** Most of what you see is noise. The profitable trades are the obvious, high-confluence ones — and they're rare. Patience is the edge.
2. **Ignoring the context chart.** Only watching the 3-min footprint is like navigating a city by staring at your feet. Always check the 30-min first: are you with or against the bigger trend?
3. **Moving stops to avoid being stopped out.** Your stop is where you're *wrong*. Being stopped is the system working. Moving it is the system breaking.
4. **Over-complicating the setup.** More indicators conflict and paralyse. Strip back to volume profile, footprint, delta. Complexity is not sophistication.
5. **Going live too soon.** Use ATAS's **replay** obsessively. Spend 60–90 days reading footprint/delta in simulated real-time before risking capital. The market will still be there; lost capital takes time to recover.
6. **Treating delta as a direction predictor.** Positive delta does *not* mean price goes up. A big positive-delta push that gets absorbed is sellers winning. Always ask: what did price do as a *result* of this delta?

---

## 12 · Learning roadmap

A realistic path from beginner to competent scalper. Assumes consistent daily study. This mirrors the staged, evidence-gated philosophy in my [4-phase validation roadmap](../strategies/absorption-fade-roadmap.md).

### Phase 1 — Foundation (Weeks 1–4)

Be comfortable navigating ATAS and understand every core concept without looking it up. Install with a demo account, watch live daily without trading, read auction-market theory, identify POC/VAH/VAL on the prior day and watch how price interacts, replay sessions each evening.

### Phase 2 — Pattern recognition (Weeks 5–10)

Identify absorption, imbalances, and delta divergence in real time. Keep replaying. Journal: *"saw X pattern at Y level, price did Z."* After ~100 logged observations the patterns start to feel intuitive.

### Phase 3 — Simulated trading (Weeks 11–16)

Execute setups consistently in sim, tracking honestly. Use ATAS sim or a paper account. Log every trade: entry reason, delta confirmation, result. After ~6 weeks, review the data — profitable? If not, fix one recurring mistake at a time (entry timing, stop placement, or setup selection).

### Phase 4 — Live, micro sizing (Weeks 17–24+)

Real capital at minimum size — **1 contract, micros first (MES/MNQ)**. An ES tick is $12.50; an MES tick is $1.25. Micros keep risk minimal while introducing the emotional and execution dynamics sim can't replicate. Only scale up after **3 consecutive profitable months**.

### The numbers to remember

| | |
|---|---|
| **6 months** | Minimum before live trading |
| **MES / MNQ** | Start with micros, not full contracts |
| **1:2** | Minimum risk:reward per trade (after costs) |
| **3** | Confluent signals aligned before entering |

> **Prop-firm note.** Many people now fund futures scalping through evaluation/prop accounts rather than personal capital. That changes the rules (daily-loss limits, trailing drawdown, consistency rules) and adds its own discipline pressure. If you go that route, treat the eval's rules as hard constraints layered *on top of* everything above.

---

## Where this guide oversimplifies (read before you rely on it)

Quick reference for future-me — the spots where the generic beginner advice needs the v2 correction:

| Generic guide says | Reality / v2 correction |
|---|---|
| Imbalance threshold 300% (3:1) for everything | **4:1 on NQ, 3:1 on ES** — NQ is noisier ([v2 C2](../strategies/absorption-fade-v2.md#c2--cluster-imbalance-at-the-extreme)) |
| Use 3-min / 5-min time footprints | **233-tick bars** avoid time-bar distortion on slow tape ([v2 chart config](../strategies/absorption-fade-v2.md#atas-chart-configuration)) |
| Delta divergence = classic only | Also watch **hidden divergence** (CVD extends, price holds) ([v2 C4](../strategies/absorption-fade-v2.md#c4--cvd-divergence-either-form-qualifies)) |
| Price returns to value ~80% of days | It's the **80% Rule** with preconditions (open outside → re-enter → accept 2 periods) |
| R:R math (1:2) | Only after **commissions + slippage** — costs are first-order for scalping |
| Footprint numbers are fact | Aggressor side is **inferred**; treat as a strong estimate, demand confluence |
| Value-area fade as first setup | It's **counter-trend** (harder); a with-trend pullback is gentler to start |
| Times in EST | Use **ET** — the US is on EDT for ~8 months of the year |

---

## Related files

- [Absorption Fade v2 — the mechanical setup I'm validating](../strategies/absorption-fade-v2.md)
- [v2 pre-trade checklist](../strategies/absorption-fade-v2-checklist.md) — print and pin
- [4-phase validation roadmap](../strategies/absorption-fade-roadmap.md) — decision gates per phase
- [v2 ATAS indicator (AbsorptionFadeConfluence)](../../indicators/atas-csharp/AbsorptionFadeConfluence/README.md)

*Some explanatory content was rephrased from external sources for compliance with licensing restrictions. Sources are linked inline.*
