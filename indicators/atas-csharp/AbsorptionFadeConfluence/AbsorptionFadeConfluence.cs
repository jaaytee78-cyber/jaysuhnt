// =============================================================================
// AbsorptionFadeConfluence.cs
// -----------------------------------------------------------------------------
// ATAS custom indicator implementing the Absorption Fade v2 strategy.
//
// Auto-scores 4 of the 5 conditions (C2-C5). The 5th condition (C1 - location
// at a predefined HTF level) is the trader's call, exposed as a toggle.
//
// Final confluence score on the trigger bar = C2 + C3 + C4 + C5 + LevelConfirmed
// (each 0 or 1). Range 0-5. Arrow + alert fires at 5/5 in a clear direction.
//
// See: knowledge-base/strategies/absorption-fade-v2.md for the full strategy.
//
// Status: Phase-2 skeleton, compilable. Condition math uses reasonable defaults
// that need tuning once Phase 1 manual replay produces feedback. Search for
// "TUNE:" comments for the places we expect to refine.
//
// Calibration: NQ -> ImbalanceRatio = 4.0  ·  ES -> ImbalanceRatio = 3.0
// =============================================================================

using System;
using System.ComponentModel;
using System.ComponentModel.DataAnnotations;
using System.Drawing;
using ATAS.Indicators;
using OFT.Attributes;

namespace Jaysuhnt.AtasIndicators.AbsorptionFadeConfluence
{
    [DisplayName("Absorption Fade Confluence")]
    [Description("v2: 0-5 confluence score combining cluster imbalance, heavy-delta-no-progress, CVD divergence (classic|hidden), trigger bar (midpoint reclaim + delta flip), and a manual level-confirmation toggle.")]
    public class AbsorptionFadeConfluence : Indicator
    {
        // =========================================================================
        // User inputs — Footprint / imbalance
        // =========================================================================

        [Display(Name = "Imbalance Ratio", GroupName = "Footprint", Order = 10,
                 Description = "Cluster ask/bid (long) or bid/ask (short) ratio at bar extreme. NQ: 4.0  ·  ES: 3.0")]
        [Range(2.0, 10.0)]
        public decimal ImbalanceRatio { get; set; } = 4.0m;


        // =========================================================================
        // User inputs — Volume / delta / structure
        // =========================================================================

        [Display(Name = "Volume Multiplier", GroupName = "Volume", Order = 20,
                 Description = "Bar volume must be >= this multiple of the rolling avg to count as a spike.")]
        [Range(1.0, 5.0)]
        public decimal VolumeMultiplier { get; set; } = 1.5m;

        [Display(Name = "Volume Avg Period", GroupName = "Volume", Order = 30,
                 Description = "Lookback bars for the rolling volume average.")]
        [Range(5, 100)]
        public int VolumeAvgPeriod { get; set; } = 20;

        [Display(Name = "Delta Threshold %", GroupName = "Delta", Order = 40,
                 Description = "Absolute bar delta must be at least this % of bar volume.")]
        [Range(40, 95)]
        public int DeltaThresholdPct { get; set; } = 70;

        [Display(Name = "Body Close %", GroupName = "Structure", Order = 50,
                 Description = "Body must close in the OPPOSITE end <= this % of bar range.")]
        [Range(5, 50)]
        public int BodyClosePct { get; set; } = 25;

        [Display(Name = "Wick %", GroupName = "Structure", Order = 60,
                 Description = "Alternative to body close: rejection wick on the aggression side >= this % of range.")]
        [Range(30, 90)]
        public int WickPct { get; set; } = 60;

        [Display(Name = "CVD Lookback Bars", GroupName = "Divergence", Order = 70,
                 Description = "Bars back to compare for CVD divergence (classic OR hidden).")]
        [Range(3, 30)]
        public int CvdLookbackBars { get; set; } = 8;


        // =========================================================================
        // User inputs — Manual gate (C1) + alerts
        // =========================================================================

