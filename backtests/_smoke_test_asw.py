"""End-to-end smoke test for the ASW pipeline on synthetic OHLCV.

Confirms the package imports, signals fire on synthetic data, the
backtest produces trades, and the report renders without errors.
Realistic outputs are NOT expected from a random walk -- this is just
a "no crash" check before touching real data.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from asw import params, report  # noqa: E402
from asw.backtest import run_backtest  # noqa: E402
from asw.signals import compute_signals  # noqa: E402


def synth_xau(n_days: int = 60, seed: int = 7) -> pd.DataFrame:
    """24-hour 5m bars with random walk close around 2000."""
    rng = np.random.default_rng(seed)
    rows = []
    base = 2000.0
    start = pd.Timestamp("2025-01-01 00:00", tz="UTC")
    bars_per_day = 24 * 12  # 288 5m bars
    for d in range(n_days):
        for b in range(bars_per_day):
            ts = start + pd.Timedelta(days=d, minutes=5 * b)
            ret = rng.normal(0, 0.0008)  # 8 bps stdev per bar
            base = max(1.0, base * (1 + ret))
            rng_bar = abs(rng.normal(0, 1.0))
            o = base + rng.normal(0, 0.3)
            c = base
            h = max(o, c) + rng_bar / 2
            l = min(o, c) - rng_bar / 2
            v = float(rng.integers(50, 500))
            rows.append((ts, o, h, l, c, v))
    df = pd.DataFrame(
        rows, columns=["ts", "open", "high", "low", "close", "volume"]
    ).set_index("ts")
    return df


def main() -> int:
    print("Building synthetic 24h XAU bars ...")
    df = synth_xau(n_days=60)
    print(f"  {len(df):,} bars: {df.index[0]} -> {df.index[-1]}")

    p = params.XAU_ASW_PARAMS
    print(f"\nUsing params (target_mode={p.target_mode}):")
    print(f"  asia {p.asia_start_utc:02d}:00 -> {p.asia_end_utc:02d}:00 UTC")
    print(f"  trade window {p.asia_end_utc:02d}:00 -> {p.trade_cutoff_utc:02d}:00 UTC")

    print("\nComputing signals ...")
    sig = compute_signals(df, p)
    print(f"  long fires: {int(sig['signal_long'].sum())}")
    print(f"  short fires: {int(sig['signal_short'].sum())}")

    print("\nBacktest ...")
    trades = run_backtest(sig, p)
    print(f"  trades: {len(trades)}")
    if not trades.empty:
        print(f"  total R: {trades['r_realised'].sum():+.2f}")
        print(f"  WR: {(trades['r_realised'] > 0).mean()*100:.1f}%")
        print(f"  exit reasons: {dict(trades['exit_reason'].value_counts())}")

    print("\nWrite report ...")
    out = HERE / "_smoke_report_asw.md"
    report.write_report(
        out_path=out,
        label="smoke",
        bars_df=df,
        sig_df=sig,
        trades=trades,
        params=p,
        notes="Synthetic random walk; numbers are meaningless",
    )
    print(f"  -> {out.name} ({out.stat().st_size:,} bytes)")
    print("\nOK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
