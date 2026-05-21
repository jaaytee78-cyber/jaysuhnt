"""XAU 5m momentum continuation after Asia range break (option C).

Opposite thesis to ASW: instead of FADING the Asia high/low sweep,
this strategy goes WITH the breakout when there is real displacement
beyond the level. Only one rule: a 5m close beyond AH/AL by >= a
displacement threshold = entry in the breakout direction.

If sweep+reverse (ASW) failed and break+continue also fails, the
combined evidence is strong that XAU 5m is just noise after costs.
"""

__version__ = "0.1.0"
