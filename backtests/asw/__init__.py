"""XAU Asian Sweep + Reversal strategy.

Implementation of the spec at backtests/specs/xau_asian_sweep.md.
Self-contained: does not depend on backtests/pss/. Helper functions
that overlap with PSS (session_id, pine_atr) are duplicated here on
purpose so this package can be developed and shipped independently.
"""

__version__ = "0.1.0"
