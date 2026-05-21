# Pine Script Indicators

Custom TradingView indicators. Pine Script v5 / v6 (per file).

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

| File | Pine | Purpose | Validated? |
|---|---|---|---|
| `killzones.pine` | v5 | London / NY killzones with optional session H/L lines | (visual aid only — no signals to validate) |
| `donchian_xau_4h.pine` | v6 | XAU 4h trend-following breakout (20-bar Donchian + 2 ATR stop + 3:1 RR) | **Yes — see backtests/reports/donchian_validation_xau_*** |

### donchian_xau_4h.pine — quick reference

- **Apply to:** XAU/USD on **4-hour** timeframe.
- **Default direction:** longs only. Shorts disabled because IS shorts (-0.87R/trade in 2024-2026 bull market) were a structural loser. Re-enable shorts manually only if a sustained downtrend is confirmed.
- **Validation:** OOS 43 trades, 42% WR, +0.62R/trade, PF 2.06, coin-flip P=0.029 (the only sub-0.05 result in this repo's validation set). See `backtests/reports/donchian_validation_xau_compare_2026-05-21.md` for the full report.
- **Position management:** stop and target are frozen at fire-bar close. No time stop. Position runs until either level hits.

## Indicators planned

- [ ] `liquidity.pine` — marks equal highs/lows and crossed liquidity
- [ ] `market-structure.pine` — auto-detects BOS / CHoCH
- [ ] `order-blocks.pine` — highlights bullish/bearish order blocks
- [ ] `fvg.pine` — fair value gap / imbalance detector
- [ ] `session-bias.pine` — Asia range + daily/weekly bias helper
