using Bonsai;
using System;
using System.ComponentModel;
using System.Collections.Generic;
using System.Linq;
using System.Reactive.Linq;
using AindBehaviorDynamicRoutingBonsaiDataSchema;

[Combinator]
[Description("")]
[WorkflowElementCategory(ElementCategory.Transform)]
public class UniformSampleList
{
    public IObservable<T> Process<T>(IObservable<List<T>> source)
    {
        Random random = new Random();
        return source.Select(value => value[random.Next(value.Count)]); 
    }
}
