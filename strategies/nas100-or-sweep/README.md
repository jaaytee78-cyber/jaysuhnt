# NAS100 — NY AM Open Range Sweep & Reversal

Research project: codify, backtest, and validate an Open Range sweep-and-reversal
strategy on NAS100 (researched on QQQ as a 1:1 proxy, traded live on NQ/MNQ).

## Hypothesis

During the first 15 minutes of the New York cash session (09:30–09:45 ET), price
forms an **Opening Range (OR)**. Frequently, one side of this OR is wicked
through during the following 75 minutes (09:45–11:00) to take resting liquidity,
after which price reverses and trades back to the opposite side of the OR or
beyond. We want to know:

1. Does this pattern produce a statistically significant edge?
2. If so, which conditions amplify or destroy the edge?
3. Can the edge survive walk-forward and out-of-sample testing?

## Strategy v1 (most mechanical possible)

| Rule | Definition |
|---|---|
| OR window | 09:30:00 → 09:44:59 ET |
| Trade window | 09:45:00 → 11:00:00 ET |
| Sweep | 1m bar that wicks beyond OR-H/L and closes back inside the OR |
| Entry | Market on close of confirmation bar |
| Stop | 1 tick beyond the sweep wick |
| Target | Opposite side of OR (≥1R) |
| Time stop | Flat at 11:00 ET if neither hit |
| Trades/day | Max 1 |

## Risk model

- Fixed dollar risk per trade (default $100), position-sized to stop distance
- Costs: $0 commission + $0.01/share slippage each side (QQQ proxy)

## Research phases

- **Phase 0** — Infrastructure: data loader, parquet cache, sessions module
- **Phase 1** — Exploratory data analysis (does the edge exist?)
- **Phase 2** — Strategy v1 backtest
- **Phase 3** — Filter iteration (only what EDA justified)
- **Phase 4** — Walk-forward + out-of-sample validation
- **Phase 5** — Pine Script confluence dashboard
- **Phase 6** — Forward test on demo

## Setup

```bash
cd strategies/nas100-or-sweep
uv sync
cp .env.example .env   # then put your POLYGON_API_KEY in .env
```

## Pulling data

```bash
# Once POLYGON_API_KEY is set in .env:
uv run python scripts/fetch_data.py --ticker QQQ --start 2020-01-01 --end 2025-05-22
```

Output is cached as parquet under `data/` (gitignored).

## Layout

```
src/
  data.py        # Polygon loader + parquet cache
  sessions.py    # NY tz, OR window, killzones
scripts/
  fetch_data.py  # CLI to pull and cache bars
notebooks/       # Jupyter notebooks for EDA (Phase 1+)
data/            # parquet cache (gitignored)
```
