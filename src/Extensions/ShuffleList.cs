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
    Random random = new Random();
    public IObservable<List<T>> Process<T>(IObservable<List<T>> source)
    {
        return source.Select(value => value.OrderBy(x => random.Next()).ToList());
    }
}