"""Markdown report writer for ASW validation runs.

Adapted from the PSS report writer for the ASW context. Same skeleton
(headline stats, R distribution, exit reasons, segments, coin-flip
baseline) plus an Asian-range diagnostic section: how often the range
got swept, how often it was reclaimed, distribution of range sizes.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd

from .params import AswParams


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
    max_dd = float((peak - cum).max())

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
    if trades.empty:
        return pd.DataFrame()
    rows = []
    for k, sub in trades.groupby(segment_col):
        if len(sub) < min_trades:
            continue
        s = core_stats(sub)
        rows.append(
            dict(
                segment=k,
                n=s.n_trades,
                wr=s.win_rate,
                exp_r=s.expectancy_r,
                total_r=s.total_r,
                pf=s.profit_factor,
            )
        )
    return pd.DataFrame(rows).set_index("segment") if rows else pd.DataFrame()


def r_distribution_buckets(trades: pd.DataFrame) -> Dict[str, int]:
    if trades.empty:
        return {}
    r = trades["r_realised"]
    edges = [-np.inf, -1.05, -0.5, -0.05, 0.05, 0.5, 1.0, 2.0, 3.0, np.inf]
    labels = [
        "below -1R",
        "-1.05R to -0.5R",
        "-0.5R to -0.05R",
        "-0.05R to +0.05R",
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
    n_simulations: int = 1000,
    seed: int = 42,
) -> dict:
    """Coin-flip on the same trades.

    For each fired trade we have an actual realised R (mostly clustered
    near -1R or near +rr_realised). To get a fair baseline we randomly
    flip the sign of each trade's R outcome and re-sum total R. This
    asks: "If you took the same setups but with random direction, what
    distribution of total-R outcomes would you see?"
    """
    if trades.empty:
        return dict(
            mean_total_r=0.0, std_total_r=0.0,
            p_at_least_strategy=1.0, strategy_total_r=0.0,
        )
    r_abs = trades["r_realised"].abs().to_numpy()
    rng = np.random.default_rng(seed)
    flips = rng.choice([-1.0, 1.0], size=(n_simulations, len(trades)))
    sims = (flips * r_abs).sum(axis=1)
    strategy_total = float(trades["r_realised"].sum())
    p_at_least = float((sims >= strategy_total).sum()) / n_simulations
    return dict(
        mean_total_r=float(sims.mean()),
        std_total_r=float(sims.std()),
        p_at_least_strategy=p_at_least,
        strategy_total_r=strategy_total,
    )


# --------------------------------------------------------------------- #
#  Asian range / sweep / reclaim diagnostics                            #
# --------------------------------------------------------------------- #

def asia_diagnostics(sig: pd.DataFrame) -> dict:
    """Per trading-day analysis of the Asian range and sweep activity.

    Returns empty dict if asia_high/asia_low not present (e.g. for
    strategies that don't use Asian session levels).
    """
    if sig.empty:
        return {}
    if "asia_high" not in sig.columns or "asia_low" not in sig.columns:
        return {}
    if sig.index.tz is None:
        idx_utc = sig.index.tz_localize("UTC")
    else:
        idx_utc = sig.index.tz_convert("UTC")
    s = sig.copy()
    s["trading_date"] = pd.to_datetime(idx_utc.date)

    # Restrict to bars where AH/AL are valid (non-Asia)
    valid = s.dropna(subset=["asia_high", "asia_low"])
    n_days = int(valid["trading_date"].nunique())

    # Per-day aggregates
    grouped = valid.groupby("trading_date")
    swept_low = grouped.apply(
        lambda g: bool((g["low"] < g["asia_low"]).any())
    )
    swept_high = grouped.apply(
        lambda g: bool((g["high"] > g["asia_high"]).any())
    )
    range_atr = grouped.apply(
        lambda g: (g["asia_high"].iloc[0] - g["asia_low"].iloc[0])
                  / g["atr"].dropna().iloc[0]
        if g["atr"].notna().any() else np.nan
    ).dropna()

    return dict(
        n_days=n_days,
        range_atr_p25=float(range_atr.quantile(0.25)) if len(range_atr) else 0.0,
        range_atr_p50=float(range_atr.quantile(0.50)) if len(range_atr) else 0.0,
        range_atr_p75=float(range_atr.quantile(0.75)) if len(range_atr) else 0.0,
        n_swept_low=int(swept_low.sum()),
        n_swept_high=int(swept_high.sum()),
        n_swept_either=int((swept_low | swept_high).sum()),
        n_swept_both=int((swept_low & swept_high).sum()),
        n_long_fires=int(sig["signal_long"].sum()),
        n_short_fires=int(sig["signal_short"].sum()),
    )


# --------------------------------------------------------------------- #
#  Markdown helpers                                                     #
# --------------------------------------------------------------------- #

def _fmt_pct(x: float) -> str:
    return f"{x * 100:5.1f}%"


def _fmt_r(x: float) -> str:
    if not np.isfinite(x):
        return "  inf"
    return f"{x:+6.3f}R"


def _table(headers: list, rows: list) -> str:
    out = ["| " + " | ".join(headers) + " |"]
    out.append("|" + "|".join(["---"] * len(headers)) + "|")
    for row in rows:
        out.append("| " + " | ".join(str(c) for c in row) + " |")
    return "\n".join(out)


def _params_table(p) -> str:
    """Generic params table. Works with any dataclass that exposes
    .as_dict() or any object with __dict__. Each row is (field, value).
    """
    if hasattr(p, "as_dict"):
        items = list(p.as_dict().items())
    else:
        items = list(vars(p).items())
    return _table(["param", "value"], items)


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
    total = int(counts.sum())
    rows = [(r, int(n), _fmt_pct(int(n) / total)) for r, n in counts.items()]
    return _table(["exit reason", "count", "share"], rows)


def _diagnostics_block(diag: dict) -> str:
    if not diag:
        return "_(no signal data)_"
    n = diag.get("n_days", 0) or 1
    rows = [
        ("trading days observed", diag["n_days"]),
        ("Asian range (AH-AL)/ATR p25", f"{diag['range_atr_p25']:.2f}"),
        ("Asian range (AH-AL)/ATR median", f"{diag['range_atr_p50']:.2f}"),
        ("Asian range (AH-AL)/ATR p75", f"{diag['range_atr_p75']:.2f}"),
        ("days where AL was swept", f"{diag['n_swept_low']} ({_fmt_pct(diag['n_swept_low']/n)})"),
        ("days where AH was swept", f"{diag['n_swept_high']} ({_fmt_pct(diag['n_swept_high']/n)})"),
        ("days where either was swept", f"{diag['n_swept_either']} ({_fmt_pct(diag['n_swept_either']/n)})"),
        ("days where both were swept", f"{diag['n_swept_both']} ({_fmt_pct(diag['n_swept_both']/n)})"),
        ("long signals fired", diag["n_long_fires"]),
        ("short signals fired", diag["n_short_fires"]),
    ]
    return _table(["metric", "value"], rows)


# --------------------------------------------------------------------- #
#  Main entry                                                           #
# --------------------------------------------------------------------- #

def write_report(
    out_path: Path,
    label: str,
    bars_df: pd.DataFrame,
    sig_df: pd.DataFrame,
    trades: pd.DataFrame,
    params: AswParams,
    notes: str = "",
) -> Path:
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    s = core_stats(trades)
    by_hour = stats_by_segment(trades, "hour_utc")
    by_dow = stats_by_segment(trades, "day_of_week")
    by_side = stats_by_segment(trades, "side")
    if not trades.empty:
        twm = trades.copy()
        twm["month"] = twm.index.strftime("%Y-%m")
        by_month = stats_by_segment(twm, "month")
    else:
        by_month = pd.DataFrame()
    rdist = r_distribution_buckets(trades)
    coin = coin_flip_baseline(trades)
    diag = asia_diagnostics(sig_df)

    bar_count = len(bars_df)
    bars_start = bars_df.index[0].isoformat() if bar_count else "n/a"
    bars_end = bars_df.index[-1].isoformat() if bar_count else "n/a"

    md = []
    md.append(f"# ASW validation report — XAU/USD ({label})")
    md.append("")
    md.append(
        f"_Generated {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}; "
        f"strategy spec: backtests/specs/xau_asian_sweep.md._"
    )
    md.append("")
    md.append("## What this report is")
    md.append("")
    md.append(
        "Asian Sweep + Reversal logic, run on real 5-minute Polygon "
        "data with the parameters as written in `backtests/asw/params.py` "
        "and the spec. **No optimisation. No tuning.** The question: "
        "does the strategy show a measurable edge on this data window?"
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
            ("instrument", "XAU/USD (Polygon C:XAUUSD)"),
            ("bars (5m)", bar_count),
            ("first bar", bars_start),
            ("last bar", bars_end),
        ],
    ))
    md.append("")

    md.append("## Asian session diagnostics")
    md.append("")
    if diag:
        md.append(_diagnostics_block(diag))
    else:
        md.append("_(strategy does not use Asian session levels)_")
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

    md.append("## Performance by day-of-week (0=Mon)")
    md.append("")
    md.append(_segment_table(by_dow, "dow"))
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
        "Random-direction baseline: keep the |R| outcomes from the "
        "strategy's actual trades, randomise the sign of each, sum "
        "total R. Repeat 1000 times. The probability that random "
        "direction matches or beats the strategy is reported below."
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
        "P > 0.20 means the result is indistinguishable from coin-flip "
        "noise. P < 0.05 is the conventional 'real signal' threshold. "
        "Anything in between is gray."
    )
    md.append("")

    out_path.write_text("\n".join(md))
    return out_path


# --------------------------------------------------------------------- #
#  IS vs OOS comparison report                                          #
# --------------------------------------------------------------------- #

def write_comparison_report(
    out_path: Path,
    is_trades: pd.DataFrame,
    oos_trades: pd.DataFrame,
    is_sig: pd.DataFrame,
    oos_sig: pd.DataFrame,
    params: AswParams,
    is_window: tuple,
    oos_window: tuple,
) -> Path:
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    is_s = core_stats(is_trades)
    oos_s = core_stats(oos_trades)
    is_coin = coin_flip_baseline(is_trades)
    oos_coin = coin_flip_baseline(oos_trades)
    is_diag = asia_diagnostics(is_sig)
    oos_diag = asia_diagnostics(oos_sig)

    is_per_year = is_s.n_trades / max(((is_window[1] - is_window[0]).days / 365.25), 1e-9)
    oos_per_year = oos_s.n_trades / max(((oos_window[1] - oos_window[0]).days / 365.25), 1e-9)

    if is_s.expectancy_r != 0:
        ratio = oos_s.expectancy_r / is_s.expectancy_r
    else:
        ratio = float("nan")

    md = []
    md.append("# ASW validation — IS vs OOS comparison")
    md.append("")
    md.append(
        f"_Generated {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}._"
    )
    md.append("")
    md.append("## Windows")
    md.append("")
    md.append(_table(
        ["split", "start", "end", "trading days approx", "trades"],
        [
            ("IS",  is_window[0].isoformat(),  is_window[1].isoformat(),
             (is_window[1] - is_window[0]).days, is_s.n_trades),
            ("OOS", oos_window[0].isoformat(), oos_window[1].isoformat(),
             (oos_window[1] - oos_window[0]).days, oos_s.n_trades),
        ],
    ))
    md.append("")

    md.append("## Side-by-side")
    md.append("")
    md.append(_table(
        ["metric", "IS", "OOS"],
        [
            ("trades", is_s.n_trades, oos_s.n_trades),
            ("trades / year", f"{is_per_year:.1f}", f"{oos_per_year:.1f}"),
            ("longs / shorts", f"{is_s.n_long} / {is_s.n_short}",
                                f"{oos_s.n_long} / {oos_s.n_short}"),
            ("win rate", _fmt_pct(is_s.win_rate), _fmt_pct(oos_s.win_rate)),
            ("expectancy", _fmt_r(is_s.expectancy_r), _fmt_r(oos_s.expectancy_r)),
            ("total R", _fmt_r(is_s.total_r), _fmt_r(oos_s.total_r)),
            ("profit factor", f"{is_s.profit_factor:.2f}", f"{oos_s.profit_factor:.2f}"),
            ("max DD", _fmt_r(-is_s.max_drawdown_r), _fmt_r(-oos_s.max_drawdown_r)),
            ("longest loss streak", is_s.longest_loss_streak, oos_s.longest_loss_streak),
            ("P(coin flip >= strat)",
             f"{is_coin['p_at_least_strategy']:.3f}",
             f"{oos_coin['p_at_least_strategy']:.3f}"),
        ],
    ))
    md.append("")

    md.append("## Asian session diagnostics, IS vs OOS")
    md.append("")
    md.append(_table(
        ["metric", "IS", "OOS"],
        [
            ("trading days", is_diag.get("n_days", 0), oos_diag.get("n_days", 0)),
            ("median range / ATR",
             f"{is_diag.get('range_atr_p50', 0):.2f}",
             f"{oos_diag.get('range_atr_p50', 0):.2f}"),
            ("days swept (either)",
             is_diag.get("n_swept_either", 0),
             oos_diag.get("n_swept_either", 0)),
            ("days swept (both)",
             is_diag.get("n_swept_both", 0),
             oos_diag.get("n_swept_both", 0)),
        ],
    ))
    md.append("")

    md.append("## Verdict (per spec section 8 / 9)")
    md.append("")
    verdict_rows = []

    def yn(b: bool) -> str:
        return "PASS" if b else "FAIL"

    pass_trade_count = is_s.n_trades >= 50 and oos_s.n_trades >= 50
    pass_oos_positive = oos_s.expectancy_r > 0
    pass_ratio = (
        np.isfinite(ratio) and ratio >= 0.7 and is_s.expectancy_r > 0
    )
    pass_oos_p = oos_coin["p_at_least_strategy"] < 0.20
    pass_dd = oos_s.max_drawdown_r <= 25
    pass_streak = oos_s.longest_loss_streak <= 8
    overall_pass = (
        pass_trade_count and pass_oos_positive and pass_ratio
        and pass_oos_p and pass_dd and pass_streak
    )

    verdict_rows.append(("trade count >= 50 each split", yn(pass_trade_count)))
    verdict_rows.append(("OOS expectancy > 0", yn(pass_oos_positive)))
    verdict_rows.append(("OOS expectancy >= 0.7 * IS", yn(pass_ratio)))
    verdict_rows.append(("OOS coin-flip P < 0.20", yn(pass_oos_p)))
    verdict_rows.append(("OOS max DD <= 25R", yn(pass_dd)))
    verdict_rows.append(("OOS longest loss streak <= 8", yn(pass_streak)))
    verdict_rows.append(("**OVERALL**", "**PASS**" if overall_pass else "**FAIL**"))

    md.append(_table(["criterion", "verdict"], verdict_rows))
    md.append("")
    md.append(
        "**PASS overall** = strategy worth taking to demo paper trading.\n"
        "**FAIL overall** = strategy stays in the repo as a learning artifact; "
        "any single failed criterion is enough to fail."
    )
    md.append("")

    out_path.write_text("\n".join(md))
    return out_path
