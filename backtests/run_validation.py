#!/usr/bin/env python3
"""PSS validation entry point.

Fetches real 5-minute data from Polygon, runs the bit-exact PSS port
with the current .pine parameters, and writes a markdown validation
report under reports/.

Usage:
    export POLYGON_API_KEY=pk_xxx
    python run_validation.py                       # both instruments, .pine params
    python run_validation.py xau                   # XAU only
    python run_validation.py qqq                   # QQQ (NQ proxy) only
    python run_validation.py --min-score 4         # override min_score for diagnostics

The --min-score override exists for one specific reason: to query a
fired-signal subset directly (e.g. "what if we only took 4/4 fires?")
WITHOUT calling that optimisation. Diagnostic isolation only. The
report filename is suffixed with the override so it never clobbers the
canonical .pine-params report.
"""
from __future__ import annotations

import argparse
import dataclasses
import os
import sys
from datetime import date
from pathlib import Path

# Allow running from repo root or from inside backtests/
HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from pss import data, params, report  # noqa: E402
from pss.backtest import run_backtest  # noqa: E402
from pss.signals import compute_signals  # noqa: E402


INSTRUMENTS = {
    "xau": dict(
        label="XAU/USD",
        polygon_ticker="C:XAUUSD",
        params=params.XAU_PARAMS,
        fetch=data.fetch_xau_5m,
        notes=(
            "Spot gold via Polygon forex. Volume is contributed-bank "
            "tick count, not exchange volume."
        ),
    ),
    "qqq": dict(
        label="QQQ (NQ proxy, RTH only)",
        polygon_ticker="QQQ",
        params=params.QQQ_PARAMS,
        fetch=data.fetch_qqq_5m_rth,
        notes=(
            "QQQ stands in for NQ futures because Polygon free tier "
            "does not include futures. RTH only (13:30-20:00 UTC). "
            "Overnight NQ behaviour is NOT validated."
        ),
    ),
}


def run_one(tag: str, api_key: str, min_score_override=None,
            label: str = "") -> Path:
    spec = INSTRUMENTS[tag]
    p = spec["params"]
    suffix_parts = []
    notes = spec["notes"]
    if min_score_override is not None and min_score_override != p.min_score:
        p = dataclasses.replace(p, min_score=min_score_override)
        suffix_parts.append(f"score{min_score_override}")
        notes = (
            f"{notes}\n\n"
            f"DIAGNOSTIC OVERRIDE: min_score forced to {min_score_override} "
            f"(.pine value is {spec['params'].min_score}). All other params "
            f"unchanged."
        )
    if label:
        suffix_parts.append(label)
    suffix = "_" + "_".join(suffix_parts) if suffix_parts else ""

    print(f"[{tag}] fetching 5m bars ...")
    bars = spec["fetch"](api_key=api_key, years=2)
    print(f"[{tag}]   {len(bars):,} bars from {bars.index[0]} to {bars.index[-1]}")

    print(f"[{tag}] computing signals (min_score={p.min_score}) ...")
    sig = compute_signals(bars, p)
    print(
        f"[{tag}]   long fires: {int(sig['signal_long'].sum()):,}   "
        f"short fires: {int(sig['signal_short'].sum()):,}"
    )

    print(f"[{tag}] running backtest ...")
    trades = run_backtest(sig, p)
    print(f"[{tag}]   trades: {len(trades):,}")

    out = (
        HERE / "reports"
        / f"pss_validation_{tag}{suffix}_{date.today().isoformat()}.md"
    )
    report.write_report(
        out_path=out,
        instrument=spec["label"],
        polygon_ticker=spec["polygon_ticker"],
        bars_df=bars,
        sig_df=sig,
        trades=trades,
        params=p,
        notes=notes,
    )
    print(f"[{tag}] report -> {out}")
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="PSS validation runner")
    parser.add_argument(
        "instruments",
        nargs="*",
        help="instrument tags to run; choose from "
             f"{sorted(INSTRUMENTS.keys())} (default: all)",
    )
    parser.add_argument(
        "--min-score",
        type=int,
        default=None,
        choices=[2, 3, 4],
        help="diagnostic override for min_score (default: use .pine value)",
    )
    parser.add_argument(
        "--label",
        type=str,
        default="",
        help="suffix appended to report filename (e.g. v2_prevdayLevels)",
    )
    args = parser.parse_args()
    invalid = [t for t in args.instruments if t not in INSTRUMENTS]
    if invalid:
        print(f"ERROR: unknown instrument(s): {invalid}", file=sys.stderr)
        return 2

    api_key = os.environ.get("POLYGON_API_KEY", "")
    if not api_key:
        print("ERROR: set POLYGON_API_KEY in your environment.", file=sys.stderr)
        return 2

    targets = args.instruments or list(INSTRUMENTS.keys())
    for tag in targets:
        try:
            run_one(tag, api_key,
                    min_score_override=args.min_score,
                    label=args.label)
        except Exception as exc:
            print(f"[{tag}] FAILED: {exc}", file=sys.stderr)
            import traceback
            traceback.print_exc()
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
