using Bonsai;
using System;
using System.ComponentModel;
using System.Collections.Generic;
using System.Linq;
using System.Reactive.Linq;
using AindBehaviorDynamicRoutingBonsaiDataSchema;

[Combinator]
[Description("Shuffles the available trials of a trial set, limiting the number of consecutive rewarded or unrewarded trials to the trial set's MaxConsecutiveSameReward.")]
[WorkflowElementCategory(ElementCategory.Transform)]
public class ShuffleTrialSet
{
    [Description("The seed for the random number generator. If not specified, a time-dependent seed is used.")]
    public int? Seed { get; set; }

    public IObservable<List<Trial>> Process(IObservable<TrialSet> source)
    {
        // Created on the first value so that a Seed set by a property mapping is applied,
        // and shared across subscriptions so that each repeat and trial set is shuffled differently.
        Random random = null;
        return source.Select(trialSet =>
        {
            if (random == null) random = Seed.HasValue ? new Random(Seed.Value) : new Random();
            var trials = trialSet.AvailableTrials;
            var maxConsecutive = trialSet.MaxConsecutiveSameReward;
            if (!maxConsecutive.HasValue)
            {
                return trials.OrderBy(x => random.Next()).ToList();
            }

            var rewarded = trials.Where(x => x.PresentationParameters.Rewarded).OrderBy(x => random.Next()).ToList();
            var unrewarded = trials.Where(x => !x.PresentationParameters.Rewarded).OrderBy(x => random.Next()).ToList();
            if (!IsFeasible(rewarded.Count, unrewarded.Count, 0, maxConsecutive.Value))
            {
                throw new InvalidOperationException(string.Format(
                    "Cannot order {0} rewarded and {1} unrewarded trials with at most {2} consecutive trials of the same type.",
                    rewarded.Count, unrewarded.Count, maxConsecutive.Value));
            }

            var result = new List<Trial>(trials.Count);
            bool? lastRewarded = null;
            var runLength = 0;
            while (rewarded.Count > 0 || unrewarded.Count > 0)
            {
                var canPickRewarded = CanPick(true, rewarded, unrewarded, lastRewarded, runLength, maxConsecutive.Value);
                var canPickUnrewarded = CanPick(false, rewarded, unrewarded, lastRewarded, runLength, maxConsecutive.Value);

                // Weight the choice by the number of remaining trials of each type
                bool pickRewarded;
                if (canPickRewarded && canPickUnrewarded)
                {
                    pickRewarded = random.Next(rewarded.Count + unrewarded.Count) < rewarded.Count;
                }
                else pickRewarded = canPickRewarded;

                var pool = pickRewarded ? rewarded : unrewarded;
                result.Add(pool[pool.Count - 1]);
                pool.RemoveAt(pool.Count - 1);
                runLength = lastRewarded == pickRewarded ? runLength + 1 : 1;
                lastRewarded = pickRewarded;
            }

            return result;
        });
    }

    // Whether picking a trial of the given type keeps the run within the limit
    // and leaves a remainder that can still be ordered.
    static bool CanPick(bool pickRewarded, List<Trial> rewarded, List<Trial> unrewarded, bool? lastRewarded, int runLength, int maxConsecutive)
    {
        var same = pickRewarded ? rewarded.Count : unrewarded.Count;
        var other = pickRewarded ? unrewarded.Count : rewarded.Count;
        if (same == 0) return false;

        var newRunLength = lastRewarded == pickRewarded ? runLength + 1 : 1;
        if (newRunLength > maxConsecutive) return false;
        return IsFeasible(same - 1, other, newRunLength, maxConsecutive);
    }

    // Whether 'current' trials of the type ending the sequence (with a run of 'runLength')
    // and 'other' trials of the opposite type can be ordered within the limit.
    static bool IsFeasible(int current, int other, int runLength, int maxConsecutive)
    {
        return current <= (maxConsecutive - runLength) + maxConsecutive * other
            && other <= maxConsecutive * (current + 1);
    }
}
