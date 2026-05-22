# OR Sweep & Reversal - Edge Analysis (QQQ 1m)

Data window     : 2024-05-22 -> 2026-05-21
Days with full OR + trade window : **501**
Days with a first sweep          : **453**

All R-multiples assume:
- Entry  = close of the sweep bar
- Stop   = sweep wick + 1 cent
- Target = opposite OR side
- Time-stop = 11:00 NY (last bar of trade window)
- 1 trade per day max, no costs/slippage applied here (pure edge measurement).

## 1. Opening Range size distribution

OR size in dollars (per share, QQQ):
```
count    501.000000
mean       2.531716
std        1.242202
min        0.720000
10%        1.260000
25%        1.635000
50%        2.259200
75%        3.060000
90%        4.160000
max        8.800000
```

OR size as % of OR open price:
```
count    501.000000
mean       0.469212
std        0.245005
min        0.143174
10%        0.238734
50%        0.403532
90%        0.764413
max        2.072002
```

## 2. Sweep frequency in [09:45, 11:00) NY

- P(any sweep)         : **90.42%**  (453/501 days)
- P(upper sweep first) : 44.31%
- P(lower sweep first) : 46.11%
- P(no sweep)          :  9.58%

## 3. Headline edge (all sweep days, no filters)

### Pooled - all years, all weekdays

- Days total              : **501**
- Days with a sweep       : **453** (90.42% of days)
- P(upper sweep first)    : 49.01%
- P(target hit)           : **16.78%**
- P(stop hit)             : 80.13%
- P(timeout / time-stop)  :  3.09%
- Win rate (R > 0)        : **19.43%**
- Expectancy per setup    : **+0.132R**
- Median R                : -1.000R
- Avg win / avg loss      : +4.807R / -0.998R
- Median OR size          : $2.28

> **Verdict:** positive expectancy.  Worth pushing into Phase 2 backtest.

## 4. Edge by year (regime stability)

```
      n_days sweep_rate win_rate expectancy_R p_target  p_stop
year                                                          
2024     154     91.56%   17.02%       0.078R    15.6%  82.98%
2025     250      89.6%   21.88%       0.164R   17.86%  78.12%
2026      97     90.72%   17.05%       0.138R   15.91%  80.68%
```

## 5. Edge by weekday

```
         n_days sweep_rate win_rate expectancy_R
weekday                                         
Mon          96     91.67%   14.77%      -0.188R
Tue         104      87.5%   28.57%       0.672R
Wed         102     94.12%   18.75%       0.148R
Thu          98      89.8%   17.05%       0.069R
Fri         101     89.11%   17.78%      -0.061R
```

## 6. Edge by sweep side

### Upper sweep (= short)

- Days total              : **222**
- Days with a sweep       : **222** (100.00% of days)
- P(upper sweep first)    : 100.00%
- P(target hit)           : **15.77%**
- P(stop hit)             : 81.98%
- P(timeout / time-stop)  :  2.25%
- Win rate (R > 0)        : **17.57%**
- Expectancy per setup    : **+0.139R**
- Median R                : -1.000R
- Avg win / avg loss      : +5.468R / -0.997R
- Median OR size          : $2.29

### Lower sweep (= long)

- Days total              : **231**
- Days with a sweep       : **231** (100.00% of days)
- P(upper sweep first)    :  0.00%
- P(target hit)           : **17.75%**
- P(stop hit)             : 78.35%
- P(timeout / time-stop)  :  3.90%
- Win rate (R > 0)        : **21.21%**
- Expectancy per setup    : **+0.125R**
- Median R                : -1.000R
- Avg win / avg loss      : +4.282R / -1.000R
- Median OR size          : $2.28


## 7. R-multiple distribution (sweep days only)

```
  <= -1R        363   (80.13%)
  -1R..-0.5R      0   ( 0.00%)
  -0.5R..0        1   ( 0.22%)
  0..0.5R         0   ( 0.00%)
  0.5R..1R        6   ( 1.32%)
  1R..2R         15   ( 3.31%)
  > 2R           67   (14.79%)
```

## 8. Time-to-target (winners only)

```
count    76.000000
mean     16.842105
std      13.590244
min       1.000000
25%       7.000000
50%      12.000000
75%      24.250000
90%      35.500000
max      61.000000
```
Implied: most winners hit target within ~12 minutes of the sweep bar.