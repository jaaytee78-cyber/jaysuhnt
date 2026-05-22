# Data Quality Report
Source: `data/QQQ_1minute.parquet`
Total bars: **439,877**
Range: **2024-05-22 08:00:00+00:00** -> **2026-05-21 23:59:00+00:00**

## Regular-session daily summary
Trading days seen: **501**
Avg RTH bars/day: **387.9**  (full session = 390)
Median RTH bars/day: **390**
Days with <380 RTH bars (likely halts/half-days): **6**

## Opening Range coverage (09:30-09:44:59 NY)
Days with full 15-bar OR: **501**
Days with partial OR (1-14 bars): **0**
Days with zero OR bars: **0**

## Calendar coverage
Business days in range: **522**
Days present in cache: **501**
Missing business days: **21**  (US market holidays will appear here, plus any data gaps)

First 10 missing dates: 2024-05-27, 2024-06-19, 2024-07-04, 2024-09-02, 2024-11-28, 2024-12-25, 2025-01-01, 2025-01-09, 2025-01-20, 2025-02-17

## Low-volume / suspicious days
Median daily RTH volume: **37,597,877** shares
Days with <30% of median volume: **0**
