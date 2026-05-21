# ASW validation — IS vs OOS comparison

_Generated 2026-05-21 22:02 UTC._

## Windows

| split | start | end | trading days approx | trades |
|---|---|---|---|---|
| IS | 2024-05-21T00:00:00+00:00 | 2025-11-18T23:50:00+00:00 | 546 | 4828 |
| OOS | 2025-11-18T23:55:00+00:00 | 2026-05-20T23:55:00+00:00 | 183 | 1594 |

## Side-by-side

| metric | IS | OOS |
|---|---|---|
| trades | 4828 | 1594 |
| trades / year | 3229.7 | 3181.5 |
| longs / shorts | 2414 / 2414 | 797 / 797 |
| win rate |  33.1% |  31.2% |
| expectancy | -0.085R | -0.076R |
| total R | -412.520R | -120.670R |
| profit factor | 0.86 | 0.87 |
| max DD | -463.330R | -149.113R |
| longest loss streak | 21 | 20 |
| P(coin flip >= strat) | 1.000 | 0.990 |

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
| trade count >= 50 each split | PASS |
| OOS expectancy > 0 | FAIL |
| OOS expectancy >= 0.7 * IS | FAIL |
| OOS coin-flip P < 0.20 | FAIL |
| OOS max DD <= 25R | FAIL |
| OOS longest loss streak <= 8 | FAIL |
| **OVERALL** | **FAIL** |

**PASS overall** = strategy worth taking to demo paper trading.
**FAIL overall** = strategy stays in the repo as a learning artifact; any single failed criterion is enough to fail.
