# Pine Script Indicators

Custom TradingView indicators. All written in **Pine Script v5**.

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

| File | Purpose |
|---|---|
| `killzones.pine` | Highlights London / NY killzones with optional session high/low lines |

## Indicators planned

- [ ] `liquidity.pine` — marks equal highs/lows and crossed liquidity
- [ ] `market-structure.pine` — auto-detects BOS / CHoCH
- [ ] `order-blocks.pine` — highlights bullish/bearish order blocks
- [ ] `fvg.pine` — fair value gap / imbalance detector
- [ ] `session-bias.pine` — Asia range + daily/weekly bias helper
