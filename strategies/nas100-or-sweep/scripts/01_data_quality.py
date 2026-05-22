"""
Phase 1.1 - Data quality report.

Answers:
  - How many trading days are in the cache?
  - Do we have a complete 09:30-09:45 OR window for each day?
  - Bar-count distribution per day (full RTH = 390 minutes)
  - Volume sanity: are there suspicious low-volume / halt days?
  - Are there gaps between consecutive sessions (missing days)?
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src import sessions  # noqa: E402

DATA_PATH = ROOT / "data" / "QQQ_1minute.parquet"
REPORT_PATH = ROOT / "reports" / "01_data_quality.md"


def main() -> int:
    if not DATA_PATH.exists():
        print(f"[error] No data at {DATA_PATH}. Run scripts/fetch_data.py first.")
        return 1

    bars = pd.read_parquet(DATA_PATH)
    if not isinstance(bars.index, pd.DatetimeIndex):
        bars.index = pd.to_datetime(bars.index, utc=True)

    report: list[str] = []
    p = report.append

    p("# Data Quality Report")
    p(f"Source: `{DATA_PATH.relative_to(ROOT)}`")
    p(f"Total bars: **{len(bars):,}**")
    p(f"Range: **{bars.index.min()}** -> **{bars.index.max()}**")
    p("")

    # --- Daily summary --------------------------------------------------------
    rth = sessions.regular_session(bars)
    rth_with_date = rth.copy()
    rth_with_date["ny_date"] = rth.index.tz_convert(sessions.NY_TZ).date
    daily = (
        rth_with_date.groupby("ny_date")
        .agg(rth_bars=("close", "size"), rth_volume=("volume", "sum"))
    )
    p("## Regular-session daily summary")
    p(f"Trading days seen: **{len(daily)}**")
    p(f"Avg RTH bars/day: **{daily['rth_bars'].mean():.1f}**  (full session = 390)")
    p(f"Median RTH bars/day: **{daily['rth_bars'].median():.0f}**")
    p(f"Days with <380 RTH bars (likely halts/half-days): "
      f"**{int((daily['rth_bars'] < 380).sum())}**")
    p("")

    # --- OR coverage ---------------------------------------------------------
    or_window = sessions.opening_range_window(bars)
    or_window_with_date = or_window.copy()
    or_window_with_date["ny_date"] = (
        or_window.index.tz_convert(sessions.NY_TZ).date
    )
    or_per_day = or_window_with_date.groupby("ny_date").size()
    full_or_days = int((or_per_day == 15).sum())
    partial_or_days = int(((or_per_day < 15) & (or_per_day > 0)).sum())
    p("## Opening Range coverage (09:30-09:44:59 NY)")
    p(f"Days with full 15-bar OR: **{full_or_days}**")
    p(f"Days with partial OR (1-14 bars): **{partial_or_days}**")
    p(f"Days with zero OR bars: **{int(len(daily) - (full_or_days + partial_or_days))}**")
    p("")

    # --- Calendar gaps -------------------------------------------------------
    if len(daily) > 1:
        idx = pd.DatetimeIndex(daily.index)
        # US business days between first and last date
        bdays = pd.bdate_range(idx.min(), idx.max())
        missing = sorted(set(pd.to_datetime(bdays.date)) - set(pd.to_datetime(idx)))
        p("## Calendar coverage")
        p(f"Business days in range: **{len(bdays)}**")
        p(f"Days present in cache: **{len(daily)}**")
        p(f"Missing business days: **{len(missing)}**  "
          "(US market holidays will appear here, plus any data gaps)")
        if missing:
            p("")
            p("First 10 missing dates: " + ", ".join(d.strftime("%Y-%m-%d") for d in missing[:10]))
        p("")

    # --- Suspicious days -----------------------------------------------------
    if len(daily) > 0:
        median_vol = daily["rth_volume"].median()
        suspicious = daily[daily["rth_volume"] < 0.3 * median_vol]
        p("## Low-volume / suspicious days")
        p(f"Median daily RTH volume: **{median_vol:,.0f}** shares")
        p(f"Days with <30% of median volume: **{len(suspicious)}**")
        if len(suspicious) > 0 and len(suspicious) <= 20:
            p("")
            for d, row in suspicious.iterrows():
                p(f"- {d}: {int(row['rth_bars'])} bars, vol={int(row['rth_volume']):,}")
        p("")

    text = "\n".join(report)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(text)
    print(text)
    print(f"\nReport saved to {REPORT_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
