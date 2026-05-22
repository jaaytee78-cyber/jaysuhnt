"""
Polygon.io aggregate-bar loader with on-disk parquet cache.

Design goals
------------
- **Transparency.** No SDK magic; we hit the REST endpoint directly so it's
  obvious what we're requesting and what we get back.
- **Pagination.** Polygon caps each page at 50,000 rows and returns a
  ``next_url``; we follow it until exhausted.
- **Rate-limit awareness.** Free tier is 5 calls/min. We sleep on 429 and
  optionally throttle preemptively.
- **Cache by default.** Bars are written to ``data/{ticker}_{mult}{span}.parquet``
  and re-used on subsequent calls; only missing date ranges are fetched.

Usage
-----
>>> from src.data import load_aggs
>>> df = load_aggs("QQQ", "2024-01-01", "2024-01-31")  # 1-minute bars by default
"""
from __future__ import annotations

import os
import time
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

import httpx
import pandas as pd
from dotenv import load_dotenv

POLYGON_BASE = "https://api.polygon.io"
DEFAULT_TIMEOUT = 30.0
DEFAULT_DATA_DIR = Path(__file__).resolve().parent.parent / "data"


# --------------------------------------------------------------------------- #
# Config
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class PolygonConfig:
    api_key: str
    base_url: str = POLYGON_BASE
    timeout: float = DEFAULT_TIMEOUT
    # If True, sleep between pages to stay under free-tier 5 req/min limit.
    free_tier_throttle: bool = False

    @classmethod
    def from_env(cls, free_tier_throttle: bool = False) -> "PolygonConfig":
        load_dotenv()
        key = os.getenv("POLYGON_API_KEY")
        if not key or key == "your_polygon_api_key_here":
            raise RuntimeError(
                "POLYGON_API_KEY not set. Copy .env.example to .env and add your key."
            )
        return cls(api_key=key, free_tier_throttle=free_tier_throttle)


# --------------------------------------------------------------------------- #
# Low-level fetch
# --------------------------------------------------------------------------- #
def _to_iso_date(d: str | date | datetime) -> str:
    """Normalise input to YYYY-MM-DD string (Polygon range endpoint format)."""
    if isinstance(d, str):
        return d  # trust the caller
    if isinstance(d, datetime):
        return d.date().isoformat()
    return d.isoformat()


def fetch_aggs(
    ticker: str,
    start: str | date | datetime,
    end: str | date | datetime,
    multiplier: int = 1,
    timespan: str = "minute",
    *,
    adjusted: bool = True,
    config: PolygonConfig | None = None,
) -> pd.DataFrame:
    """
    Fetch raw aggregate bars from Polygon, following pagination.

    Returns a DataFrame indexed by UTC timestamp with columns:
    ``open, high, low, close, volume, vwap, transactions``.
    """
    cfg = config or PolygonConfig.from_env()
    url = (
        f"{cfg.base_url}/v2/aggs/ticker/{ticker.upper()}/range/"
        f"{multiplier}/{timespan}/{_to_iso_date(start)}/{_to_iso_date(end)}"
    )
    params: dict[str, str | int] = {
        "adjusted": str(adjusted).lower(),
        "sort": "asc",
        "limit": 50_000,
    }

    rows: list[dict] = []
    with httpx.Client(timeout=cfg.timeout) as client:
        while url:
            resp = client.get(
                url,
                params={**params, "apiKey": cfg.api_key} if "apiKey" not in url else {"apiKey": cfg.api_key},
            )

            # Handle rate limiting gracefully (free tier especially).
            if resp.status_code == 429:
                time.sleep(13)  # 5 req/min => ~12s spacing; pad a bit
                continue
            resp.raise_for_status()

            payload = resp.json()
            rows.extend(payload.get("results", []) or [])

            next_url = payload.get("next_url")
            if not next_url:
                break

            # next_url already contains query params; we only re-attach apiKey.
            url = next_url
            params = {}  # consumed; further params come from next_url

            if cfg.free_tier_throttle:
                time.sleep(13)

    if not rows:
        return _empty_aggs_frame()

    return _normalise_aggs(rows)


def _empty_aggs_frame() -> pd.DataFrame:
    return pd.DataFrame(
        columns=["open", "high", "low", "close", "volume", "vwap", "transactions"],
        index=pd.DatetimeIndex([], tz="UTC", name="ts"),
    )


