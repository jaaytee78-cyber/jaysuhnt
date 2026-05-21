"""PSS validation package.

Bug-fixed Python port of indicators/pine-script/phase4_signals.pine,
plus a realistic backtest engine and a markdown report writer.

This package is deliberately READ-ONLY with respect to strategy logic:
no parameter optimisation, no curve-fitting. Its only job is to take the
parameters as written in the .pine file and tell us, honestly, whether
the strategy has a measurable edge on real data.
"""

__version__ = "0.1.0"
