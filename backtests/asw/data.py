"""Data loader for ASW validation.

Reads from the parquet cache that was populated when PSS validation
ran (backtests/data/xau_5m.parquet). If the cache is missing, instructs
the user how to regenerate it.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def load_xau_5m() -> pd.DataFrame:
    """Load the cached XAU 5m bars (Polygon C:XAUUSD).

    Returns a DataFrame indexed by tz-aware UTC timestamp with columns:
    open, high, low, close, volume.
    """
    p = DATA_DIR / "xau_5m.parquet"
    if not p.exists():
        raise RuntimeError(
            f"XAU data cache not found at {p}.\n"
            f"Regenerate with: cd backtests && "
            f"POLYGON_API_KEY=... python run_validation.py xau"
        )
    df = pd.read_parquet(p)
    if df.index.tz is None:
        df.index = df.index.tz_localize("UTC")
    return df.sort_index()
