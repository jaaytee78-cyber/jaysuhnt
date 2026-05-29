# AbsorptionFadeConfluence — ATAS Indicator (v2)

Custom ATAS indicator implementing [Absorption Fade v2](../../../knowledge-base/strategies/absorption-fade-v2.md). It auto-scores 4 of the 5 conditions (C2–C5) on a 0–4 histogram. The 5th condition (C1 — location at a predefined HTF level) is your call, exposed as a toggle. When the total reaches 5/5 in a clear direction, an arrow plots and an alert fires.

> **Status:** Phase-2 skeleton ([roadmap](../../../knowledge-base/strategies/absorption-fade-roadmap.md)). Compilable and runnable. Condition math uses reasonable defaults that need tuning once Phase 1 manual replay produces feedback. Search for `// TUNE:` comments in `AbsorptionFadeConfluence.cs`.

> **Supersedes:** [`AbsorptionFadeScout`](../AbsorptionFadeScout/README.md) — kept for reference and side-by-side comparison.

---

## What it does

| Condition | Auto-detected? | How |
|---|---|---|
| **C1** Location at HTF level | ⚠ Manual toggle | You flip `LevelConfirmed` in the indicator settings when price reaches a real level |
| **C2** Cluster imbalance at extreme | ✅ Auto | Scans clusters within 4 ticks of bar high/low for `AskVol/BidVol` (long) or `BidVol/AskVol` (short) ≥ `ImbalanceRatio` |
| **C3** Heavy delta + no progress | ✅ Auto | `Volume ≥ 1.5× 20-bar avg` AND `\|Delta\| ≥ 70% of vol` AND (close in opposite ≤25% OR rejection wick ≥ 60%) |
| **C4** CVD divergence (classic OR hidden) | ✅ Auto | Compares price extreme + running CVD over `CvdLookbackBars`. Either form qualifies |
| **C5** Trigger bar (midpoint + delta flip) | ✅ Auto | Bar N closes through bar N-1 midpoint AND delta sign flipped — both required |

Final score on the trigger bar = `C2 + C3 + C4 + C5 + LevelConfirmed`, capped at 5. Arrow + alert fire at 5/5 in a clear direction.

---

## Score scale — reading the histogram

| Score | Meaning | Action |
|---|---|---|
| 0–2 | No edge | Ignore. The indicator protecting you from false setups is as valuable as it firing on real ones |
| 3 | Conditions building | Pay attention. Check which condition is missing |
| 4 | High probability forming | Hands on keyboard. Pre-plan entry, stop, target. Wait for the 5th |
| **5** | **FULL SIGNAL** | Arrow + alert. All 5 confirmed. Enter on bar close |

The histogram is colored by score (dim → amber → green → bright green at 5).

---

## Calibration per instrument

| Instrument | `ImbalanceRatio` | Notes |
|---|---|---|
| **NQ / MNQ** | **4.0** | NQ is materially noisier than ES. 3.0 produces too many false positives |
| **ES / MES** | **3.0** | Standard 3:1 footprint imbalance threshold |
| Cleaner signals | 5.0 | Fewer trades, higher quality. Test in replay first |

Set this once per chart. If you switch instruments, change the parameter.

---

## Zero-programming install (Windows)

Total time: ~20 minutes the first time, ~30 seconds for every update after.

### Step 1 — Install Visual Studio Community (free)

1. Go to <https://visualstudio.microsoft.com/downloads/>
2. Download **Visual Studio Community 2022** (free for individual use)
3. During install, on the **Workloads** screen, tick:
   - ☑ **.NET desktop development**
4. Click **Install**, wait, restart if it asks.

### Step 2 — Locate the ATAS DLLs

ATAS ships its API as DLLs you'll reference. They live here on Windows:

```
C:\Users\<YOU>\AppData\Roaming\ATAS\Bin
```

You should see:

- `ATAS.Indicators.dll`
- `ATAS.DataFeedsCore.dll`
- `OFT.Attributes.dll`
- `Utils.Common.dll`

Don't move them. Just remember the path.

### Step 3 — Open this project in Visual Studio

