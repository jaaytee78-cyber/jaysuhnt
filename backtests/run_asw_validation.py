#!/usr/bin/env python3
"""ASW validation entry point.

Reads cached XAU 5m data, splits into IS (18 months) and OOS (last 6
months held out), runs both, writes three reports:

  - asw_validation_xau_is_<date>.md
  - asw_validation_xau_oos_<date>.md
  - asw_validation_xau_compare_<date>.md
"""
from __future__ import annotations

import argparse
import sys
from datetime import date, datetime, timezone, timedelta
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from asw import data, params, report  # noqa: E402
from asw.backtest import run_backtest  # noqa: E402
from asw.signals import compute_signals  # noqa: E402


def run_split(
    label: str,
    bars: pd.DataFrame,
    p,
    notes: str,
    suffix: str = "",
) -> tuple:
    print(f"[{label}] computing signals on {len(bars):,} bars "
          f"({bars.index[0]} -> {bars.index[-1]}) ...")
    sig = compute_signals(bars, p)
    print(f"[{label}]   long fires: {int(sig['signal_long'].sum())}, "
          f"short fires: {int(sig['signal_short'].sum())}")

    print(f"[{label}] running backtest ...")
    trades = run_backtest(sig, p)
    print(f"[{label}]   trades: {len(trades)}")

    out = (HERE / "reports"
           / f"asw_validation_xau_{label}{suffix}_{date.today().isoformat()}.md")
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
    return sig, trades, out


def main() -> int:
    parser = argparse.ArgumentParser(description="ASW validation runner")
    parser.add_argument(
        "--target-mode",
        choices=["asian_range", "fixed_rr"],
        default=None,
        help="Override target_mode; default uses params.XAU_ASW_PARAMS",
    )
    parser.add_argument(
        "--label-suffix",
        default="",
        help="Suffix appended to report filenames (e.g. _fixedrr)",
    )
    args = parser.parse_args()

    p = params.XAU_ASW_PARAMS
    if args.target_mode is not None:
        import dataclasses
        p = dataclasses.replace(p, target_mode=args.target_mode)

    suffix = args.label_suffix
    if suffix and not suffix.startswith("_"):
        suffix = "_" + suffix

    print("Loading XAU 5m data ...")
    bars = data.load_xau_5m()
    if bars.index.tz is None:
        bars.index = bars.index.tz_localize("UTC")
    print(f"  {len(bars):,} bars loaded "
          f"({bars.index[0]} -> {bars.index[-1]})")

    # Split: last 6 months OOS, prior 18 months IS
    end_dt = bars.index[-1]
    oos_start = end_dt - pd.Timedelta(days=183)  # ~6 months
    is_bars = bars[bars.index < oos_start]
    oos_bars = bars[bars.index >= oos_start]

    is_window = (is_bars.index[0].to_pydatetime(), is_bars.index[-1].to_pydatetime())
    oos_window = (oos_bars.index[0].to_pydatetime(), oos_bars.index[-1].to_pydatetime())

    print(f"\nSplit:\n  IS : {is_window[0]} -> {is_window[1]} "
          f"({len(is_bars):,} bars)\n  OOS: {oos_window[0]} -> {oos_window[1]} "
          f"({len(oos_bars):,} bars)\n")

    is_sig, is_trades, _ = run_split(
        "is", is_bars, p,
        notes=f"In-sample window. target_mode={p.target_mode}. "
              f"OOS window held out separately.",
        suffix=suffix,
    )
    print()
    oos_sig, oos_trades, _ = run_split(
        "oos", oos_bars, p,
        notes=f"Out-of-sample held-out window. target_mode={p.target_mode}. "
              f"Strategy was NOT tuned on this window.",
        suffix=suffix,
    )

    cmp_path = (HERE / "reports"
                / f"asw_validation_xau_compare{suffix}_{date.today().isoformat()}.md")
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
    print(f"\n[compare] report -> {cmp_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
