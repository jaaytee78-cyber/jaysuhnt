"""TA primitives for the ASW strategy.

Causal by construction. Helper duplicates of session_id / pine_atr from
the PSS package so this package stands alone.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


# --------------------------------------------------------------------- #
#  Pine-style primitives                                                #
# --------------------------------------------------------------------- #

def pine_rma(x: pd.Series, length: int) -> pd.Series:
    """Wilder's RMA: alpha = 1/length. Used by ta.atr internally."""
    return x.ewm(alpha=1.0 / length, adjust=False).mean()


def true_range(df: pd.DataFrame) -> pd.Series:
    prev_close = df["close"].shift(1)
    hl = df["high"] - df["low"]
    hc = (df["high"] - prev_close).abs()
    lc = (df["low"] - prev_close).abs()
    return pd.concat([hl, hc, lc], axis=1).max(axis=1)


def pine_atr(df: pd.DataFrame, length: int) -> pd.Series:
    """ta.atr(length) -- Wilder's RMA of True Range."""
    return pine_rma(true_range(df), length)


# --------------------------------------------------------------------- #
#  Asian session high / low                                             #
# --------------------------------------------------------------------- #

def asia_session_levels(
    df: pd.DataFrame,
    asia_start_utc: int = 22,
    asia_end_utc: int = 6,
) -> pd.DataFrame:
    """Compute Asian session high (AH) and low (AL) for each bar.

    Asia session for "trading day X" runs from
        [asia_start_utc on day X-1, asia_end_utc on day X)

    Causality contract:
      - Bars DURING Asia (the session is still forming) get AH=AL=NaN.
        We never trade in Asia anyway; this prevents accidental future
        leakage if the strategy is ever extended.
      - Bars from asia_end_utc on day X up to (asia_start_utc on day X)
        receive AH(X), AL(X) from the just-completed Asia session.

    Parameters
    ----------
    asia_start_utc, asia_end_utc : int (0-23)
        Asia session boundaries. Default 22:00 -> 06:00 UTC.

    Returns
    -------
    DataFrame indexed like df, columns: asia_high, asia_low
    """
    if df.index.tz is None:
        idx = df.index.tz_localize("UTC")
    else:
        idx = df.index.tz_convert("UTC")

    hours = idx.hour
    # "in Asia" => bar is part of an Asia session that is still forming
    in_asia = (hours >= asia_start_utc) | (hours < asia_end_utc)

    # For bars IN Asia, anchor to the trading-day they belong to:
    #   hours [asia_start_utc, 24) belong to NEXT day's session
    #   hours [0, asia_end_utc)    belong to TODAY's session
    asia_idx = df.index[in_asia]
    if len(asia_idx) == 0:
        out = pd.DataFrame(
            index=df.index, columns=["asia_high", "asia_low"], dtype="float64"
        )
        return out

    asia_idx_utc = (
        asia_idx.tz_localize("UTC") if asia_idx.tz is None
        else asia_idx.tz_convert("UTC")
    )
    asia_hours = asia_idx_utc.hour
    asia_dates = pd.to_datetime(asia_idx_utc.date)
    plus_one = pd.Timedelta(days=1)
    anchor_dates = pd.Series(
        np.where(asia_hours >= asia_start_utc,
                 asia_dates + plus_one,
                 asia_dates),
        index=asia_idx,
    )

    asia_df = df.loc[in_asia, ["high", "low"]].copy()
    asia_df["anchor"] = anchor_dates
    per_day = asia_df.groupby("anchor").agg(
        asia_high=("high", "max"),
        asia_low=("low", "min"),
    )

    # For NON-Asia bars, anchor = bar's UTC date
    out = pd.DataFrame(
        index=df.index, columns=["asia_high", "asia_low"], dtype="float64"
    )
    non_asia_mask = ~in_asia
    if non_asia_mask.any():
        non_asia_idx = df.index[non_asia_mask]
        non_asia_idx_utc = (
            non_asia_idx.tz_localize("UTC") if non_asia_idx.tz is None
            else non_asia_idx.tz_convert("UTC")
        )
        non_asia_dates = pd.Series(
            pd.to_datetime(non_asia_idx_utc.date), index=non_asia_idx
        )
        out.loc[non_asia_mask, "asia_high"] = non_asia_dates.map(
            per_day["asia_high"]
        ).values
        out.loc[non_asia_mask, "asia_low"] = non_asia_dates.map(
            per_day["asia_low"]
        ).values
    # Asia bars stay NaN
    return out
