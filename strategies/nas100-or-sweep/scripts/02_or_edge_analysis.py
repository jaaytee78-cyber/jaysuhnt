"""
Phase 1.2 - The core edge analysis.

This script answers the questions that decide whether the strategy is even worth
backtesting in detail.

Answers
-------
1. OR-size distribution (overall, by year, by weekday)
2. P(any sweep occurs in trade window) - sweep rate
3. P(upper sweep first | any sweep)  -- side bias?
4. P(target hit) | sweep                  *** THE EDGE ***
5. Win rate, expectancy, R-distribution given a sweep
6. Same metrics broken down by year and weekday (regime stability)
7. Saves: per-day setup table CSV + summary markdown report.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src import research  # noqa: E402

DATA_PATH = ROOT / "data" / "QQQ_1minute.parquet"
SETUPS_CSV = ROOT / "reports" / "setups.csv"
REPORT_PATH = ROOT / "reports" / "02_edge_analysis.md"


def fmt_pct(x: float) -> str:
    return f"{x * 100:5.2f}%" if pd.notna(x) else "  n/a"


def fmt_R(x: float) -> str:
    return f"{x:+.3f}R" if pd.notna(x) else "  n/a"


def section_header(p, title: str) -> None:
    p("")
    p(f"## {title}")
    p("")


def render_summary_block(p, summary: pd.Series, label: str) -> None:
    p(f"### {label}")
    p("")
    p(f"- Days total              : **{int(summary['days_total'])}**")
    p(f"- Days with a sweep       : **{int(summary['days_with_sweep'])}** "
      f"({fmt_pct(summary['sweep_rate'])} of days)")
    p(f"- P(upper sweep first)    : {fmt_pct(summary['p_upper_first'])}")
    p(f"- P(target hit)           : **{fmt_pct(summary['p_target_hit'])}**")
    p(f"- P(stop hit)             : {fmt_pct(summary['p_stop_hit'])}")
    p(f"- P(timeout / time-stop)  : {fmt_pct(summary['p_timeout'])}")
    p(f"- Win rate (R > 0)        : **{fmt_pct(summary['win_rate'])}**")
    p(f"- Expectancy per setup    : **{fmt_R(summary['expectancy_R'])}**")
    p(f"- Median R                : {fmt_R(summary['median_R'])}")
    p(f"- Avg win / avg loss      : {fmt_R(summary['avg_win_R'])} / {fmt_R(summary['avg_loss_R'])}")
    p(f"- Median OR size          : ${summary['or_size_median']:.2f}")
    p("")


def main() -> int:
    if not DATA_PATH.exists():
        print(f"[error] No data at {DATA_PATH}. Run scripts/fetch_data.py first.")
        return 1

    bars = pd.read_parquet(DATA_PATH)
    if not isinstance(bars.index, pd.DatetimeIndex):
        bars.index = pd.to_datetime(bars.index, utc=True)

    print(f"Loaded {len(bars):,} bars; building per-day setup table...")
    setups = research.build_setup_table(bars)
    if setups.empty:
        print("[error] No setups produced. Check data window vs OR/trade hours.")
        return 1

    SETUPS_CSV.parent.mkdir(parents=True, exist_ok=True)
    setups.to_csv(SETUPS_CSV)
    print(f"Wrote {len(setups)} day-rows to {SETUPS_CSV.relative_to(ROOT)}")

    # Add helper columns for slicing.
    setups = setups.copy()
    setups["year"] = setups.index.year
    setups["weekday"] = setups.index.dayofweek  # 0=Mon ... 4=Fri
    setups["or_size_pct"] = setups["or_size"] / setups["or_open"] * 100  # relative size

    report: list[str] = []
    p = report.append

    p("# OR Sweep & Reversal - Edge Analysis (QQQ 1m)")
    p("")
    p(f"Data window     : {setups.index.min().date()} -> {setups.index.max().date()}")
    p(f"Days with full OR + trade window : **{len(setups)}**")
    p(f"Days with a first sweep          : **{int(setups['sweep_side'].notna().sum())}**")
    p("")
    p("All R-multiples assume:")
    p("- Entry  = close of the sweep bar")
    p("- Stop   = sweep wick + 1 cent")
    p("- Target = opposite OR side")
    p("- Time-stop = 11:00 NY (last bar of trade window)")
    p("- 1 trade per day max, no costs/slippage applied here (pure edge measurement).")

    # ------------------------------------------------------------------ #
    # 1. OR-size distribution
    # ------------------------------------------------------------------ #
    section_header(p, "1. Opening Range size distribution")
    or_desc = setups["or_size"].describe(
        percentiles=[0.1, 0.25, 0.5, 0.75, 0.9]
    )
    p("OR size in dollars (per share, QQQ):")
    p("```")
    p(or_desc.to_string())
    p("```")
    p("")
    p("OR size as % of OR open price:")
    p("```")
    p(setups["or_size_pct"].describe(percentiles=[0.1, 0.5, 0.9]).to_string())
    p("```")

    # ------------------------------------------------------------------ #
    # 2. Sweep frequency
    # ------------------------------------------------------------------ #
    section_header(p, "2. Sweep frequency in [09:45, 11:00) NY")
    n_sweep = int(setups["sweep_side"].notna().sum())
    n_total = int(len(setups))
    p(f"- P(any sweep)         : **{fmt_pct(n_sweep / n_total)}**  "
      f"({n_sweep}/{n_total} days)")
    p(f"- P(upper sweep first) : {fmt_pct((setups['sweep_side'] == 'upper').mean())}")
    p(f"- P(lower sweep first) : {fmt_pct((setups['sweep_side'] == 'lower').mean())}")
    p(f"- P(no sweep)          : {fmt_pct((setups['sweep_side'].isna()).mean())}")

    # ------------------------------------------------------------------ #
    # 3. The headline edge
    # ------------------------------------------------------------------ #
    section_header(p, "3. Headline edge (all sweep days, no filters)")
    summary = research.edge_summary(setups)
    render_summary_block(p, summary, "Pooled - all years, all weekdays")

    if pd.notna(summary["expectancy_R"]):
        if summary["expectancy_R"] > 0.05:
            p("> **Verdict:** positive expectancy.  Worth pushing into Phase 2 backtest.")
        elif summary["expectancy_R"] > -0.05:
            p("> **Verdict:** flat.  Edge depends on filters - investigate breakdowns below.")
        else:
            p("> **Verdict:** negative pooled expectancy.  Strategy as-stated does not work; "
              "either rules need changing (entry timing, target type) or it's a fade.")

    # ------------------------------------------------------------------ #
    # 4. Edge by year
    # ------------------------------------------------------------------ #
    section_header(p, "4. Edge by year (regime stability)")
    rows = []
    for yr, grp in setups.groupby("year"):
        s = research.edge_summary(grp)
        if s.empty:
            continue
        rows.append({
            "year": int(yr),
            "n_days": int(s["days_total"]),
            "sweep_rate": s["sweep_rate"],
            "win_rate": s["win_rate"],
            "expectancy_R": s["expectancy_R"],
            "p_target": s["p_target_hit"],
            "p_stop": s["p_stop_hit"],
        })
    if rows:
        ydf = pd.DataFrame(rows).set_index("year")
        ydf_disp = ydf.copy()
        for c in ["sweep_rate", "win_rate", "p_target", "p_stop"]:
            ydf_disp[c] = (ydf_disp[c] * 100).round(2).astype(str) + "%"
        ydf_disp["expectancy_R"] = ydf["expectancy_R"].round(3).astype(str) + "R"
        p("```")
        p(ydf_disp.to_string())
        p("```")

    # ------------------------------------------------------------------ #
    # 5. Edge by weekday
    # ------------------------------------------------------------------ #
    section_header(p, "5. Edge by weekday")
    weekday_names = {0: "Mon", 1: "Tue", 2: "Wed", 3: "Thu", 4: "Fri"}
    rows = []
    for wd, grp in setups.groupby("weekday"):
        s = research.edge_summary(grp)
        if s.empty:
            continue
        rows.append({
            "weekday": weekday_names.get(int(wd), str(wd)),
            "n_days": int(s["days_total"]),
            "sweep_rate": s["sweep_rate"],
            "win_rate": s["win_rate"],
            "expectancy_R": s["expectancy_R"],
        })
    if rows:
        wdf = pd.DataFrame(rows).set_index("weekday")
        wdf_disp = wdf.copy()
        for c in ["sweep_rate", "win_rate"]:
            wdf_disp[c] = (wdf_disp[c] * 100).round(2).astype(str) + "%"
        wdf_disp["expectancy_R"] = wdf["expectancy_R"].round(3).astype(str) + "R"
        p("```")
        p(wdf_disp.to_string())
        p("```")

    # ------------------------------------------------------------------ #
    # 6. By sweep side (upper vs lower)
    # ------------------------------------------------------------------ #
    section_header(p, "6. Edge by sweep side")
    for side in ("upper", "lower"):
        grp = setups[setups["sweep_side"] == side]
        if grp.empty:
            continue
        s = research.edge_summary(grp)
        render_summary_block(p, s, f"{side.title()} sweep (= {'short' if side == 'upper' else 'long'})")

    # ------------------------------------------------------------------ #
    # 7. R-distribution buckets
    # ------------------------------------------------------------------ #
    section_header(p, "7. R-multiple distribution (sweep days only)")
    sweep_days = setups[setups["sweep_side"].notna()]
    if not sweep_days.empty:
        bins = [-np.inf, -1.0, -0.5, 0.0, 0.5, 1.0, 2.0, np.inf]
        labels = ["<= -1R", "-1R..-0.5R", "-0.5R..0", "0..0.5R",
                  "0.5R..1R", "1R..2R", "> 2R"]
        cuts = pd.cut(sweep_days["r_multiple"], bins=bins, labels=labels, right=True)
        dist = cuts.value_counts().reindex(labels, fill_value=0)
        p("```")
        for lbl, n in dist.items():
            pct = n / len(sweep_days)
            p(f"  {lbl:<12} {n:4d}   ({pct * 100:5.2f}%)")
        p("```")

    # ------------------------------------------------------------------ #
    # 8. Time-to-target distribution
    # ------------------------------------------------------------------ #
    section_header(p, "8. Time-to-target (winners only)")
    winners = setups[setups["target_hit"]]
    if not winners.empty:
        ttt = winners["bars_to_target"].dropna()
        p("```")
        p(ttt.describe(percentiles=[0.25, 0.5, 0.75, 0.9]).to_string())
        p("```")
        p(f"Implied: most winners hit target within "
          f"~{int(ttt.median())} minutes of the sweep bar.")

    text = "\n".join(report)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(text)
    print("\n" + text)
    print(f"\nReport saved to {REPORT_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
