#!/usr/bin/env python3
"""Donchian-4h validation runner. IS = first 18 months, OOS = last 6 months."""
from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from donchian import data, params  # noqa: E402
from donchian.backtest import run_backtest  # noqa: E402
from donchian.signals import compute_signals  # noqa: E402

# Reuse the ASW report writer (now generic re params)
from asw import report  # noqa: E402


def run_split(label, bars, p, notes):
    print(f"[{label}] computing signals on {len(bars):,} 4h bars "
          f"({bars.index[0]} -> {bars.index[-1]}) ...")
    sig = compute_signals(bars, p)
    print(f"[{label}]   long fires: {int(sig['signal_long'].sum())}, "
          f"short fires: {int(sig['signal_short'].sum())}")
    print(f"[{label}] running backtest ...")
    trades = run_backtest(sig, p)
    print(f"[{label}]   trades: {len(trades)}")
    out = (HERE / "reports"
           / f"donchian_validation_xau_{label}_{date.today().isoformat()}.md")
    report.write_report(
        out_path=out,
        label=label,
        bars_df=bars,
        sig_df=sig,
        trades=trades,
        params=p,
        notes=notes,
    )
    print(f"[{label}] report -> {out}")
    return sig, trades


def main():
    print("Loading XAU 4h data (resampled from 5m cache) ...")
    bars = data.load_xau_4h()
    print(f"  {len(bars):,} 4h bars ({bars.index[0]} -> {bars.index[-1]})")
    p = params.XAU_DONCHIAN_PARAMS

    end_dt = bars.index[-1]
    oos_start = end_dt - pd.Timedelta(days=183)
    is_bars = bars[bars.index < oos_start]
    oos_bars = bars[bars.index >= oos_start]

    is_window = (is_bars.index[0].to_pydatetime(), is_bars.index[-1].to_pydatetime())
    oos_window = (oos_bars.index[0].to_pydatetime(), oos_bars.index[-1].to_pydatetime())

    print(f"\nIS  : {is_window[0]} -> {is_window[1]} ({len(is_bars):,} bars)")
    print(f"OOS : {oos_window[0]} -> {oos_window[1]} ({len(oos_bars):,} bars)\n")

    is_sig, is_trades = run_split("is", is_bars, p,
                                  notes="In-sample window. Donchian 4h on XAU.")
    print()
    oos_sig, oos_trades = run_split("oos", oos_bars, p,
                                    notes="Out-of-sample held-out window.")

    cmp_path = (HERE / "reports"
                / f"donchian_validation_xau_compare_{date.today().isoformat()}.md")
    report.write_comparison_report(
        out_path=cmp_path,
        is_trades=is_trades,
        oos_trades=oos_trades,
        is_sig=is_sig,
        oos_sig=oos_sig,
        params=p,
        is_window=is_window,
        oos_window=oos_window,
    )
    print(f"\n[compare] -> {cmp_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
