# ASW validation — IS vs OOS comparison

_Generated 2026-05-21 21:48 UTC._

## Windows

| split | start | end | trading days approx | trades |
|---|---|---|---|---|
| IS | 2024-05-21T00:00:00+00:00 | 2025-11-18T16:00:00+00:00 | 546 | 149 |
| OOS | 2025-11-18T20:00:00+00:00 | 2026-05-20T20:00:00+00:00 | 183 | 43 |

## Side-by-side

| metric | IS | OOS |
|---|---|---|
| trades | 149 | 43 |
| trades / year | 99.7 | 85.8 |
| longs / shorts | 105 / 44 | 30 / 13 |
| win rate |  28.2% |  41.9% |
| expectancy | +0.101R | +0.621R |
| total R | +15.035R | +26.690R |
| profit factor | 1.14 | 2.06 |
| max DD | -26.493R | -6.144R |
| longest loss streak | 19 | 5 |
| P(coin flip >= strat) | 0.247 | 0.029 |

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
| OOS expectancy >= 0.7 * IS | PASS |
| OOS coin-flip P < 0.20 | PASS |
| OOS max DD <= 25R | PASS |
| OOS longest loss streak <= 8 | PASS |
| **OVERALL** | **FAIL** |

**PASS overall** = strategy worth taking to demo paper trading.
**FAIL overall** = strategy stays in the repo as a learning artifact; any single failed criterion is enough to fail.