def _normalise_aggs(rows: list[dict]) -> pd.DataFrame:
    """Convert Polygon's compact JSON to a tidy, UTC-indexed OHLCV DataFrame."""
    df = pd.DataFrame(rows)
    df = df.rename(
        columns={
            "t": "ts_ms",
            "o": "open",
            "h": "high",
            "l": "low",
            "c": "close",
            "v": "volume",
            "vw": "vwap",
            "n": "transactions",
        }
    )
    df["ts"] = pd.to_datetime(df["ts_ms"], unit="ms", utc=True)
    df = df.drop(columns=["ts_ms"]).set_index("ts").sort_index()
    # Drop any duplicates (Polygon occasionally double-reports on page boundaries).
    df = df[~df.index.duplicated(keep="first")]
    keep = ["open", "high", "low", "close", "volume", "vwap", "transactions"]
    return df[[c for c in keep if c in df.columns]]


# --------------------------------------------------------------------------- #
# Cache layer
# --------------------------------------------------------------------------- #
def _cache_path(ticker: str, multiplier: int, timespan: str, data_dir: Path) -> Path:
    return data_dir / f"{ticker.upper()}_{multiplier}{timespan}.parquet"


def load_aggs(
    ticker: str,
    start: str | date | datetime,
    end: str | date | datetime,
    multiplier: int = 1,
    timespan: str = "minute",
    *,
    adjusted: bool = True,
    data_dir: Path | None = None,
    config: PolygonConfig | None = None,
    refresh: bool = False,
) -> pd.DataFrame:
    """
    Load aggregate bars, transparently using/extending an on-disk parquet cache.

    Parameters
    ----------
    refresh : bool
        If True, ignore the cache and re-fetch the full range.
    """
    data_dir = data_dir or DEFAULT_DATA_DIR
    data_dir.mkdir(parents=True, exist_ok=True)
    path = _cache_path(ticker, multiplier, timespan, data_dir)

    requested_start = pd.Timestamp(_to_iso_date(start), tz="UTC")
    # End is inclusive on Polygon's API; treat as end-of-day in UTC for caching.
    requested_end = pd.Timestamp(_to_iso_date(end), tz="UTC") + pd.Timedelta(days=1)

    cached: pd.DataFrame | None = None
    if path.exists() and not refresh:
        cached = pd.read_parquet(path)
        if not isinstance(cached.index, pd.DatetimeIndex):
            cached.index = pd.to_datetime(cached.index, utc=True)

    needed_ranges = _missing_ranges(cached, requested_start, requested_end)
    new_frames: list[pd.DataFrame] = []
    for r_start, r_end in needed_ranges:
        df = fetch_aggs(
            ticker,
            r_start.date(),
            (r_end - pd.Timedelta(days=1)).date(),
            multiplier=multiplier,
            timespan=timespan,
            adjusted=adjusted,
            config=config,
        )
        if not df.empty:
            new_frames.append(df)

    parts = [p for p in [cached, *new_frames] if p is not None and not p.empty]
    if not parts:
        return _empty_aggs_frame()

    combined = pd.concat(parts).sort_index()
    combined = combined[~combined.index.duplicated(keep="last")]

    # Persist updated cache (full file rewrite — fine at our data sizes).
    combined.to_parquet(path)

    # Slice to the requested window only.
    return combined.loc[(combined.index >= requested_start) & (combined.index < requested_end)]


def _missing_ranges(
    cached: pd.DataFrame | None,
    start: pd.Timestamp,
    end: pd.Timestamp,
) -> list[tuple[pd.Timestamp, pd.Timestamp]]:
    """
    Determine which date ranges still need to be fetched.

    Strategy: figure out the gap before the cache and the gap after; we don't
    try to patch interior holes (Polygon is reliable for completed sessions).
    """
    if cached is None or cached.empty:
        return [(start, end)]

    cache_start = cached.index.min()
    cache_end = cached.index.max() + pd.Timedelta(minutes=1)

    gaps: list[tuple[pd.Timestamp, pd.Timestamp]] = []
    if start < cache_start:
        gaps.append((start, min(cache_start, end)))
    if end > cache_end:
        gaps.append((max(cache_end, start), end))
    return gaps
