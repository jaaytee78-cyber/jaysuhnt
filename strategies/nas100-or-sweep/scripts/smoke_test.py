"""Smoke test: verify imports + sessions logic without hitting Polygon."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src import data, sessions  # noqa: E402


def synthetic_minute_bars(date: str = "2024-06-03") -> pd.DataFrame:
    """Build one trading day of synthetic 1-minute bars (NY 04:00 -> 20:00)."""
    start = pd.Timestamp(f"{date} 04:00", tz="America/New_York").tz_convert("UTC")
    idx = pd.date_range(start=start, periods=16 * 60, freq="1min", tz="UTC")
    rng = np.random.default_rng(42)
    closes = 400 + np.cumsum(rng.normal(0, 0.05, len(idx)))
    return pd.DataFrame(
        {
            "open": closes - 0.02,
            "high": closes + 0.05,
            "low": closes - 0.05,
            "close": closes,
            "volume": rng.integers(1000, 10000, len(idx)),
            "vwap": closes,
            "transactions": rng.integers(10, 200, len(idx)),
        },
        index=pd.DatetimeIndex(idx, name="ts"),
    )


def main() -> int:
    print(f"data module       : {data.__file__}")
    print(f"sessions module   : {sessions.__file__}")
    print(f"NY_TZ             : {sessions.NY_TZ}")
    print(f"OR window (NY)    : {sessions.OR_START} -> {sessions.OR_END}")
    print(f"Trade window (NY) : {sessions.TRADE_START} -> {sessions.TRADE_END}")

    df = synthetic_minute_bars()
    print(f"\nSynthetic bars    : {len(df):,} rows  ({df.index.min()} -> {df.index.max()})")

    rth = sessions.regular_session(df)
    or_win = sessions.opening_range_window(df)
    tw = sessions.trade_window(df)
    print(f"Regular session   : {len(rth)} bars   (expect ~390)")
    print(f"Opening range win : {len(or_win)} bars   (expect 15)")
    print(f"Trade window      : {len(tw)} bars    (expect 75)")

    or_table = sessions.opening_ranges(df)
    print("\nopening_ranges() output:")
    print(or_table)

    # Sanity: OR high/low must equal max/min over the OR window.
    expected_high = or_win["high"].max()
    expected_low = or_win["low"].min()
    actual_high = float(or_table["or_high"].iloc[0])
    actual_low = float(or_table["or_low"].iloc[0])
    assert np.isclose(actual_high, expected_high), (actual_high, expected_high)
    assert np.isclose(actual_low, expected_low), (actual_low, expected_low)
    assert int(or_table["n_bars"].iloc[0]) == 15

    # Killzones smoke check.
    ny_am = sessions.in_killzone(df, "ny_am")
    asia = sessions.in_killzone(df, "asia")  # tests wrap-around
    print(f"\nKillzone ny_am    : {len(ny_am)} bars   (expect 240, 07:00-11:00)")
    print(f"Killzone asia     : {len(asia)} bars   (covers 04:00 hour from this day's frame)")

    # Verify fetch_aggs still surfaces a clear error without an API key.
    try:
        data.PolygonConfig.from_env()
    except RuntimeError as exc:
        print(f"\nNo-API-key path OK: {exc}")
    else:
        print("\nWARNING: expected RuntimeError without POLYGON_API_KEY")

    print("\nSmoke test PASSED.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
