"""
Phase 1.3 - Variant grid: stop/target/entry ablations + costs + bootstrap CIs.

Runs each ``VariantConfig`` from ``research.standard_variants()`` twice:
  1. Without execution costs (gross edge)
  2. With $0.01/share slippage each side (net edge)

For each run we report:
  - Sample size, win rate, P(target/stop/timeout)
  - Mean R-multiple with 95% bootstrap CI
  - Median R, avg win, avg loss
  - Whether the CI crosses zero (= can't reject "no edge")

Outputs:
  reports/03_variant_grid.md          human-readable comparison report
  reports/variant_summary.csv         machine-readable for further analysis
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src import bootstrap, research  # noqa: E402

DATA_PATH = ROOT / "data" / "QQQ_1minute.parquet"
REPORT_PATH = ROOT / "reports" / "03_variant_grid.md"
SUMMARY_CSV = ROOT / "reports" / "variant_summary.csv"

SLIPPAGE_PER_SHARE = 0.01  # $ per share each side
N_BOOTSTRAP = 5000


def fmt_pct(x: float) -> str:
    return f"{x * 100:5.2f}%" if pd.notna(x) else "  n/a"


def fmt_R(x: float) -> str:
    return f"{x:+.3f}R" if pd.notna(x) else "  n/a"


def evaluate_variant(
    bars: pd.DataFrame,
    variant: research.VariantConfig,
    costs: research.CostConfig,
) -> dict:
    """Run a single variant + cost config, return a flat dict of metrics."""
    setups = research.build_setup_table(bars, config=variant, costs=costs)
    if setups.empty:
        return {"variant": variant.name, "n": 0}

    entries = setups[setups["sweep_side"].notna()].copy()
    if entries.empty:
        return {
            "variant": variant.name,
            "cost_per_rt": costs.per_round_trip,
            "n_days": int(len(setups)),
            "n_entries": 0,
        }

    r = entries["r_multiple"].dropna().to_numpy()
    boot = bootstrap.bootstrap_mean(r, n_iter=N_BOOTSTRAP)
    wins = (entries["r_multiple"] > 0).to_numpy()
    wr = bootstrap.bootstrap_win_rate(wins, n_iter=N_BOOTSTRAP)

    return {
        "variant": variant.name,
        "description": variant.description,
        "cost_per_rt": costs.per_round_trip,
        "n_days": int(len(setups)),
        "n_entries": int(len(entries)),
        "entry_rate": len(entries) / len(setups),
        "p_target": float(entries["target_hit"].mean()),
        "p_stop": float(entries["stop_hit"].mean()),
        "p_timeout": float(entries["timed_out"].mean()),
        "expectancy_R": boot.statistic,
        "expectancy_ci_low": boot.ci_low,
        "expectancy_ci_high": boot.ci_high,
        "expectancy_significant": not boot.crosses_zero,
        "win_rate": wr.statistic,
        "win_rate_ci_low": wr.ci_low,
        "win_rate_ci_high": wr.ci_high,
        "median_R": float(entries["r_multiple"].median()),
        "avg_win_R": float(entries.loc[entries["r_multiple"] > 0, "r_multiple"].mean())
            if wins.any() else float("nan"),
        "avg_loss_R": float(entries.loc[entries["r_multiple"] < 0, "r_multiple"].mean())
            if (entries["r_multiple"] < 0).any() else float("nan"),
        "median_risk_$": float(entries["risk"].median()),
    }


def render_table(results: list[dict], title: str) -> str:
    """Pretty-print a results table for inclusion in the markdown report."""
    if not results:
        return f"## {title}\n\n(no results)\n"

    lines = [f"## {title}", ""]
    header = (
        "| Variant | N | Win % | P(tgt) | P(stop) | "
        "Exp R (95% CI) | Sig? | Avg Win | Avg Loss | Median R | Risk $ |"
    )
    sep = "|---|---|---|---|---|---|---|---|---|---|---|"
    lines.append(header)
    lines.append(sep)
    for r in results:
        if r.get("n_entries", 0) == 0:
            lines.append(f"| **{r['variant']}** | 0 | - | - | - | - | - | - | - | - | - |")
            continue
        ci = f"{r['expectancy_R']:+.3f} ({r['expectancy_ci_low']:+.3f}, {r['expectancy_ci_high']:+.3f})"
        sig = "yes" if r["expectancy_significant"] else "no"
        lines.append(
            f"| **{r['variant']}** | {r['n_entries']} | "
            f"{r['win_rate']*100:.1f}% ({r['win_rate_ci_low']*100:.1f}-"
            f"{r['win_rate_ci_high']*100:.1f}) | "
            f"{r['p_target']*100:.1f}% | {r['p_stop']*100:.1f}% | "
            f"{ci} | {sig} | "
            f"{r['avg_win_R']:+.2f}R | {r['avg_loss_R']:+.2f}R | "
            f"{r['median_R']:+.2f}R | ${r['median_risk_$']:.2f} |"
        )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    if not DATA_PATH.exists():
        print(f"[error] No data at {DATA_PATH}.")
        return 1

    bars = pd.read_parquet(DATA_PATH)
    if not isinstance(bars.index, pd.DatetimeIndex):
        bars.index = pd.to_datetime(bars.index, utc=True)

    print(f"Loaded {len(bars):,} bars")
    variants = research.standard_variants()
    no_costs = research.CostConfig(slippage_per_share=0.0)
    with_costs = research.CostConfig(slippage_per_share=SLIPPAGE_PER_SHARE)

    print(f"Evaluating {len(variants)} variants x 2 cost models...")
    gross_rows: list[dict] = []
    net_rows: list[dict] = []
    for v in variants:
        print(f"  - {v.name:30s} ", end="", flush=True)
        gross_rows.append(evaluate_variant(bars, v, no_costs))
        net_rows.append(evaluate_variant(bars, v, with_costs))
        print(
            f"gross E={gross_rows[-1].get('expectancy_R', float('nan')):+.3f}R, "
            f"net E={net_rows[-1].get('expectancy_R', float('nan')):+.3f}R"
        )

    # Build report
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    out: list[str] = []
    out.append("# Variant Grid - Stop/Target/Entry ablations + costs + bootstrap CIs")
    out.append("")
    out.append(f"Data: QQQ 1m, {len(bars):,} bars, {bars.index.min().date()} -> {bars.index.max().date()}")
    out.append(f"Bootstrap iterations: **{N_BOOTSTRAP:,}**, 95% CI percentile method.")
    out.append(f"Slippage applied (net columns): **${SLIPPAGE_PER_SHARE}/share each side** "
               f"(${2*SLIPPAGE_PER_SHARE}/share round-trip).")
    out.append("")
    out.append("**Reading guide:**")
    out.append("- `Exp R (95% CI)`: bootstrap mean R with lower/upper bounds.")
    out.append("- `Sig?`: \"yes\" if the 95% CI does not include 0 - i.e. we can reject \"no edge\" at 5%.")
    out.append("- `Avg Win` / `Avg Loss` are mean R-multiples within winners/losers.")
    out.append("- `Risk $` is the median dollar risk per share at entry - "
               "tells you how much slippage actually eats into the edge.")
    out.append("")

    # Variant descriptions block
    out.append("## Variants")
    out.append("")
    for v in variants:
        out.append(f"- **{v.name}** - {v.description}")
        out.append(f"    entry={v.entry_method}, stop={v.stop_method}, "
                   f"target={v.target_method}"
                   + (f" ({v.target_R:.1f}R)" if v.target_method == "fixed_R" else "")
                   + (f", buffer=${v.stop_buffer:.2f}" if v.stop_method.startswith("wick") else "")
                   + (f", pct_or={v.stop_pct_or:.0%}" if v.stop_method == "pct_or" else ""))
    out.append("")

    out.append(render_table(gross_rows, "Gross results (no costs)"))
    out.append(render_table(net_rows, f"Net results (slippage ${SLIPPAGE_PER_SHARE}/share each side)"))

    # Top picks
    out.append("## Ranked by net expectancy (lower bound of 95% CI)")
    out.append("")
    ranked = sorted(
        [r for r in net_rows if r.get("n_entries", 0) > 0],
        key=lambda r: r["expectancy_ci_low"],
        reverse=True,
    )
    out.append("| Rank | Variant | Net Exp R | 95% CI low | Win % | N |")
    out.append("|---|---|---|---|---|---|")
    for i, r in enumerate(ranked, 1):
        out.append(
            f"| {i} | {r['variant']} | {r['expectancy_R']:+.3f}R | "
            f"{r['expectancy_ci_low']:+.3f}R | {r['win_rate']*100:.1f}% | {r['n_entries']} |"
        )
    out.append("")

    out.append("## Verdict")
    out.append("")
    survivors = [r for r in net_rows if r.get("expectancy_significant", False) and r["expectancy_ci_low"] > 0]
    if survivors:
        names = ", ".join(s["variant"] for s in survivors)
        out.append(f"**{len(survivors)} variant(s) have a 95% CI strictly above 0R after costs:** {names}")
        out.append("These are candidates for a Phase 2 backtest with full equity-curve and drawdown analysis.")
    else:
        out.append("**No variant survives costs at the 95% confidence level.**")
        out.append("Either the rules need a structural change (e.g. add HTF bias / liquidity filter), or the "
                   "true edge is too small to overcome QQQ retail execution costs at this trade frequency.")
    out.append("")

    text = "\n".join(out)
    REPORT_PATH.write_text(text)

    pd.DataFrame(gross_rows).assign(cost_model="gross").to_csv(SUMMARY_CSV, index=False, mode="w")
    pd.DataFrame(net_rows).assign(cost_model="net").to_csv(SUMMARY_CSV, index=False, mode="a", header=False)

    print()
    print(text)
    print(f"\nReport: {REPORT_PATH.relative_to(ROOT)}")
    print(f"CSV   : {SUMMARY_CSV.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
