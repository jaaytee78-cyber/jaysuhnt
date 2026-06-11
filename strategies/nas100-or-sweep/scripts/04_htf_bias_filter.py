"""
Phase 1.4 - HTF bias filter test (Path 2).

For each variant + each bias method, slice the setup table into:
  - aligned : bias and sweep direction agree (with the trend)
  - against : bias and sweep direction disagree (counter-trend)
  - all     : every setup (the unfiltered universe = our previous result)

Bootstrap 95% CIs on net-of-cost expectancy for each subset.

Hypothesis: aligned subsets should outperform against subsets. If any
(variant, bias) aligned subset has a 95% CI strictly above 0R, we have a
real, statistically significant edge inside a higher-quality slice of the
universe.

Output: reports/04_htf_bias_filter.md
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src import bias, bootstrap, research  # noqa: E402

DATA_PATH = ROOT / "data" / "QQQ_1minute.parquet"
REPORT_PATH = ROOT / "reports" / "04_htf_bias_filter.md"
SUMMARY_CSV = ROOT / "reports" / "bias_filter_summary.csv"

SLIPPAGE_PER_SHARE = 0.01
N_BOOTSTRAP = 5000


def evaluate_subset(setups_subset: pd.DataFrame) -> dict:
    """Compute n, win rate, expectancy + 95% CI on a subset."""
    s = setups_subset[setups_subset["sweep_side"].notna()].copy()
    n = len(s)
    if n == 0:
        return {"n": 0}

    r = s["r_multiple"].dropna().to_numpy()
    boot = bootstrap.bootstrap_mean(r, n_iter=N_BOOTSTRAP)
    wins = (s["r_multiple"] > 0).to_numpy()
    wr = bootstrap.bootstrap_win_rate(wins, n_iter=N_BOOTSTRAP)
    return {
        "n": int(n),
        "win_rate": float(wr.statistic),
        "win_rate_ci_low": float(wr.ci_low),
        "win_rate_ci_high": float(wr.ci_high),
        "expectancy_R": float(boot.statistic),
        "expectancy_ci_low": float(boot.ci_low),
        "expectancy_ci_high": float(boot.ci_high),
        "expectancy_significant": (not boot.crosses_zero) and boot.ci_low > 0,
        "p_target": float(s["target_hit"].mean()),
        "p_stop": float(s["stop_hit"].mean()),
        "avg_win_R": float(s.loc[s["r_multiple"] > 0, "r_multiple"].mean())
            if wins.any() else float("nan"),
        "avg_loss_R": float(s.loc[s["r_multiple"] < 0, "r_multiple"].mean())
            if (s["r_multiple"] < 0).any() else float("nan"),
    }


def fmt_subset_row(label: str, m: dict) -> str:
    if m.get("n", 0) == 0:
        return f"| {label} | 0 | - | - | - | - |"
    ci = f"{m['expectancy_R']:+.3f} ({m['expectancy_ci_low']:+.3f}, {m['expectancy_ci_high']:+.3f})"
    sig = "**yes**" if m["expectancy_significant"] else "no"
    return (
        f"| {label} | {m['n']} | {m['win_rate']*100:.1f}% | "
        f"{m['p_target']*100:.1f}% | {ci} | {sig} |"
    )


def main() -> int:
    if not DATA_PATH.exists():
        print(f"[error] No data at {DATA_PATH}")
        return 1

    bars = pd.read_parquet(DATA_PATH)
    if not isinstance(bars.index, pd.DatetimeIndex):
        bars.index = pd.to_datetime(bars.index, utc=True)

    print(f"Loaded {len(bars):,} bars")
    bias_methods = bias.standard_bias_methods()
    bias_series = {name: fn(bars) for name, fn in bias_methods.items()}

    # Quick sanity: distribution of each bias.
    print("\nBias distribution (bull / bear / neutral, days):")
    for name, ser in bias_series.items():
        counts = ser.value_counts()
        print(f"  {name:18s} bull={int(counts.get('bull', 0))} "
              f"bear={int(counts.get('bear', 0))} "
              f"neutral={int(counts.get('neutral', 0))}")

    variants = research.standard_variants()
    costs = research.CostConfig(slippage_per_share=SLIPPAGE_PER_SHARE)

    out: list[str] = []
    p = out.append

    p("# HTF Bias Filter Test (Path 2)")
    p("")
    p(f"Data: QQQ 1m, {bars.index.min().date()} -> {bars.index.max().date()}")
    p(f"Slippage applied: ${SLIPPAGE_PER_SHARE}/share each side. Bootstrap n={N_BOOTSTRAP:,}.")
    p("")
    p("**Hypothesis:** counter-trend OR sweeps fail more than with-trend sweeps. "
      "Filtering to **aligned** setups should lift expectancy above the unfiltered baseline.")
    p("")
    p("**Bias methods tested:**")
    p("- `prev_close_dir`: bullish if prev RTH close > day-before RTH close")
    p("- `gap_dir`: bullish if today's RTH open > yesterday's RTH close (gap)")
    p("- `ema_20`: bullish if prev RTH close > 20-period EMA of RTH closes")
    p("")
    p("**Reading guide:**")
    p("- `Sig?`: yes only if 95% CI strictly above 0R (real edge after costs)")
    p("- `aligned` rows are the *filtered* universe; `all` is the unfiltered baseline")
    p("- `against` rows are the *anti*-filter (should be worse than `aligned` if our hypothesis holds)")
    p("")

    summary_rows: list[dict] = []

    for v in variants:
        print(f"\nVariant {v.name}...")
        # One setup table per variant (with costs); we then slice by bias.
        setups = research.build_setup_table(bars, config=v, costs=costs)
        if setups.empty:
            continue

        p(f"## {v.name}")
        p(f"_{v.description}_")
        p("")

        for bias_name, bias_ser in bias_series.items():
            # Align bias series to the setup index (ny_date).
            joined = setups.join(bias_ser.rename("bias"), how="left")
            joined["alignment"] = bias.alignment(joined["bias"], joined["sweep_side"])

            all_metrics = evaluate_subset(joined)
            aligned_metrics = evaluate_subset(joined[joined["alignment"] == "aligned"])
            against_metrics = evaluate_subset(joined[joined["alignment"] == "against"])

            p(f"### bias = `{bias_name}`")
            p("")
            p("| Subset | N | Win % | P(tgt) | Net Exp R (95% CI) | Sig? |")
            p("|---|---|---|---|---|---|")
            p(fmt_subset_row("all", all_metrics))
            p(fmt_subset_row("aligned", aligned_metrics))
            p(fmt_subset_row("against", against_metrics))
            p("")

            for label, m in (
                ("all", all_metrics),
                ("aligned", aligned_metrics),
                ("against", against_metrics),
            ):
                if m.get("n", 0) > 0:
                    summary_rows.append({
                        "variant": v.name,
                        "bias": bias_name,
                        "subset": label,
                        **m,
                    })

            print(f"  {bias_name:18s}  "
                  f"all n={all_metrics.get('n', 0):3d} E={all_metrics.get('expectancy_R', float('nan')):+.3f}R | "
                  f"aligned n={aligned_metrics.get('n', 0):3d} E={aligned_metrics.get('expectancy_R', float('nan')):+.3f}R | "
                  f"against n={against_metrics.get('n', 0):3d} E={against_metrics.get('expectancy_R', float('nan')):+.3f}R")

    # Top picks across all (variant, bias, aligned) combinations
    p("---")
    p("")
    p("## Top aligned subsets ranked by net expectancy lower 95% CI")
    p("")
    aligned_only = [r for r in summary_rows if r["subset"] == "aligned"]
    ranked = sorted(aligned_only, key=lambda r: r["expectancy_ci_low"], reverse=True)[:15]
    p("| Rank | Variant | Bias | N | Win % | Net Exp R | 95% CI low | Sig? |")
    p("|---|---|---|---|---|---|---|---|")
    for i, r in enumerate(ranked, 1):
        sig = "**yes**" if r["expectancy_significant"] else "no"
        p(
            f"| {i} | {r['variant']} | {r['bias']} | {r['n']} | "
            f"{r['win_rate']*100:.1f}% | {r['expectancy_R']:+.3f}R | "
            f"{r['expectancy_ci_low']:+.3f}R | {sig} |"
        )
    p("")

    # Verdict
    survivors = [r for r in aligned_only if r["expectancy_significant"]]
    p("## Verdict")
    p("")
    if survivors:
        p(f"**{len(survivors)} (variant, bias) combinations have an aligned-subset 95% CI strictly above 0 after costs.**")
        for r in survivors:
            p(f"- `{r['variant']}` x `{r['bias']}`: net +{r['expectancy_R']:.3f}R "
              f"(CI {r['expectancy_ci_low']:+.3f} to {r['expectancy_ci_high']:+.3f}), "
              f"n={r['n']}, win rate {r['win_rate']*100:.1f}%")
        p("")
        p("Recommended next step: validate the survivor(s) on more data (Polygon upgrade -> 5+ years).")
    else:
        p("**No (variant, bias) combination's aligned-subset 95% CI is strictly above 0R after costs.**")
        p("HTF bias filtering does not unambiguously surface a real edge in our 2-year sample. ")
        p("Look at the ranked table above - if any rows show a clear *direction* (aligned >> against), ")
        p("that's still useful information even without statistical significance.")
    p("")

    text = "\n".join(out)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(text)
    pd.DataFrame(summary_rows).to_csv(SUMMARY_CSV, index=False)

    print()
    print(text)
    print(f"\nReport: {REPORT_PATH.relative_to(ROOT)}")
    print(f"CSV   : {SUMMARY_CSV.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
