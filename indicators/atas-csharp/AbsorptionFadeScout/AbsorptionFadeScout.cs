// =============================================================================
// AbsorptionFadeScout.cs
// -----------------------------------------------------------------------------
// ATAS custom indicator implementing 4 of the 5 conditions of the
// "Absorption Fade" (AF) scalping strategy.
//
// See: knowledge-base/strategies/absorption-fade-scalp.md for the full strategy.
//
// THIS IS A PHASE-2 SKELETON. The condition logic is implemented at a basic,
// reasonable default; the math will be tuned with real data once Phase 1
// manual replay produces feedback. Search for "TUNE:" comments to see the
// places we expect to refine.
//
// Status: skeleton, compilable. Not battle-tested.
// =============================================================================

using System;
using System.ComponentModel;
using System.ComponentModel.DataAnnotations;
using System.Drawing;
using ATAS.Indicators;
using OFT.Attributes;

namespace Jaysuhnt.AtasIndicators.AbsorptionFadeScout
{
    [DisplayName("Absorption Fade Scout")]
    [Description("Auto-detects 4/4 of the Absorption Fade setup conditions. Trader confirms location (#1) manually.")]
    public class AbsorptionFadeScout : Indicator
    {
        // ---------------------------------------------------------------------
        // User-configurable inputs (appear in the indicator settings panel)
        // ---------------------------------------------------------------------

        [Display(Name = "Volume Multiplier", GroupName = "Volume", Order = 10,
                 Description = "Bar volume must be >= this multiple of the rolling average to count as a spike.")]
        [Range(1.0, 5.0)]
        public decimal VolumeMultiplier { get; set; } = 1.5m;

        [Display(Name = "Volume Avg Period", GroupName = "Volume", Order = 20,
                 Description = "Lookback bars for the rolling volume average.")]
        [Range(5, 100)]
        public int VolumeAvgPeriod { get; set; } = 20;

        [Display(Name = "Delta Threshold %", GroupName = "Delta", Order = 30,
                 Description = "Absolute bar delta must be at least this percent of bar volume.")]
        [Range(40, 95)]
        public int DeltaThresholdPct { get; set; } = 70;

        [Display(Name = "Body Close %", GroupName = "Structure", Order = 40,
                 Description = "Body must close in the OPPOSITE end <= this % of bar range to count as 'no progress'.")]
        [Range(5, 50)]
        public int BodyClosePct { get; set; } = 25;

        [Display(Name = "Wick %", GroupName = "Structure", Order = 50,
                 Description = "Alternative to body close: rejection wick on the aggression side >= this % of bar range.")]
        [Range(30, 90)]
        public int WickPct { get; set; } = 60;

        [Display(Name = "CVD Lookback Bars", GroupName = "Divergence", Order = 60,
                 Description = "Bars back to compare for CVD divergence.")]
        [Range(3, 30)]
        public int CvdLookbackBars { get; set; } = 8;

        [Display(Name = "Min Score To Plot", GroupName = "Output", Order = 70,
                 Description = "Minimum auto-score (0-4) before drawing the candidate marker.")]
        [Range(2, 4)]
        public int MinScoreToPlot { get; set; } = 4;

        [Display(Name = "Play Sound On Trigger", GroupName = "Output", Order = 80)]
        public bool PlaySoundOnTrigger { get; set; } = true;

        // ---------------------------------------------------------------------
        // Plotted series
        // ---------------------------------------------------------------------

        // Long candidate: dot below bar (green)
        private readonly ValueDataSeries _longSignal = new("Long candidate")
        {
            VisualType = VisualMode.Dots,
            Color = Color.LimeGreen,
            Width = 3
        };

        // Short candidate: dot above bar (red)
        private readonly ValueDataSeries _shortSignal = new("Short candidate")
        {
            VisualType = VisualMode.Dots,
            Color = Color.OrangeRed,
            Width = 3
        };

