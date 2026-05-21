"""Smoke test against synthetic OHLCV.

Not a unit test, not a meaningful backtest -- just confirms the
pipeline runs end-to-end and the report renders without crashing.
Realistic outputs are NOT expected from a random walk; this is purely
to catch import errors, dtype problems, and shape mismatches before
we burn Polygon API calls.

Run: python _smoke_test.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from pss import params  # noqa: E402
from pss.backtest import run_backtest  # noqa: E402
from pss.report import write_report  # noqa: E402
from pss.signals import compute_signals  # noqa: E402


def synth(n_days: int = 60, bars_per_day: int = 78, seed: int = 7) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []
    base = 100.0
    start = pd.Timestamp("2025-01-02 13:30", tz="UTC")
    for d in range(n_days):
        day_start = start + pd.Timedelta(days=d)
        if day_start.dayofweek > 4:
            continue
        for b in range(bars_per_day):
            ts = day_start + pd.Timedelta(minutes=5 * b)
            ret = rng.normal(0, 0.001)
            base = max(1.0, base * (1 + ret))
            spread = abs(rng.normal(0, 0.2))
            o = base + rng.normal(0, 0.05)
            c = base
            h = max(o, c) + spread / 2
            l = min(o, c) - spread / 2
            v = float(rng.integers(100, 5000))
            rows.append((ts, o, h, l, c, v))
    df = pd.DataFrame(rows, columns=["ts", "open", "high", "low", "close", "volume"])
    return df.set_index("ts")


def main() -> int:
    print("Building synthetic 5m bars...")
    df = synth(n_days=80)
    print(f"  {len(df):,} bars: {df.index[0]} -> {df.index[-1]}")

    for label, p in [("XAU", params.XAU_PARAMS), ("QQQ", params.QQQ_PARAMS)]:
        print(f"\n[{label}] computing signals...")
        sig = compute_signals(df, p)
        print(
            f"  long fires: {int(sig['signal_long'].sum())}, "
            f"short fires: {int(sig['signal_short'].sum())}"
        )

        print(f"[{label}] backtest...")
        trades = run_backtest(sig, p)
        print(f"  trades: {len(trades)}")
        if not trades.empty:
            print(f"  total R: {trades['r_realised'].sum():+.2f}")
            print(f"  exit reasons: {dict(trades['exit_reason'].value_counts())}")

        out = HERE / f"_smoke_report_{label.lower()}.md"
        write_report(
            out_path=out,
            instrument=f"SYNTH-{label}",
            polygon_ticker="(synthetic)",
            bars_df=df,
            sig_df=sig,
            trades=trades,
            params=p,
            notes="Smoke test on synthetic random walk -- numbers are meaningless.",
        )
        size = out.stat().st_size
        print(f"  report -> {out.name} ({size:,} bytes)")

    print("\nOK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