        [Display(Name = "Level Confirmed (C1)", GroupName = "Manual Gate", Order = 80,
                 Description = "YOUR call. Toggle ON when price is at a predefined HTF level (PDH/PDL, weekly H/L, VAH/VAL/POC, HVN, VWAP +/- band).")]
        public bool LevelConfirmed { get; set; } = false;

        [Display(Name = "Min Score To Arrow", GroupName = "Output", Order = 90,
                 Description = "Plot the directional arrow only when score >= this. Keep 5 for live; lower to 4 to review near-misses in replay.")]
        [Range(3, 5)]
        public int MinScoreToArrow { get; set; } = 5;

        [Display(Name = "Alert On Full Score", GroupName = "Alerts", Order = 100,
                 Description = "Pop sound + alert when score reaches 5/5.")]
        public bool AlertOnFull { get; set; } = true;

        // =========================================================================
        // Plotted series
        // =========================================================================

        // Confluence histogram (0-5) on a separate panel
        private readonly ValueDataSeries _confluence = new("Confluence (0-5)")
        {
            VisualType = VisualMode.Histogram,
            ShowZeroValue = false
        };

        // Long/short arrows on price panel
        private readonly ValueDataSeries _longSignal = new("Long signal")
        {
            VisualType = VisualMode.UpArrow,
            ShowZeroValue = false,
            Color = Color.LimeGreen,
            Width = 3
        };

        private readonly ValueDataSeries _shortSignal = new("Short signal")
        {
            VisualType = VisualMode.DownArrow,
            ShowZeroValue = false,
            Color = Color.OrangeRed,
            Width = 3
        };


        // Hidden helper series
        private readonly ValueDataSeries _cvd = new("CVD") { IsHidden = true };
        private readonly ValueDataSeries _absScore = new("Abs Score (0-3)") { IsHidden = true };
        private readonly ValueDataSeries _direction = new("Direction (-1/0/+1)") { IsHidden = true };

        // Running CVD anchored to chart start. TUNE: anchor to session boundaries.
        private decimal _runningCvd;

        // =========================================================================
        // ctor
        // =========================================================================

        public AbsorptionFadeConfluence() : base(useCandles: true)
        {
            // Histogram on its own panel
            _confluence.Panel = IndicatorDataProvider.NewPanel;

            // Arrows on price panel
            _longSignal.Panel = IndicatorDataProvider.CandlesPanel;
            _shortSignal.Panel = IndicatorDataProvider.CandlesPanel;

            DataSeries[0] = _confluence;
            DataSeries.Add(_longSignal);
            DataSeries.Add(_shortSignal);
            DataSeries.Add(_cvd);
            DataSeries.Add(_absScore);
            DataSeries.Add(_direction);
        }

        // =========================================================================
        // Main calculation
        // =========================================================================

