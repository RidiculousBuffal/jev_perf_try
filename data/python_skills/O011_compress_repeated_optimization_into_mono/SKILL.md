---
skill_id: O011
type: operator
language: python
family: streaming
name: Compress Repeated Optimization into Monotone Feasibility, Greedy State, or Algebraic Candidates
description: Reusable optimization pattern distilled from weighted traces.
tags:
- binary-search-on-answer
- monotone-feasibility
- greedy-state-compression
- bruteforce-to-greedy
- algebraic-reformulation
- closed-form-case-analysis
- streaming-minimum
- candidate-pruning
- aggregation
- simulation-elimination
triggers:
- The objective asks for the smallest or largest threshold satisfying a condition that becomes permanently true or false as
  the threshold changes.
- A binary-search check scans the full array and performs repeated expensive arithmetic, allocation, or library calls.
- A process repeatedly sorts, redistributes, or applies uniform updates even though the final result may depend only on total
  operations and per-item deficits.
- A brute-force search assigns each of n items to one of a fixed small number of groups and validates monotonicity or threshold
  constraints afterward.
- A loop enumerates operation orders whose effects can be compared by a local swap argument.
- A loop evaluates many scalar candidates and calls min() once, or stores candidates that are never reused.
- A loop repeatedly adds the same constant or evaluates a piecewise-linear cost over a one-dimensional count.
- A shared bundle or paired action affects two demands symmetrically.
---

## When to use
- The objective asks for the smallest or largest threshold satisfying a condition that becomes permanently true or false as the threshold changes.
- A binary-search check scans the full array and performs repeated expensive arithmetic, allocation, or library calls.
- A process repeatedly sorts, redistributes, or applies uniform updates even though the final result may depend only on total operations and per-item deficits.
- A brute-force search assigns each of n items to one of a fixed small number of groups and validates monotonicity or threshold constraints afterward.
- A loop enumerates operation orders whose effects can be compared by a local swap argument.
- A loop evaluates many scalar candidates and calls min() once, or stores candidates that are never reused.
- A loop repeatedly adds the same constant or evaluates a piecewise-linear cost over a one-dimensional count.
- A shared bundle or paired action affects two demands symmetrically.

## Steps
1. State the original decision or optimization predicate precisely and identify the true answer variable.
2. Look for monotonicity: prove that feasibility at one candidate implies feasibility for all smaller or larger candidates.
3. Replace direct minimization or simulation with a feasibility function and binary search the tightest valid answer range.
4. Derive a safe, constraint-based search bound such as [0, max(initial objective)] instead of an unnecessarily huge constant.
5. Rewrite per-item requirements using integer arithmetic, especially ceil division as (x + d - 1) // d, and avoid floating-point operations when exact counts are intended.
6. In each feasibility check, skip already-satisfied items, accumulate required work directly, and break immediately once the global budget is exceeded.
7. If the same check repeats over large data, replace Python-level vector loops and temporary arrays with one tight scalar loop or carefully chosen bulk operations.
8. For two-way monotone partitioning, maintain only the current tail of each subsequence; place each value on the largest tail it can extend and fail immediately if neither tail accepts it.

## Complexity
- Time: Common target: O(n log U) for monotone answer search with an O(n) feasibility check; O(n) for fixed-width greedy state compression or aggregate scans; O(1) when a piecewise-linear enumeration reduces to a constant number of cases
- Space: Prefer O(1) auxiliary space for streaming minima, greedy tails, algebraic formulas, and direct feasibility scans. Use O(n) space when sorting, storing input, or precomputing products is useful. Avoid per-subset or per-probe temporary

## Pitfalls
- Using binary search without proving monotonicity or reversing the direction of the predicate.
- Choosing an unnecessarily large search interval and paying for extra feasibility probes.
- Replacing a direct closed-form minimum with binary search when the direct formula is simpler, faster, and numerically safe.
- Assuming a greedy tail rule is valid without proving that the retained frontier state preserves all future feasibility information.
- Initializing greedy tails or counters with domain-specific sentinels such as zero when negative or zero-valued inputs are possible.
- Using global top values instead of per-subsequence tails in sequence-partition problems.
- Simulating every operation, sorting after every update, or repeatedly applying uniform changes instead of deriving aggregate counts.
- Using floating-point ceil, division, or formatting for exact integer quantities.

## When not to use
- The feasibility predicate is not monotone or cannot be evaluated reliably for a candidate answer.
- The input size is genuinely small and exhaustive enumeration is simpler, safer, and comfortably within limits.
- The proposed greedy state discards information that can affect future choices and no exchange argument or invariant proves sufficiency.
- The objective depends on path-dependent side effects, order interactions, or nonlocal state that cannot be summarized by counts or frontiers.
- Vectorized libraries are demonstrably faster for the actual array sizes and are permitted by the execution environment.
- A fixed constraint cap is unknown, unstable, or too large for bounded enumeration.

## Minimal example
Before:
```py
# O011 focus: compress
vals = []
for x in data:
    vals.append(transform(x))
ans = sum(vals)
```
After:
```py
# optimized for compress
ans = 0
for x in data:
    ans += transform(x)
# single-pass aggregate
```
