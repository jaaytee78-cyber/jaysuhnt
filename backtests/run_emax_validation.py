#!/usr/bin/env python3
"""9/21 EMA crossover validation. Runs at both 5m and 4h."""
from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from asw import data as asw_data, report  # noqa: E402
from asw.backtest import run_backtest as asw_backtest  # noqa: E402
from donchian import data as donchian_data  # noqa: E402
from donchian.backtest import run_backtest as donchian_backtest  # noqa: E402

from emax import params as emax_params  # noqa: E402
from emax.signals import compute_signals  # noqa: E402


def split_is_oos(bars):
    end_dt = bars.index[-1]
    oos_start = end_dt - pd.Timedelta(days=183)
    is_bars = bars[bars.index < oos_start]
    oos_bars = bars[bars.index >= oos_start]
    is_window = (is_bars.index[0].to_pydatetime(), is_bars.index[-1].to_pydatetime())
    oos_window = (oos_bars.index[0].to_pydatetime(), oos_bars.index[-1].to_pydatetime())
    return is_bars, oos_bars, is_window, oos_window


def run_one_tf(tf: str):
    print(f"\n{'='*60}\n  9/21 EMA CROSS -- {tf}\n{'='*60}")
    if tf == "5m":
        bars = asw_data.load_xau_5m()
        p = emax_params.XAU_EMAX_5M_PARAMS
        backtest_fn = asw_backtest
    elif tf == "4h":
        bars = donchian_data.load_xau_4h()
        p = emax_params.XAU_EMAX_4H_PARAMS
        backtest_fn = donchian_backtest
    else:
        raise ValueError(f"unknown tf: {tf}")

    print(f"  bars: {len(bars):,} ({bars.index[0]} -> {bars.index[-1]})")
    is_bars, oos_bars, is_w, oos_w = split_is_oos(bars)
    print(f"  IS  : {is_w[0]} -> {is_w[1]} ({len(is_bars):,} bars)")
    print(f"  OOS : {oos_w[0]} -> {oos_w[1]} ({len(oos_bars):,} bars)")

    def run_split(label, bars_split, notes):
        print(f"\n[{label}] computing signals ...")
        sig = compute_signals(bars_split, p)
        print(f"[{label}]   long fires: {int(sig['signal_long'].sum())}, "
              f"short fires: {int(sig['signal_short'].sum())}")
        print(f"[{label}] running backtest ...")
        trades = backtest_fn(sig, p)
        print(f"[{label}]   trades: {len(trades)}")
        out = (HERE / "reports"
               / f"emax_validation_xau_{tf}_{label}_{date.today().isoformat()}.md")
        report.write_report(
            out_path=out,
            label=f"{tf}_{label}",
            bars_df=bars_split,
            sig_df=sig,
            trades=trades,
            params=p,
            notes=notes,
        )
        print(f"[{label}] -> {out.name}")
        return sig, trades

    is_sig, is_trades = run_split("is", is_bars, f"In-sample {tf} 9/21 EMA cross.")
    oos_sig, oos_trades = run_split("oos", oos_bars, f"OOS held-out {tf}.")

    cmp_path = (HERE / "reports"
                / f"emax_validation_xau_{tf}_compare_{date.today().isoformat()}.md")
    report.write_comparison_report(
        out_path=cmp_path,
        is_trades=is_trades,
        oos_trades=oos_trades,
        is_sig=is_sig,
        oos_sig=oos_sig,
        params=p,
        is_window=is_w,
        oos_window=oos_w,
    )
    print(f"\n  compare -> {cmp_path.name}")


def main():
    run_one_tf("5m")
    run_one_tf("4h")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