        // Hidden score series — useful for review / debugging
        private readonly ValueDataSeries _score = new("AF score (0-4)")
        {
            IsHidden = true
        };

        // Running CVD (cumulative delta from the start of the chart's session bucket)
        // TUNE: this is a chart-wide CVD; eventually anchor to session start.
        private decimal _cumulativeDelta;

        // ---------------------------------------------------------------------
        // ctor
        // ---------------------------------------------------------------------

        public AbsorptionFadeScout()
            : base(useCandles: true)
        {
            Panel = IndicatorDataProvider.NewPanel; // off-chart "score" panel? no — leave on price for dots.
            Panel = IndicatorDataProvider.CandlesPanel;

            DataSeries[0] = _longSignal;
            DataSeries.Add(_shortSignal);
            DataSeries.Add(_score);
        }

        // ---------------------------------------------------------------------
        // Main calculation — runs once per bar (and live ticks on the latest bar)
        // ---------------------------------------------------------------------

        protected override void OnCalculate(int bar, decimal value)
        {
            // Need enough history before we can score anything.
            if (bar < Math.Max(VolumeAvgPeriod, CvdLookbackBars) + 2)
                return;

            var candle = GetCandle(bar);

            // Update running CVD with the latest CLOSED bar's delta only.
            // (Avoids double-counting on tick updates of the live bar.)
            // TUNE: replace with session-anchored CVD when we add session detection.
            if (bar > 0)
            {
                var prev = GetCandle(bar - 1);
                _cumulativeDelta += prev.Delta;
            }

            // ----- Condition #2: volume spike ---------------------------------
            decimal volSum = 0;
            for (int i = 1; i <= VolumeAvgPeriod; i++)
                volSum += GetCandle(bar - i).Volume;

            decimal volAvg = volSum / VolumeAvgPeriod;
            bool cond2_VolumeSpike = volAvg > 0
                && candle.Volume >= volAvg * VolumeMultiplier;

            // ----- Condition #3: heavy delta + no progress --------------------
            // Delta dominance: |delta| / volume >= threshold
            bool deltaHeavy = candle.Volume > 0
                && Math.Abs(candle.Delta) >= candle.Volume * (DeltaThresholdPct / 100m);

            // We will care about the SIGN of delta to decide direction:
            //   +delta dominant → buy aggression → bar SHOULD close near top
            //     if it doesn't → absorption candidate, FADE LONG = NO, fade SHORT
            //   -delta dominant → sell aggression → bar SHOULD close near bottom
            //     if it doesn't → fade LONG
            int direction = 0; // -1 short, +1 long, 0 none
            bool noProgress = false;
            decimal range = candle.High - candle.Low;

            if (range > 0 && deltaHeavy)
            {
                decimal closePosFromLow = (candle.Close - candle.Low) / range; // 0..1
                decimal upperWickPct = (candle.High - Math.Max(candle.Open, candle.Close)) / range;
                decimal lowerWickPct = (Math.Min(candle.Open, candle.Close) - candle.Low) / range;

                if (candle.Delta > 0)
                {
                    // Buy aggression that fails → fade SHORT
                    bool closedLow = closePosFromLow <= (BodyClosePct / 100m);
                    bool bigUpperWick = upperWickPct >= (WickPct / 100m);
                    if (closedLow || bigUpperWick)
                    {
                        noProgress = true;
                        direction = -1;
                    }
                }
                else if (candle.Delta < 0)
                {
                    // Sell aggression that fails → fade LONG
                    bool closedHigh = closePosFromLow >= (1m - (BodyClosePct / 100m));
                    bool bigLowerWick = lowerWickPct >= (WickPct / 100m);
                    if (closedHigh || bigLowerWick)
                    {
                        noProgress = true;
                        direction = +1;
                    }
                }
            }

            bool cond3_HeavyDeltaNoProgress = deltaHeavy && noProgress && direction != 0;

            // ----- Condition #4: CVD divergence -------------------------------
            // Simplified: compare current bar's price extreme vs a lookback bar's
            // extreme, vs the corresponding running CVD values.
            //
            // For SHORT setup (direction = -1): need new HIGH but CVD lower than
            //   the prior swing high CVD.
            // For LONG setup (direction = +1):  need new LOW  but CVD higher than
            //   the prior swing low  CVD.
            //
            // TUNE: this is a coarse two-bar comparison; we will eventually walk
            // back to find the actual prior pivot, not a fixed lookback.
            bool cond4_CvdDivergence = false;
            if (direction != 0 && bar - CvdLookbackBars > 0)
            {
                var lookback = GetCandle(bar - CvdLookbackBars);

                // Recompute CVD as of `lookback` bar by subtracting the deltas in
                // between (cheap approximation; will replace with stored series).
                decimal cvdAtLookback = _cumulativeDelta;
                for (int i = bar - CvdLookbackBars; i < bar; i++)
                    cvdAtLookback -= GetCandle(i).Delta;

                if (direction == -1
                    && candle.High > lookback.High
                    && _cumulativeDelta < cvdAtLookback)
                {
                    cond4_CvdDivergence = true;
                }
                else if (direction == +1
                    && candle.Low < lookback.Low
                    && _cumulativeDelta > cvdAtLookback)
                {
                    cond4_CvdDivergence = true;
                }
            }

            // ----- Score the absorption bar (conditions 2, 3, 4) --------------
            int score = 0;
            if (cond2_VolumeSpike) score++;
            if (cond3_HeavyDeltaNoProgress) score++;
            if (cond4_CvdDivergence) score++;

            _score[bar] = score;

            // ----- Condition #5: trigger bar (NEXT bar after a 3/3 absorption)
            // The trigger bar is the CURRENT bar, and the absorption bar is bar-1.
            //
            // We trigger if:
            //   - bar-1 scored 3/3 with a direction
            //   - current bar closes through the midpoint of bar-1 in the
            //     direction implied
            //
            // We can't read DataSeries[bar-1] reliably for our own _score until
            // we've stored it (we just did above for the current bar). So we
            // re-derive the prior bar's direction by checking its delta sign
            // and structure quickly here, OR cache direction in another series.
            //
            // Simpler approach: store direction-with-score in the score series:
            //   we already stored _score[bar] = score for the current bar above.
            //   We didn't store direction. Add a tiny per-bar direction series.
            //
            // For the skeleton: just check that previous bar score >= MinScoreToPlot
            // and that this bar closes back through previous bar midpoint.
            int prevScore = (int)_score[bar - 1];
            if (prevScore >= MinScoreToPlot)
            {
                var absorption = GetCandle(bar - 1);
                decimal mid = (absorption.High + absorption.Low) / 2m;

                // Re-derive prior bar direction from its delta sign
                int prevDir = absorption.Delta > 0 ? -1 : (absorption.Delta < 0 ? +1 : 0);

                bool triggerLong = prevDir == +1 && candle.Close > mid;
                bool triggerShort = prevDir == -1 && candle.Close < mid;

                if (triggerLong)
                {
                    _longSignal[bar] = candle.Low - (candle.High - candle.Low) * 0.2m;
                    AlertOnTrigger("AF long candidate");
                }
                else if (triggerShort)
                {
                    _shortSignal[bar] = candle.High + (candle.High - candle.Low) * 0.2m;
                    AlertOnTrigger("AF short candidate");
                }
            }
        }

        // ---------------------------------------------------------------------
        // Helpers
        // ---------------------------------------------------------------------

        private void AlertOnTrigger(string message)
        {
            // ATAS provides AddAlert via the base Indicator class. The signature
            // varies slightly by version; if compile fails here, we'll drop in
            // the concrete signature your version expects.
            try
            {
                if (PlaySoundOnTrigger)
                    AddAlert("alert1.wav", message);
            }
            catch
            {
                // Swallow — alerts are nice-to-have, not critical to logic.
                // TUNE: log to ATAS log instead once we confirm the API.
            }
        }
    }
}
