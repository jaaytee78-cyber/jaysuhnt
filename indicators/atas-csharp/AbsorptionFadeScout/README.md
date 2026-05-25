# AbsorptionFadeScout — ATAS Indicator

A custom ATAS indicator that auto-detects setups for the [Absorption Fade strategy](../../../knowledge-base/strategies/absorption-fade-scalp.md). It is a **scout** — it spots candidates, but you still confirm condition #1 (location) yourself. It is not an auto-trader.

> **Status:** Skeleton (Phase 2 of the [roadmap](../../../knowledge-base/strategies/absorption-fade-roadmap.md)). Compilable and runnable, but the condition math is intentionally kept simple. We tune it together once you've finished Phase 1 manual replay.

---

## What it does

For each bar, it scores the bar against 4 of the 5 AF conditions (it can't know what you've decided is a "predefined level," so condition #1 is your job):

| Condition | Auto-detected? |
|---|---|
| #1 Location at HTF level | ❌ Your job |
| #2 Volume spike (≥ 1.5× 20-bar avg) | ✅ |
| #3 Heavy delta + no progress (close % / wick %) | ✅ |
| #4 CVD divergence | ✅ |
| #5 Trigger bar closes through midpoint | ✅ |

When a bar scores **4/4 on auto conditions** AND the next bar fires the trigger, the indicator:

- Plots a coloured **dot** below (long) or above (short) the trigger bar
- Optionally plays a sound and pops a desktop alert
- Logs a value in a `Score` series so you can review historically

You then glance at the chart and ask: *"Is this at a real level?"* If yes → trade. If no → skip.

---

## Zero-programming install guide

Total time: ~20 minutes the first time, ~30 seconds for every update after.

### Step 1 — Install Visual Studio Community (free)

1. Go to <https://visualstudio.microsoft.com/downloads/>
2. Download **Visual Studio Community 2022** (free for individual use)
3. During install, on the **Workloads** screen, tick:
   - ☑ **.NET desktop development**
4. Click **Install**, wait, restart if it asks.

### Step 2 — Locate the ATAS DLLs on your machine

ATAS ships its API as DLLs you'll reference. They live here on Windows:

```
C:\Users\<YOU>\AppData\Roaming\ATAS\Bin
```

You should see files like:

- `ATAS.Indicators.dll`
- `ATAS.DataFeedsCore.dll`
- `OFT.Attributes.dll`
- `Utils.Common.dll`

Don't move them. Just remember the path.

### Step 3 — Open this project in Visual Studio

1. Clone or download this repo to your computer (if you haven't already).
2. Open `AbsorptionFadeScout.csproj` by **double-clicking it** — Visual Studio launches.
3. In the **Solution Explorer** (right side), right-click **References** (or **Dependencies** in newer VS) → **Add Reference** → **Browse**.
4. Navigate to `C:\Users\<YOU>\AppData\Roaming\ATAS\Bin` and select all 4 DLLs listed in Step 2. Click **Add**.

### Step 4 — Build the indicator

1. Top menu: **Build → Build Solution** (or press `Ctrl + Shift + B`).
2. Watch the **Output** window at the bottom. You want to see:
   ```
   Build: 1 succeeded, 0 failed
   ```
3. The compiled file appears at:
   ```
   indicators\atas-csharp\AbsorptionFadeScout\bin\Debug\net8.0\AbsorptionFadeScout.dll
   ```
   (path may vary slightly by .NET version)

### Step 5 — Install into ATAS

1. Copy `AbsorptionFadeScout.dll` (just that one file) into your ATAS indicators folder:
   ```
   C:\Users\<YOU>\Documents\ATAS\Indicators
   ```
   (Create that folder if it doesn't exist.)
2. Restart ATAS.
3. Open a chart → click the indicator icon → search for **"Absorption Fade Scout"** → add it.

### Step 6 — Configure on chart

In the indicator settings, you'll see:

- **Volume Multiplier** (default: 1.5)
- **Volume Avg Period** (default: 20)
- **Delta Threshold %** (default: 70)
- **Body Close %** (default: 25)
- **Wick %** (default: 60)
- **CVD Lookback Bars** (default: 8)
- **Min Score To Plot** (default: 4)
- **Play Sound On Trigger** (default: true)

Leave defaults for now. We tune after Phase 1 data tells us what works.

---

## When it doesn't work — common errors

| Error | Likely cause | Fix |
|---|---|---|
| `'ATAS.Indicators' could not be found` | DLLs not referenced | Redo Step 3 |
| Build succeeded but indicator doesn't appear in ATAS | DLL copied to wrong folder | Copy to `Documents\ATAS\Indicators`, not `AppData\...\ATAS\Bin` |
| ATAS crashes on chart load | Indicator threw an exception | Check `Documents\ATAS\Logs\` for the latest log file → paste error to Kiro |
| Indicator appears but never plots | Auto-conditions too strict | Send a screenshot of a bar you think should fire — Kiro will adjust |

**Whenever something breaks → copy the error message to me. Don't try to fix it yourself.**

---

## Updating the indicator

When Kiro ships a new version of `AbsorptionFadeScout.cs`:

1. `git pull` in your local repo (or download the latest file from the PR)
2. In Visual Studio: **Build → Build Solution**
3. Copy the new DLL into `Documents\ATAS\Indicators` (overwrite)
4. Restart ATAS

That's it. ~30 seconds once set up.

---

## Feedback loop — what to send Kiro

When you use the indicator and it does something wrong, send me:

1. **Screenshot** of the chart with the indicator visible
2. **Plain English** description: *"This bar at 14:32 fired but shouldn't have because the wick was tiny and price kept falling — that's a continuation, not absorption."*
3. **Approximate bar values** if visible: volume, delta, close position
4. **Time-of-day and instrument**

I translate that into a code change. Ship a new version. You rebuild. We iterate.

---

## Files in this folder

| File | Purpose |
|---|---|
| `AbsorptionFadeScout.csproj` | Visual Studio project file (tells the compiler what to build) |
| `AbsorptionFadeScout.cs` | The indicator code itself |
| `README.md` | This file |
