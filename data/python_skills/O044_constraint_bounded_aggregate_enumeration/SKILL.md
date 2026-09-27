---
skill_id: O044
type: operator
language: python
family: streaming
name: Constraint Bounded Aggregate Enumeration
description: Optimize small integer combination searches by reasoning in terms of aggregate totals rather than generating
  all component tuples or independent candidate sets. Derive tight coefficient bounds from capacity constraints, enumerate
  one dependent component in the context of the other, apply feasibility checks immediately, deduplicate only when useful,
  and update the optimum online. When the capacity is the natural
tags:
- bounded-enumeration
- brute-force-optimization
- state-space-reduction
- reachability-dp
- deduplication
- constraint-pruning
- ratio-maximization
- integer-arithmetic
triggers:
- A solution uses several nested loops over item counts with bounds based on a loose capacity or arbitrary constants.
- Different count tuples produce the same aggregate state, while the objective and constraints depend only on those aggregates.
- Feasibility of one component depends on the value of another component through monotone capacity or ratio constraints.
- Candidate states are materialized, sorted repeatedly, or filtered only after generation.
- The original limits are small enough to derive tight count ceilings from item sizes and total capacity.
- A bounded capacity is suitable for boolean reachability or knapsack-style DP.
- The objective is a fraction or concentration that can be compared exactly with integer products.
---

## When to use
- A solution uses several nested loops over item counts with bounds based on a loose capacity or arbitrary constants.
- Different count tuples produce the same aggregate state, while the objective and constraints depend only on those aggregates.
- Feasibility of one component depends on the value of another component through monotone capacity or ratio constraints.
- Candidate states are materialized, sorted repeatedly, or filtered only after generation.
- The original limits are small enough to derive tight count ceilings from item sizes and total capacity.
- A bounded capacity is suitable for boolean reachability or knapsack-style DP.
- The objective is a fraction or concentration that can be compared exactly with integer products.

## Steps
1. Identify the minimal aggregate state needed by feasibility and the objective; discard decomposition details that do not affect the result.
2. Normalize units early so all constraints and objective comparisons use integers.
3. Derive every loop bound from the capacity and the corresponding generator size, such as capacity divided by item mass, rather than looping to the raw capacity.
4. Enumerate the less-dependent aggregate first, typically deduplicating reachable nonzero totals.
5. For each first-component total, enumerate the dependent component directly within remaining capacity and any monotone upper bound.
6. Apply all feasibility predicates during construction, including positivity, total-capacity limits, and component-relative limits.
7. Exploit monotonicity: break or skip immediately once sorted or incrementally generated values exceed a bound.
8. Track the best feasible candidate online; avoid storing all feasible combinations unless reconstruction requires it.

## Complexity
- Time: (pattern dependent)
- Space: O(|S1|) for on-the-fly dependent enumeration, O(|S1| + |S2|) when storing both deduplicated sets, O(C) for one-dimensional reachability, and O(C^2) for a two-dimensional aggregate-state DP.

## Pitfalls
- Using arbitrary loop ceilings that are larger than the maximum feasible item count.
- Generating two broad candidate sets and scanning their full Cartesian product.
- Relying on sorting to compensate for weak bounds or late feasibility checks.
- Sorting the same candidate collection inside an outer loop.
- Deduplicating only after enormous redundant tuple generation.
- Materializing every feasible state when only the optimum is needed.
- Using floating-point division for repeated ratio comparisons or boundary checks.
- Applying a break condition that prunes only the innermost loop while outer loops still enumerate impossible states.

## When not to use
- Generator counts or capacities are too large for bounded enumeration and no small state bound exists.
- The objective depends on the exact item decomposition, ordering, or selected-count vector rather than aggregate totals.
- Feasibility is nonmonotone, so early breaks or one-sided pruning are invalid.
- The aggregate state requires many dimensions, making deduplication or DP memory-prohibitive.
- A standard polynomial-time method, greedy proof, shortest-path formulation, or more scalable knapsack algorithm is clearly applicable.
- The problem requires enumerating or outputting all feasible combinations rather than only optimizing one.

## Minimal example
Before:
```py
# O044 focus: constraint
vals = []
for x in data:
    vals.append(transform(x))
ans = sum(vals)
```
After:
```py
# optimized for constraint
ans = 0
for x in data:
    ans += transform(x)
# single-pass aggregate
```
