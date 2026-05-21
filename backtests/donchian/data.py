"""Data loader: resamples the cached 5m XAU parquet to 4h bars."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def load_xau_4h() -> pd.DataFrame:
    """Load 5m XAU bars from the cache and resample to 4h.

    Resample anchored at 00:00 UTC so the bars line up with the
    standard 4h chart on TradingView.
    """
    p = DATA_DIR / "xau_5m.parquet"
    if not p.exists():
        raise RuntimeError(
            f"XAU 5m cache not found at {p}.\n"
            f"Run: cd backtests && POLYGON_API_KEY=... python run_validation.py xau"
        )
    df = pd.read_parquet(p)
    if df.index.tz is None:
        df.index = df.index.tz_localize("UTC")
    df = df.sort_index()

    agg = df.resample("4h", label="left", closed="left").agg(
        open=("open", "first"),
        high=("high", "max"),
        low=("low", "min"),
        close=("close", "last"),
        volume=("volume", "sum"),
    )
    # Drop bars with no underlying 5m data (weekends, market closes)
    agg = agg.dropna(subset=["close"])
    return agg
