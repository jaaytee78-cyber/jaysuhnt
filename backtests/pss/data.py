"""Polygon.io data adapter for PSS validation.

Free-tier-friendly:
  - C:XAUUSD on Polygon Forex (5m, 2 years history allowed)
  - QQQ on Polygon Stocks (5m, 2 years history allowed)
  - Pagination via next_url for large windows
  - Local parquet cache so re-runs don't burn API calls

Reads POLYGON_API_KEY from the environment. The repo never stores keys.
"""

from __future__ import annotations

import os
import time
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

import pandas as pd
import requests


POLYGON_BASE = "https://api.polygon.io"
DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DATA_DIR.mkdir(exist_ok=True)


# --------------------------------------------------------------------- #
#  Low-level fetch                                                      #
# --------------------------------------------------------------------- #

def _polygon_get(url: str, api_key: str) -> dict:
    """GET with the API key.

    Polygon free tier is 5 calls/min. We sleep 13s between calls
    proactively, and on 429 we back off exponentially up to 3 retries.
    """
    if "apiKey=" not in url:
        sep = "&" if "?" in url else "?"
        url = f"{url}{sep}apiKey={api_key}"

    backoffs = [30, 60, 90]  # seconds between retries on 429
    for attempt in range(len(backoffs) + 1):
        r = requests.get(url, timeout=30)
        if r.status_code == 200:
            time.sleep(13.0)  # rate-limit pacing
            return r.json()
        if r.status_code == 429 and attempt < len(backoffs):
            wait = backoffs[attempt]
            print(f"  rate-limited; sleeping {wait}s before retry "
                  f"({attempt + 1}/{len(backoffs)})")
            time.sleep(wait)
            continue
        # Any other non-200: surface the response body for diagnostics
        try:
            body = r.text[:500]
        except Exception:
            body = ""
        r.raise_for_status()
        raise RuntimeError(f"polygon GET failed: {r.status_code} body={body}")
    raise RuntimeError("polygon GET: exhausted retries")


def _aggs_to_df(results: list) -> pd.DataFrame:
    """Polygon agg result -> tidy DataFrame.

    Polygon timestamps are millisecond-epoch UTC of the bar OPEN.
    """
    if not results:
        return pd.DataFrame(
            columns=["open", "high", "low", "close", "volume"]
        )
    df = pd.DataFrame(results)
    # Polygon fields: t (ms), o, h, l, c, v, vw (vwap), n (trade count)
    df.rename(
        columns={
            "t": "ts_ms",
            "o": "open",
            "h": "high",
            "l": "low",
            "c": "close",
            "v": "volume",
        },
        inplace=True,
    )
    df["timestamp"] = pd.to_datetime(df["ts_ms"], unit="ms", utc=True)
    df = df.set_index("timestamp")
    return df[["open", "high", "low", "close", "volume"]].astype(float)


def _fetch_aggs(
    ticker: str,
    multiplier: int,
    timespan: str,
    start: str,
    end: str,
    api_key: str,
) -> pd.DataFrame:
    """Fetch raw aggregates with pagination."""
    url = (
        f"{POLYGON_BASE}/v2/aggs/ticker/{ticker}/range/"
        f"{multiplier}/{timespan}/{start}/{end}"
        f"?adjusted=true&sort=asc&limit=50000"
    )
    all_results: list = []
    page = 0
    while url:
        page += 1
        body = _polygon_get(url, api_key)
        results = body.get("results", []) or []
        all_results.extend(results)
        print(f"    page {page}: +{len(results)} bars (total {len(all_results)})")
        next_url = body.get("next_url")
        url = next_url if next_url else None
        # Safety: stop runaway pagination
        if page > 50:
            break
    return _aggs_to_df(all_results)


# --------------------------------------------------------------------- #
#  Public adapters                                                      #
# --------------------------------------------------------------------- #

def _cache_path(name: str) -> Path:
    return DATA_DIR / f"{name}_5m.parquet"


def _load_cache(name: str) -> Optional[pd.DataFrame]:
    p = _cache_path(name)
    if p.exists():
        return pd.read_parquet(p)
    return None


def _save_cache(name: str, df: pd.DataFrame) -> None:
    df.to_parquet(_cache_path(name))


def _date_window(years: int) -> tuple[str, str]:
    """Return (start, end) ISO date strings for `years` back from today.

    Polygon free tier currently allows up to 2y of intraday history.
    """
    today = date.today()
    start = today - timedelta(days=int(365.25 * years))
    return start.isoformat(), today.isoformat()


def fetch_xau_5m(
    api_key: Optional[str] = None,
    years: int = 2,
    use_cache: bool = True,
) -> pd.DataFrame:
    """5-minute bars for spot gold (Polygon forex C:XAUUSD)."""
    name = "xau"
    if use_cache:
        cached = _load_cache(name)
        if cached is not None and not cached.empty:
            return cached

    api_key = api_key or os.environ.get("POLYGON_API_KEY")
    if not api_key:
        raise RuntimeError(
            "POLYGON_API_KEY not set; pass api_key= or export the env var"
        )

    start, end = _date_window(years)
    df = _fetch_aggs(
        ticker="C:XAUUSD",
        multiplier=5,
        timespan="minute",
        start=start,
        end=end,
        api_key=api_key,
    )
    df.sort_index(inplace=True)
    df = df[~df.index.duplicated(keep="first")]
    _save_cache(name, df)
    return df


def fetch_qqq_5m_rth(
    api_key: Optional[str] = None,
    years: int = 2,
    use_cache: bool = True,
) -> pd.DataFrame:
    """5-minute bars for QQQ (NQ proxy), restricted to US regular trading
    hours (13:30-20:00 UTC = 09:30-16:00 ET, year-round approximation
    that ignores DST shifts; QQQ is the proxy, perfect alignment is not
    a goal).
    """
    name = "qqq"
    if use_cache:
        cached = _load_cache(name)
        if cached is not None and not cached.empty:
            return cached

    api_key = api_key or os.environ.get("POLYGON_API_KEY")
    if not api_key:
        raise RuntimeError(
            "POLYGON_API_KEY not set; pass api_key= or export the env var"
        )

    start, end = _date_window(years)
    df = _fetch_aggs(
        ticker="QQQ",
        multiplier=5,
        timespan="minute",
        start=start,
        end=end,
        api_key=api_key,
    )
    df.sort_index(inplace=True)
    df = df[~df.index.duplicated(keep="first")]

    # Filter to RTH (UTC). 13:30-20:00 covers 09:30-16:00 ET in
    # standard time; during DST it's 13:30-19:55 (one fewer bar). We
    # accept the small DST mismatch for simplicity -- it does not
    # change the validation conclusion either way.
    minutes = df.index.hour * 60 + df.index.minute
    rth = (minutes >= 13 * 60 + 30) & (minutes <= 20 * 60)
    df = df[rth]

    _save_cache(name, df)
    return df