        protected override void OnCalculate(int bar, decimal value)
        {
            // Need enough history before we can score anything
            int warmup = Math.Max(VolumeAvgPeriod, CvdLookbackBars) + 2;
            if (bar < warmup) return;

            var candle = GetCandle(bar);

            // Update running CVD using the prior CLOSED bar's delta only
            // (avoids double-counting on tick updates of the live bar).
            // TUNE: replace with session-anchored CVD when we add session detection.
            if (bar > 0)
                _runningCvd += GetCandle(bar - 1).Delta;
            _cvd[bar] = _runningCvd;


            // ----- C2: Cluster imbalance at bar extreme ---------------------------
            // Long: ask/bid >= ratio at bar low.   Short: bid/ask >= ratio at bar high.
            bool c2_askAbsorption = false;   // long signal
            bool c2_bidAbsorption = false;   // short signal
            decimal tickSize = InstrumentInfo?.TickSize ?? 0.25m;
            decimal extremeBand = 4m * tickSize;   // count clusters within 4 ticks of high/low

            if (candle.Clusters != null)
            {
                foreach (var cl in candle.Clusters)
                {
                    if (cl.BidVolume <= 0 || cl.AskVolume <= 0) continue;

                    // Near bar low -> long candidate
                    if (cl.Price <= candle.Low + extremeBand)
                    {
                        decimal ratio = cl.AskVolume / (decimal)cl.BidVolume;
                        if (ratio >= ImbalanceRatio) c2_askAbsorption = true;
                    }
                    // Near bar high -> short candidate
                    if (cl.Price >= candle.High - extremeBand)
                    {
                        decimal ratio = cl.BidVolume / (decimal)cl.AskVolume;
                        if (ratio >= ImbalanceRatio) c2_bidAbsorption = true;
                    }
                }
            }

            // ----- C3: Heavy delta + no progress (volume + delta + structure) ----
            decimal volSum = 0;
            for (int i = 1; i <= VolumeAvgPeriod; i++)
                volSum += GetCandle(bar - i).Volume;
            decimal volAvg = volSum / VolumeAvgPeriod;

            bool volSpike = volAvg > 0 && candle.Volume >= volAvg * VolumeMultiplier;
            bool deltaHeavy = candle.Volume > 0
                && Math.Abs(candle.Delta) >= candle.Volume * (DeltaThresholdPct / 100m);


            int direction = 0;            // -1 short, +1 long, 0 none
            bool c3_noProgress = false;
            decimal range = candle.High - candle.Low;

            if (range > 0 && volSpike && deltaHeavy)
            {
                decimal closePosFromLow = (candle.Close - candle.Low) / range;   // 0..1
                decimal upperWickPct = (candle.High - Math.Max(candle.Open, candle.Close)) / range;
                decimal lowerWickPct = (Math.Min(candle.Open, candle.Close) - candle.Low) / range;

                if (candle.Delta > 0)
                {
                    // Buy aggression that failed to push higher -> fade SHORT
                    bool closedLow = closePosFromLow <= (BodyClosePct / 100m);
                    bool bigUpperWick = upperWickPct >= (WickPct / 100m);
                    if (closedLow || bigUpperWick) { c3_noProgress = true; direction = -1; }
                }
                else if (candle.Delta < 0)
                {
                    // Sell aggression that failed to push lower -> fade LONG
                    bool closedHigh = closePosFromLow >= (1m - (BodyClosePct / 100m));
                    bool bigLowerWick = lowerWickPct >= (WickPct / 100m);
                    if (closedHigh || bigLowerWick) { c3_noProgress = true; direction = +1; }
                }
            }

            // ----- C4: CVD divergence (classic OR hidden) -------------------------
            // Walk back the lookback window to find the prior pivot extreme + its CVD.
            // Classic LONG : current bar prints lower low than prior, CVD higher than at prior low.
            // Hidden  LONG : CVD lower than at prior low, but price held above prior low.
            // Mirror for SHORT.
            bool c4_long = false, c4_short = false;
            if (bar - CvdLookbackBars > 0)
            {
                decimal priorLow = decimal.MaxValue, priorHigh = decimal.MinValue;
                decimal cvdAtPriorLow = 0m, cvdAtPriorHigh = 0m;
                for (int i = bar - CvdLookbackBars; i < bar; i++)
                {
                    var c = GetCandle(i);
                    if (c.Low < priorLow) { priorLow = c.Low; cvdAtPriorLow = _cvd[i]; }
                    if (c.High > priorHigh) { priorHigh = c.High; cvdAtPriorHigh = _cvd[i]; }
                }


                // Classic long: price made new low, CVD did NOT confirm (CVD higher than at prior low)
                bool classicLong = candle.Low <= priorLow && _runningCvd > cvdAtPriorLow;
                // Hidden long: CVD made new low, price did NOT (price held above prior low)
                bool hiddenLong = _runningCvd < cvdAtPriorLow && candle.Low > priorLow;
                c4_long = classicLong || hiddenLong;

                // Classic short: price new high, CVD didn't confirm (CVD lower than at prior high)
                bool classicShort = candle.High >= priorHigh && _runningCvd < cvdAtPriorHigh;
                // Hidden short: CVD made new high, price didn't (price held below prior high)
                bool hiddenShort = _runningCvd > cvdAtPriorHigh && candle.High < priorHigh;
                c4_short = classicShort || hiddenShort;
            }

            // ----- Score this bar AS AN ABSORPTION CANDIDATE (C2 + C3 + C4) -------
            // Direction-aware: only count C2/C4 in the implied direction.
            int absScore = 0;
            if (direction == +1)
            {
                if (c2_askAbsorption) absScore++;   // C2 long
                if (c3_noProgress) absScore++;      // C3 (already direction-aware)
                if (c4_long) absScore++;            // C4 long
            }
            else if (direction == -1)
            {
                if (c2_bidAbsorption) absScore++;
                if (c3_noProgress) absScore++;
                if (c4_short) absScore++;
            }
            // If direction == 0 absScore stays 0 (no absorption candidate this bar).

            _absScore[bar] = absScore;
            _direction[bar] = direction;

            // ----- C5: Trigger bar = bar AFTER an absorption candidate ------------
            // Look at bar-1: if it was a candidate (absScore >= 2 with a direction),
            // check whether THIS bar reclaims its midpoint AND has opposite delta sign.
            int prevAbsScore = (int)_absScore[bar - 1];
            int prevDir = (int)_direction[bar - 1];
            bool c5 = false;
            int triggerDir = 0;


            if (prevAbsScore >= 2 && prevDir != 0)
            {
                var absorption = GetCandle(bar - 1);
                decimal mid = (absorption.High + absorption.Low) / 2m;

                // Long fade: prev was sell-aggression-that-failed (prevDir = +1)
                //            this bar must close ABOVE mid AND have positive delta
                if (prevDir == +1 && candle.Close > mid && candle.Delta > 0)
                {
                    c5 = true; triggerDir = +1;
                }
                // Short fade: prev was buy-aggression-that-failed (prevDir = -1)
                //             this bar must close BELOW mid AND have negative delta
                else if (prevDir == -1 && candle.Close < mid && candle.Delta < 0)
                {
                    c5 = true; triggerDir = -1;
                }
            }

            // ----- Final confluence at the trigger bar ---------------------------
            // confluence = absScore(prev) + C5 + LevelConfirmed
            // Range 0-5. Cap at 5.
            int confluence = 0;
            if (c5)
            {
                confluence = prevAbsScore + 1 + (LevelConfirmed ? 1 : 0);
            }
            else
            {
                // No trigger yet — show the candidate score from this bar so user sees
                // confluence building. Add level toggle if active.
                confluence = absScore + (LevelConfirmed ? 1 : 0);
            }
            if (confluence > 5) confluence = 5;
            _confluence[bar] = confluence;

            // Color the histogram by score
            _confluence.Colors[bar] = confluence >= 5 ? Color.FromArgb(255, 0, 255, 136)
                                  : confluence == 4 ? Color.FromArgb(255, 100, 220, 80)
                                  : confluence == 3 ? Color.FromArgb(255, 255, 200, 0)
                                  : confluence == 2 ? Color.FromArgb(255, 100, 130, 160)
                                  : Color.FromArgb(255, 80, 100, 120);


            // ----- Plot arrow + alert at threshold -------------------------------
            if (c5 && triggerDir != 0 && confluence >= MinScoreToArrow)
            {
                if (triggerDir == +1)
                {
                    // Long arrow below the trigger bar
                    _longSignal[bar] = candle.Low - 4 * tickSize;
                    _shortSignal[bar] = 0;
                    if (AlertOnFull && confluence >= 5)
                        TryAlert("AF v2 LONG — 5/5 confluence");
                }
                else
                {
                    // Short arrow above the trigger bar
                    _shortSignal[bar] = candle.High + 4 * tickSize;
                    _longSignal[bar] = 0;
                    if (AlertOnFull && confluence >= 5)
                        TryAlert("AF v2 SHORT — 5/5 confluence");
                }
            }
            else
            {
                _longSignal[bar] = 0;
                _shortSignal[bar] = 0;
            }
        }

        // =========================================================================
        // Helpers
        // =========================================================================

        private void TryAlert(string message)
        {
            // ATAS AddAlert signatures vary slightly by version. Wrap in try/catch
            // so an alert failure never breaks scoring.
            try { AddAlert("alert1.wav", message); }
            catch { /* swallow — alerts are nice-to-have, not critical */ }
        }
    }
}
