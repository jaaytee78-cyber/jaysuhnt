# ASW validation — IS vs OOS comparison

_Generated 2026-05-21 21:49 UTC._

## Windows

| split | start | end | trading days approx | trades |
|---|---|---|---|---|
| IS | 2024-05-21T00:00:00+00:00 | 2025-11-18T23:50:00+00:00 | 546 | 438 |
| OOS | 2025-11-18T23:55:00+00:00 | 2026-05-20T23:55:00+00:00 | 183 | 120 |

## Side-by-side

| metric | IS | OOS |
|---|---|---|
| trades | 438 | 120 |
| trades / year | 293.0 | 239.5 |
| longs / shorts | 249 / 189 | 71 / 49 |
| win rate |  41.6% |  40.0% |
| expectancy | -0.157R | -0.079R |
| total R | -68.601R | -9.466R |
| profit factor | 0.78 | 0.88 |
| max DD | -83.837R | -12.761R |
| longest loss streak | 12 | 10 |
| P(coin flip >= strat) | 0.995 | 0.776 |

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
