"""
CLI to pull and cache aggregate bars from Polygon.

Examples
--------
# Default: QQQ 1-minute bars for the last full year, into data/QQQ_1minute.parquet
python scripts/fetch_data.py --ticker QQQ --start 2024-01-01 --end 2024-12-31

# Free-tier friendly throttling (5 req/min):
python scripts/fetch_data.py --ticker QQQ --start 2024-01-01 --end 2024-12-31 --throttle

# Force re-fetch (ignore cache):
python scripts/fetch_data.py --ticker QQQ --start 2024-01-01 --end 2024-12-31 --refresh
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Allow running as a plain script from the project root.
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.data import PolygonConfig, load_aggs  # noqa: E402


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Fetch and cache Polygon aggregate bars.")
    p.add_argument("--ticker", default="QQQ", help="Ticker symbol (default: QQQ)")
    p.add_argument("--start", required=True, help="Start date YYYY-MM-DD (inclusive)")
    p.add_argument("--end", required=True, help="End date YYYY-MM-DD (inclusive)")
    p.add_argument("--multiplier", type=int, default=1, help="Bar multiplier (default: 1)")
    p.add_argument(
        "--timespan",
        default="minute",
        choices=["minute", "hour", "day"],
        help="Bar timespan (default: minute)",
    )
    p.add_argument("--refresh", action="store_true", help="Ignore cache and re-fetch")
    p.add_argument(
        "--throttle",
        action="store_true",
        help="Sleep 13s between pages (free-tier 5/min friendly)",
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()

    try:
        cfg = PolygonConfig.from_env(free_tier_throttle=args.throttle)
    except RuntimeError as exc:
        print(f"[error] {exc}", file=sys.stderr)
        return 2

    print(
        f"Fetching {args.ticker} {args.multiplier}{args.timespan} "
        f"from {args.start} to {args.end} (refresh={args.refresh}, "
        f"throttle={args.throttle})..."
    )

    df = load_aggs(
        args.ticker,
        args.start,
        args.end,
        multiplier=args.multiplier,
        timespan=args.timespan,
        config=cfg,
        refresh=args.refresh,
    )

    if df.empty:
        print("[warn] No bars returned. Check your date range and ticker.")
        return 1

    print(f"\nFetched {len(df):,} bars")
    print(f"  range : {df.index.min()}  →  {df.index.max()}")
    print(f"  cols  : {list(df.columns)}")
    print("\nHead:")
    print(df.head(3))
    print("\nTail:")
    print(df.tail(3))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