1. Clone or download this repo to your computer (if you haven't already).
2. Open `AbsorptionFadeConfluence.csproj` by **double-clicking it** — Visual Studio launches.
3. In the **Solution Explorer** (right side), right-click **References** (or **Dependencies** in newer VS) → **Add Reference** → **Browse**.
4. Navigate to `C:\Users\<YOU>\AppData\Roaming\ATAS\Bin` and select all 4 DLLs from Step 2. Click **Add**.

### Step 4 — Build the indicator

1. Top menu: **Build → Build Solution** (or press `Ctrl + Shift + B`).
2. Watch the **Output** window at the bottom for:
   ```
   Build: 1 succeeded, 0 failed
   ```
3. The compiled file appears at:
   ```
   indicators\atas-csharp\AbsorptionFadeConfluence\bin\Debug\net8.0\AbsorptionFadeConfluence.dll
   ```

### Step 5 — Install into ATAS

1. Copy `AbsorptionFadeConfluence.dll` (just that one file) into your ATAS indicators folder:
   ```
   C:\Users\<YOU>\Documents\ATAS\Indicators
   ```
   (Create that folder if it doesn't exist.)
2. Restart ATAS.
3. Open a 233-tick footprint chart → indicator icon → search **"Absorption Fade Confluence"** → add.

### Step 6 — Configure on chart

The indicator has these parameters (defaults shown):

| Parameter | Default | Notes |
|---|---|---|
| `ImbalanceRatio` | 4.0 | **Calibrate per instrument: NQ 4.0 / ES 3.0** |
| `VolumeMultiplier` | 1.5 | Bar vol vs 20-bar avg |
| `VolumeAvgPeriod` | 20 | Lookback bars |
| `DeltaThresholdPct` | 70 | \|delta\| / vol % |
| `BodyClosePct` | 25 | Body close in opposite end ≤ % |
| `WickPct` | 60 | Alternative: rejection wick ≥ % |
| `CvdLookbackBars` | 8 | Pivot window for divergence |
| `LevelConfirmed` | false | **YOUR C1 toggle.** Flip ON at a real level |
| `MinScoreToArrow` | 5 | 5 for live; 4 to review near-misses in replay |
| `AlertOnFull` | true | Sound + popup on 5/5 |

Leave everything except `ImbalanceRatio` at default for now. Tune after Phase 1 data tells us what works.

---

## How to use it during a session

1. **Mark levels** at session start: PDH/PDL, weekly H/L, ON H/L, VAH/VAL/POC, HVNs, VWAP ±1σ/±2σ.
2. **Watch the histogram** as price approaches a level. It builds 1 → 2 → 3 → 4 as conditions confirm.
3. **When price reaches your level**, flip `LevelConfirmed` ON. The histogram bumps by +1.
4. **Wait for the trigger bar** to close. If C5 fires (midpoint + delta flip), score hits 5 → arrow + alert.
5. **Enter on bar close** at market or limit. Set stop 1 tick beyond absorption wick. TP1 = 1R. TP2 = structural.
6. **After the trade**, flip `LevelConfirmed` OFF until the next setup.

Treat the indicator as a *mechanical second opinion* — it can't see whether the level you're at is meaningful. That's why C1 is your call.

---

## When it doesn't work — common errors

| Error | Likely cause | Fix |
|---|---|---|
| `'ATAS.Indicators' could not be found` | DLLs not referenced | Redo Step 3 |
| Build succeeded but indicator doesn't appear in ATAS | DLL copied to wrong folder | Copy to `Documents\ATAS\Indicators`, not `AppData\...\ATAS\Bin` |
| ATAS crashes on chart load | Indicator threw an exception | Check `Documents\ATAS\Logs\` for the latest log file → paste error to Kiro |
| Indicator appears but never plots | Auto-conditions too strict, or no clusters in feed | Verify your data feed exposes `Clusters` (Rithmic / CQG do; some demo feeds don't). Send a screenshot of a missed setup to Kiro |
| Score always tops out at 4 | Forgot to toggle `LevelConfirmed` | Flip the toggle when price reaches your level |
| Score histogram doesn't show | Histogram panel collapsed | Right-click chart panels → expand the indicator panel |

**Whenever something breaks → copy the error message to Kiro. Don't try to fix it yourself.**

---

## Updating the indicator

When Kiro ships a new version of `AbsorptionFadeConfluence.cs`:

1. `git pull` in your local repo (or download the latest file from the PR)
2. In Visual Studio: **Build → Build Solution**
3. Copy the new DLL into `Documents\ATAS\Indicators` (overwrite)
4. Restart ATAS

That's it. ~30 seconds once set up.

---

## Feedback loop — what to send Kiro

When the indicator does something wrong, send:

1. **Screenshot** of the chart with the indicator visible (price panel + histogram subgraph)
2. **Plain English** description: *"This bar at 14:32 fired but shouldn't have because the wick was tiny and price kept falling — that's a continuation, not absorption."*
3. **Approximate bar values** if visible: volume, delta, close position, cluster ratios at the extreme
4. **Time-of-day, instrument, and your `ImbalanceRatio` setting**

Kiro translates that into a code change. Ships a new version. You rebuild. We iterate.

---

## Files in this folder

| File | Purpose |
|---|---|
| `AbsorptionFadeConfluence.csproj` | Visual Studio project file (tells the compiler what to build) |
| `AbsorptionFadeConfluence.cs` | The indicator source code (~380 lines) |
| `README.md` | This file |

---

## Differences from `AbsorptionFadeScout` (v1)

| Aspect | Scout (v1) | Confluence (v2) |
|---|---|---|
| Score range | 0–4 (auto) | 0–5 (4 auto + 1 manual toggle) |
| C2 (volume) | Bar vol vs 20-bar avg | Cluster imbalance at extreme + bar vol (combined into C2/C3 split) |
| C4 (CVD) | Classic divergence only | Classic OR hidden divergence |
| C5 (trigger) | Midpoint reclaim only | Midpoint reclaim AND delta flip |
| Histogram | Hidden score series for review | Visible color-coded 0–5 panel |
| Level confirmation | Implicit (you eyeball the chart) | Explicit `LevelConfirmed` toggle that contributes to score |
| Calibration | Single threshold | `ImbalanceRatio` calibrated per instrument |
