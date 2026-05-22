# Strategies

This folder is where I document each mechanical strategy I'm studying or testing. The goal: turn ideas into rules, rules into backtests, backtests into trades, trades into a journal.

## Index

| # | Strategy | Instrument | Status | Notes |
|---|---|---|---|---|
| 01 | [5-Minute Opening Range Breakout (ORB)](./01-orb-5min-nasdaq.md) | NAS100 / NQ / QQQ / TQQQ | Studying | Academically proven, fully mechanical |

## My filter for adding a strategy here

A strategy makes it into this folder only if I can answer **yes** to all of these:

1. Are the rules **mechanical** — i.e., a robot could trade it without judgement?
2. Is there **published evidence** of edge (peer-reviewed paper, large-sample backtest, or my own 200+ trade backtest)?
3. Can it be traded inside my **available time window** (London + NY killzones)?
4. Does it fit my **instrument list** (NAS100 first, then XAU, EUR, GBP)?
5. Is the **R-multiple math** workable on a small account with realistic spreads/commissions?

If any answer is "no", the idea goes in the `knowledge-base/ict-smc/` notes for further study, not here.
