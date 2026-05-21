# ASW validation — IS vs OOS comparison

_Generated 2026-05-21 21:36 UTC._

## Windows

| split | start | end | trading days approx | trades |
|---|---|---|---|---|
| IS | 2024-05-21T00:00:00+00:00 | 2025-11-18T23:50:00+00:00 | 546 | 430 |
| OOS | 2025-11-18T23:55:00+00:00 | 2026-05-20T23:55:00+00:00 | 183 | 119 |

## Side-by-side

| metric | IS | OOS |
|---|---|---|
| trades | 430 | 119 |
| trades / year | 287.7 | 237.5 |
| longs / shorts | 190 / 240 | 54 / 65 |
| win rate |  24.2% |  31.1% |
| expectancy | -0.243R | -0.070R |
| total R | -104.399R | -8.313R |
| profit factor | 0.71 | 0.90 |
| max DD | -121.772R | -16.384R |
| longest loss streak | 16 | 9 |
| P(coin flip >= strat) | 0.992 | 0.705 |

## Asian session diagnostics, IS vs OOS

| metric | IS | OOS |
|---|---|---|
| trading days | 386 | 127 |
| median range / ATR | 10.81 | 11.90 |
| days swept (either) | 376 | 118 |
| days swept (both) | 113 | 27 |

## Verdict (per spec section 8 / 9)

| criterion | verdict |
|---|---|
| trade count >= 50 each split | PASS |
| OOS expectancy > 0 | FAIL |
| OOS expectancy >= 0.7 * IS | FAIL |
| OOS coin-flip P < 0.20 | FAIL |
| OOS max DD <= 25R | PASS |
| OOS longest loss streak <= 8 | FAIL |
| **OVERALL** | **FAIL** |

**PASS overall** = strategy worth taking to demo paper trading.
**FAIL overall** = strategy stays in the repo as a learning artifact; any single failed criterion is enough to fail.
