# Pine Script Indicators

Custom TradingView indicators. Most are written in **Pine Script v5**; the
all-in-one Valentini Pro Scalper is on **Pine Script v6**.

## How to install one

1. Open TradingView and load any chart.
2. Click the **Pine Editor** tab at the bottom of the screen.
3. Delete whatever is in there.
4. Open the `.pine` file from this folder, copy the entire contents.
5. Paste into the Pine Editor.
6. Click **Save** (give it a name) → click **Add to chart**.
7. Adjust the settings via the gear icon next to the indicator name.

To save it permanently across charts, click **Add to chart**, then on the chart open the indicator settings → **Template** → **Save as default**.

## Indicators in this folder

| File | Version | Purpose |
|---|---|---|
| `killzones.pine` | v5 | Highlights London / NY killzones with optional session high/low lines |
| `valentini-pro-v3.pine` | v6 | All-in-one scalper: EMA ribbon, session VWAP, volume profile POC, BOS/MSS, order blocks, FVGs, Triple-A pattern, HTF trend filter, 7-factor confluence score, structure-aware ATR stops, trade state machine, expanded dashboard |

## Indicators planned

- [x] `market-structure.pine` — auto-detects BOS / CHoCH *(integrated into `valentini-pro-v3.pine`)*
- [x] `order-blocks.pine` — highlights bullish/bearish order blocks *(integrated into `valentini-pro-v3.pine`)*
- [x] `fvg.pine` — fair value gap / imbalance detector *(integrated into `valentini-pro-v3.pine`)*
- [x] `session-bias.pine` — partial; kill zones and HTF EMA bias inside `valentini-pro-v3.pine`. Standalone Asia-range / weekly-bias helper still TODO.
- [ ] `liquidity.pine` — marks equal highs/lows and crossed liquidity
