"""Markdown report writer for PSS validation runs.

Computes the metrics specified in the validation plan and renders them
as a single markdown report file. No charts (keep dependencies light);
the tables and distributions are enough to draw conclusions.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd

from .params import PSSParams


# --------------------------------------------------------------------- #
#  Metrics                                                              #
# --------------------------------------------------------------------- #

@dataclass
class CoreStats:
    n_trades: int
    n_long: int
    n_short: int
    win_rate: float
    avg_r: float
    avg_win_r: float
    avg_loss_r: float
    expectancy_r: float
    profit_factor: float
    total_r: float
    max_drawdown_r: float
    longest_loss_streak: int
    longest_win_streak: int


def core_stats(trades: pd.DataFrame) -> CoreStats:
    if trades.empty:
        return CoreStats(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    r = trades["r_realised"]
    n = len(r)
    wins_mask = r > 0
    losses_mask = r < 0
    avg_win_r = float(r[wins_mask].mean()) if wins_mask.any() else 0.0
    avg_loss_r = float(r[losses_mask].mean()) if losses_mask.any() else 0.0
    win_rate = float(wins_mask.sum() / n)
    expectancy_r = win_rate * avg_win_r + (1 - win_rate) * avg_loss_r

    gross_win = float(r[wins_mask].sum())
    gross_loss = float(-r[losses_mask].sum())
    profit_factor = gross_win / gross_loss if gross_loss > 0 else float("inf")

    total_r = float(r.sum())
    cum = r.cumsum()
    peak = cum.cummax()
    drawdown = peak - cum
    max_dd = float(drawdown.max())

    # Streaks (zeros not counted on either side; rare edge case)
    streak_loss = streak_win = max_loss = max_win = 0
    for v in r.values:
        if v < 0:
            streak_loss += 1
            streak_win = 0
            max_loss = max(max_loss, streak_loss)
        elif v > 0:
            streak_win += 1
            streak_loss = 0
            max_win = max(max_win, streak_win)
        else:
            streak_loss = 0
            streak_win = 0

    return CoreStats(
        n_trades=n,
        n_long=int((trades["side"] == "long").sum()),
        n_short=int((trades["side"] == "short").sum()),
        win_rate=win_rate,
        avg_r=float(r.mean()),
        avg_win_r=avg_win_r,
        avg_loss_r=avg_loss_r,
        expectancy_r=float(expectancy_r),
        profit_factor=float(profit_factor),
        total_r=total_r,
        max_drawdown_r=max_dd,
        longest_loss_streak=max_loss,
        longest_win_streak=max_win,
    )


def stats_by_segment(
    trades: pd.DataFrame,
    segment_col: str,
    min_trades: int = 5,
) -> pd.DataFrame:
    """Group trades by `segment_col` and return per-segment stats."""
    if trades.empty:
        return pd.DataFrame()
    g = trades.groupby(segment_col)
    rows = []
    for k, sub in g:
        if len(sub) < min_trades:
            continue
        s = core_stats(sub)
        rows.append(
            dict(
                segment=k,
                n=s.n_trades,
                wr=s.win_rate,
                avg_r=s.avg_r,
                exp_r=s.expectancy_r,
                total_r=s.total_r,
                pf=s.profit_factor,
            )
        )
    return pd.DataFrame(rows).set_index("segment") if rows else pd.DataFrame()


def r_distribution_buckets(trades: pd.DataFrame) -> Dict[str, int]:
    """Coarse histogram of R outcomes for inclusion in the report."""
    if trades.empty:
        return {}
    r = trades["r_realised"]
    edges = [-np.inf, -1.05, -0.5, -0.05, 0.05, 0.5, 1.0, 2.0, 3.0, np.inf]
    labels = [
        "below -1R (slippage worse than planned)",
        "-1.05R to -0.5R",
        "-0.5R to -0.05R",
        "-0.05R to +0.05R (scratch)",
        "+0.05R to +0.5R",
        "+0.5R to +1.0R",
        "+1.0R to +2.0R",
        "+2.0R to +3.0R",
        "above +3R",
    ]
    counts = pd.cut(r, bins=edges, labels=labels, include_lowest=True).value_counts()
    return counts.reindex(labels, fill_value=0).to_dict()


def coin_flip_baseline(
    trades: pd.DataFrame,
    p,  # PSSParams
    n_simulations: int = 1000,
    seed: int = 42,
) -> dict:
    """Compare strategy to random direction with same stops/targets.

    For a fixed-stop, fixed-target system, a random-direction trade has
    expected value of 0 minus costs. We approximate by replacing each
    trade's side with a coin flip and re-evaluating R using the SAME
    bar outcomes -- but since we don't preserve the per-bar path here,
    we use the simpler approximation: a coin flip wins with probability
    1/(1+rr_ratio) (the fair break-even win rate ignoring costs), and
    each win pays rr_ratio R, each loss pays -1R.

    Returns the mean and std of total_R over n_simulations such trades.
    Use this to ask: is the strategy's total_R clearly outside the
    coin-flip distribution?
    """
    if trades.empty:
        return dict(mean_total_r=0.0, std_total_r=0.0, p_at_least_strategy=1.0)

    rng = np.random.default_rng(seed)
    n = len(trades)
    p_win = 1.0 / (1.0 + p.rr_ratio)
    rr = p.rr_ratio

    sims = rng.random((n_simulations, n)) < p_win
    sim_r = np.where(sims, rr, -1.0)
    totals = sim_r.sum(axis=1)
    strategy_total = float(trades["r_realised"].sum())
    p_at_least = float((totals >= strategy_total).sum()) / n_simulations
    return dict(
        mean_total_r=float(totals.mean()),
        std_total_r=float(totals.std()),
        p_at_least_strategy=p_at_least,
        strategy_total_r=strategy_total,
    )


# --------------------------------------------------------------------- #
#  Markdown formatting                                                  #
# --------------------------------------------------------------------- #

def _fmt_pct(x: float) -> str:
    return f"{x * 100:5.1f}%"


def _fmt_r(x: float) -> str:
    if not np.isfinite(x):
        return "  inf"
    return f"{x:+6.3f}R"


def _table(headers: list, rows: list) -> str:
    """Render a markdown table."""
    out = ["| " + " | ".join(headers) + " |"]
    out.append("|" + "|".join(["---"] * len(headers)) + "|")
    for row in rows:
        out.append("| " + " | ".join(str(c) for c in row) + " |")
    return "\n".join(out)


def _params_table(p) -> str:
    rows = [
        ("sd_mult", p.sd_mult),
        ("atr_period", p.atr_period),
        ("stop_mult", p.stop_mult),
        ("rr_ratio", p.rr_ratio),
        ("cooldown", p.cooldown),
        ("level_tol", p.level_tol),
        ("compress_pct", p.compress_pct),
        ("min_score", p.min_score),
        ("hour_filter", p.hour_filter),
        ("hour_start_utc", p.hour_start_utc),
        ("hour_end_utc", p.hour_end_utc),
        ("half_spread (cost model)", p.half_spread),
        ("stop_slippage (cost model)", p.stop_slippage),
    ]
    return _table(["param", "value"], rows)


def _core_table(s: CoreStats) -> str:
    rows = [
        ("trades total", s.n_trades),
        ("longs / shorts", f"{s.n_long} / {s.n_short}"),
        ("win rate", _fmt_pct(s.win_rate)),
        ("expectancy per trade", _fmt_r(s.expectancy_r)),
        ("avg R per trade", _fmt_r(s.avg_r)),
        ("avg win", _fmt_r(s.avg_win_r)),
        ("avg loss", _fmt_r(s.avg_loss_r)),
        ("profit factor", f"{s.profit_factor:.2f}"),
        ("total R", _fmt_r(s.total_r)),
        ("max drawdown", _fmt_r(-s.max_drawdown_r)),
        ("longest loss streak", s.longest_loss_streak),
        ("longest win streak", s.longest_win_streak),
    ]
    return _table(["metric", "value"], rows)


def _segment_table(df: pd.DataFrame, segment_label: str) -> str:
    if df.empty:
        return "_(no segments with enough trades)_"
    rows = []
    for seg, row in df.iterrows():
        rows.append(
            (
                seg,
                int(row["n"]),
                _fmt_pct(row["wr"]),
                _fmt_r(row["exp_r"]),
                _fmt_r(row["total_r"]),
                f"{row['pf']:.2f}" if np.isfinite(row["pf"]) else "inf",
            )
        )
    return _table(
        [segment_label, "n", "win%", "expectancy", "total R", "PF"],
        rows,
    )


def _distribution_table(d: Dict[str, int], total: int) -> str:
    if total == 0:
        return "_(no trades)_"
    rows = []
    for label, n in d.items():
        share = n / total if total else 0.0
        rows.append((label, n, _fmt_pct(share)))
    return _table(["bucket", "count", "share"], rows)


def _exit_reason_table(trades: pd.DataFrame) -> str:
    if trades.empty:
        return "_(no trades)_"
    counts = trades["exit_reason"].value_counts()
    rows = []
    total = int(counts.sum())
    for reason, n in counts.items():
        rows.append((reason, int(n), _fmt_pct(int(n) / total)))
    return _table(["exit reason", "count", "share"], rows)


# --------------------------------------------------------------------- #
#  Main entry                                                           #
# --------------------------------------------------------------------- #

def write_report(
    out_path: Path,
    instrument: str,
    polygon_ticker: str,
    bars_df: pd.DataFrame,
    sig_df: pd.DataFrame,
    trades: pd.DataFrame,
    params: PSSParams,
    notes: str = "",
) -> Path:
    """Render the full markdown report and write it to disk."""
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    s = core_stats(trades)
    by_hour = stats_by_segment(trades, "hour_utc", min_trades=5)
    by_score = stats_by_segment(trades, "score", min_trades=5)
    by_side = stats_by_segment(trades, "side", min_trades=5)
    if not trades.empty:
        trades_with_month = trades.copy()
        trades_with_month["month"] = trades_with_month.index.strftime("%Y-%m")
        by_month = stats_by_segment(trades_with_month, "month", min_trades=5)
    else:
        by_month = pd.DataFrame()
    rdist = r_distribution_buckets(trades)
    coin = coin_flip_baseline(trades, params)

    bar_count = len(bars_df)
    if bar_count:
        bars_start = bars_df.index[0].isoformat()
        bars_end = bars_df.index[-1].isoformat()
    else:
        bars_start = bars_end = "n/a"

    candidate_long = int(((sig_df["score_long"] >= params.min_score)
                          & sig_df["long_trend_ok"] & sig_df["hour_ok"]).sum())
    candidate_short = int(((sig_df["score_short"] >= params.min_score)
                           & sig_df["short_trend_ok"] & sig_df["hour_ok"]).sum())
    fired_long = int(sig_df["signal_long"].sum())
    fired_short = int(sig_df["signal_short"].sum())

    md = []
    md.append(f"# PSS validation report — {instrument}")
    md.append("")
    md.append(
        f"_Generated {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}; "
        f"data source: Polygon `{polygon_ticker}`._"
    )
    md.append("")
    md.append("## What this report is")
    md.append("")
    md.append(
        "PSS Phase-4 logic, ported bit-exactly from "
        "`indicators/pine-script/phase4_signals.pine`, run on real "
        "5-minute Polygon data with the parameters as currently written "
        "in the .pine file. **No optimisation. No tuning.** The only "
        "question being answered: does the strategy as written show a "
        "measurable edge on this data?"
    )
    md.append("")
    if notes:
        md.append(f"_Notes: {notes}_")
        md.append("")

    md.append("## Parameters used")
    md.append("")
    md.append(_params_table(params))
    md.append("")

    md.append("## Data window")
    md.append("")
    md.append(_table(
        ["field", "value"],
        [
            ("instrument", instrument),
            ("polygon ticker", polygon_ticker),
            ("bars (5m)", bar_count),
            ("first bar", bars_start),
            ("last bar", bars_end),
        ],
    ))
    md.append("")

    md.append("## Signal frequency")
    md.append("")
    md.append(_table(
        ["counter", "value"],
        [
            ("long candidates (pre-cooldown)", candidate_long),
            ("short candidates (pre-cooldown)", candidate_short),
            ("long fires (post-cooldown)", fired_long),
            ("short fires (post-cooldown)", fired_short),
        ],
    ))
    md.append("")

    md.append("## Headline performance")
    md.append("")
    md.append(_core_table(s))
    md.append("")

    md.append("## R-multiple distribution")
    md.append("")
    md.append(_distribution_table(rdist, s.n_trades))
    md.append("")

    md.append("## Exit reason breakdown")
    md.append("")
    md.append(_exit_reason_table(trades))
    md.append("")

    md.append("## Performance by hour-of-day (UTC)")
    md.append("")
    md.append(_segment_table(by_hour, "hour"))
    md.append("")

    md.append("## Performance by signal score (3 vs 4)")
    md.append("")
    md.append(_segment_table(by_score, "score"))
    md.append("")

    md.append("## Long vs short")
    md.append("")
    md.append(_segment_table(by_side, "side"))
    md.append("")

    md.append("## Performance by month")
    md.append("")
    md.append(_segment_table(by_month, "month"))
    md.append("")

    md.append("## Coin-flip baseline")
    md.append("")
    md.append(
        "If you had taken the same number of trades with random "
        "direction (same fixed stop, same fixed target, no costs), "
        "what total R would you have ended at?"
    )
    md.append("")
    md.append(_table(
        ["metric", "value"],
        [
            ("strategy total R", _fmt_r(coin["strategy_total_r"])),
            ("coin-flip mean total R", _fmt_r(coin["mean_total_r"])),
            ("coin-flip std total R", f"{coin['std_total_r']:.2f}"),
            ("P(coin flip >= strategy)", f"{coin['p_at_least_strategy']:.3f}"),
        ],
    ))
    md.append("")
    md.append(
        "If `P(coin flip >= strategy)` is high (say > 0.20), the "
        "observed result is **not distinguishable from random direction "
        "with the same R:R**. If it is low (say < 0.05), the strategy is "
        "doing something a coin flip on the same trade structure would "
        "rarely match."
    )
    md.append("")

    md.append("## Caveats")
    md.append("")
    md.append("1. **Spot-FX volume is synthetic.** Polygon's volume for "
              "`C:XAUUSD` is contributed-bank tick count, not exchange "
              "volume. The CVD-driven D condition relies on this; treat "
              "any conclusion about CVD edge with extra scepticism on XAU.")
    md.append("2. **QQQ is a proxy for NQ futures.** Polygon free tier "
              "does not include futures. QQQ trades RTH only, so the "
              "overnight portion of NQ behaviour is not validated here.")
    md.append("3. **Costs are modelled, not measured.** The half-spread "
              "and stop-slippage values are reasonable retail-broker "
              "estimates. Real fills on a paper or live account will "
              "vary.")
    md.append("4. **No optimisation.** These are the parameters as "
              "currently written in `phase4_signals.pine`. If the .pine "
              "changes, this report becomes stale.")
    md.append("")

    out_path.write_text("\n".join(md))
    return out_path
