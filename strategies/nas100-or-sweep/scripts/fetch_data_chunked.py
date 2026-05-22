"""
Chunked Polygon fetch with visible progress and incremental cache writes.

Pulls one calendar month at a time, saves the parquet cache after each chunk
so the run is resumable, and respects the free-tier rate limit (5 req/min).

Usage:
    python scripts/fetch_data_chunked.py --ticker QQQ --start 2024-05-22 --end 2026-05-22
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.data import (  # noqa: E402
    DEFAULT_DATA_DIR,
    PolygonConfig,
    _cache_path,
    fetch_aggs,
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--ticker", default="QQQ")
    p.add_argument("--start", required=True)
    p.add_argument("--end", required=True)
    p.add_argument("--multiplier", type=int, default=1)
    p.add_argument("--timespan", default="minute")
    p.add_argument("--sleep", type=float, default=13.0,
                   help="Seconds between month requests (free tier ~5/min).")
    return p.parse_args()


def month_chunks(start: str, end: str) -> list[tuple[str, str]]:
    """Yield (chunk_start, chunk_end) inclusive monthly windows covering [start, end]."""
    s = pd.Timestamp(start).normalize()
    e = pd.Timestamp(end).normalize()
    chunks: list[tuple[str, str]] = []
    cur = s
    while cur <= e:
        month_end = (cur + pd.offsets.MonthEnd(0)).normalize()
        ce = min(month_end, e)
        chunks.append((cur.date().isoformat(), ce.date().isoformat()))
        cur = (ce + pd.Timedelta(days=1)).normalize()
    return chunks


def main() -> int:
    args = parse_args()
    cfg = PolygonConfig.from_env()
    cache = _cache_path(args.ticker, args.multiplier, args.timespan, DEFAULT_DATA_DIR)
    DEFAULT_DATA_DIR.mkdir(parents=True, exist_ok=True)

    existing: pd.DataFrame | None = None
    if cache.exists():
        existing = pd.read_parquet(cache)
        print(f"Existing cache: {len(existing):,} bars  "
              f"({existing.index.min()} -> {existing.index.max()})")

    chunks = month_chunks(args.start, args.end)
    print(f"Will fetch {len(chunks)} monthly chunks from {chunks[0][0]} to {chunks[-1][1]}")

    new_frames: list[pd.DataFrame] = []
    for i, (cs, ce) in enumerate(chunks, 1):
        # Skip chunks already covered by cache (cheap check).
        if existing is not None and not existing.empty:
            cov_start = existing.index.min()
            cov_end = existing.index.max()
            chunk_start = pd.Timestamp(cs, tz="UTC")
            chunk_end = pd.Timestamp(ce, tz="UTC") + pd.Timedelta(days=1)
            if chunk_start >= cov_start and chunk_end <= cov_end + pd.Timedelta(minutes=1):
                print(f"[{i:2d}/{len(chunks)}] {cs} -> {ce}  cached, skipping")
                continue

        t0 = time.time()
        try:
            df = fetch_aggs(
                args.ticker, cs, ce,
                multiplier=args.multiplier,
                timespan=args.timespan,
                config=cfg,
            )
        except Exception as exc:  # noqa: BLE001
            print(f"[{i:2d}/{len(chunks)}] {cs} -> {ce}  ERROR: {exc}")
            # Save what we have so far before bailing.
            _save(existing, new_frames, cache)
            return 2

        elapsed = time.time() - t0
        print(f"[{i:2d}/{len(chunks)}] {cs} -> {ce}  {len(df):>6,} bars  ({elapsed:5.2f}s)")

        if not df.empty:
            new_frames.append(df)
            # Incremental save every chunk (cheap at this size).
            _save(existing, new_frames, cache)

        if i < len(chunks):
            time.sleep(args.sleep)

    final = _save(existing, new_frames, cache)
    print(f"\nDone. Cache size: {len(final):,} bars  "
          f"({final.index.min()} -> {final.index.max()})")
    return 0


def _save(
    existing: pd.DataFrame | None,
    new_frames: list[pd.DataFrame],
    cache: Path,
) -> pd.DataFrame:
    parts = [p for p in [existing, *new_frames] if p is not None and not p.empty]
    if not parts:
        return pd.DataFrame()
    combined = pd.concat(parts).sort_index()
    combined = combined[~combined.index.duplicated(keep="last")]
    combined.to_parquet(cache)
    return combined


if __name__ == "__main__":
    raise SystemExit(main())
