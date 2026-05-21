# ASW validation — IS vs OOS comparison

_Generated 2026-05-21 22:02 UTC._

## Windows

| split | start | end | trading days approx | trades |
|---|---|---|---|---|
| IS | 2024-05-21T00:00:00+00:00 | 2025-11-18T16:00:00+00:00 | 546 | 92 |
| OOS | 2025-11-18T20:00:00+00:00 | 2026-05-20T20:00:00+00:00 | 183 | 25 |

## Side-by-side

| metric | IS | OOS |
|---|---|---|
| trades | 92 | 25 |
| trades / year | 61.5 | 49.9 |
| longs / shorts | 46 / 46 | 12 / 13 |
| win rate |  25.0% |  44.0% |
| expectancy | -0.030R | +0.577R |
| total R | -2.781R | +14.417R |
| profit factor | 0.96 | 2.02 |
| max DD | -14.031R | -5.012R |
| longest loss streak | 10 | 5 |
| P(coin flip >= strat) | 0.560 | 0.078 |

## Asian session diagnostics, IS vs OOS

| metric | IS | OOS |
|---|---|---|
| trading days | 0 | 0 |
| median range / ATR | 0.00 | 0.00 |
| days swept (either) | 0 | 0 |
| days swept (both) | 0 | 0 |

## Verdict (per spec section 8 / 9)

| criterion | verdict |
|---|---|
| trade count >= 50 each split | FAIL |
| OOS expectancy > 0 | PASS |
| OOS expectancy >= 0.7 * IS | FAIL |
| OOS coin-flip P < 0.20 | PASS |
| OOS max DD <= 25R | PASS |
| OOS longest loss streak <= 8 | PASS |
| **OVERALL** | **FAIL** |

**PASS overall** = strategy worth taking to demo paper trading.
**FAIL overall** = strategy stays in the repo as a learning artifact; any single failed criterion is enough to fail.
