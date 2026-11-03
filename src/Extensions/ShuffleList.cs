using Bonsai;
using System;
using System.ComponentModel;
using System.Collections.Generic;
using System.Linq;
using System.Reactive.Linq;

[Combinator]
[Description("")]
[WorkflowElementCategory(ElementCategory.Transform)]
public class ShuffleList
{
    [Description("The seed for the random number generator. If not specified, a time-dependent seed is used.")]
    public int? Seed { get; set; }

    public IObservable<List<T>> Process<T>(IObservable<List<T>> source)
    {
        // Created on the first value so that a Seed set by a property mapping is applied,
        // and shared across subscriptions so that repeated shuffles differ from each other.
        Random random = null;
        return source.Select(value =>
        {
            if (random == null) random = Seed.HasValue ? new Random(Seed.Value) : new Random();
            return value.OrderBy(x => random.Next()).ToList();
        });
    }
}
