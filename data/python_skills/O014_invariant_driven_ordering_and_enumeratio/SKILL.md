---
skill_id: O014
type: operator
language: python
family: combinatorics
name: Invariant Driven Ordering and Enumeration Reduction
description: Replace indirect simulations, repeated sorting, exhaustive candidate materialization, and numeric-range scans
  with the smallest data structure or formula that preserves the required invariant. First identify whether decisions depend
  on global order, extrema, bounded values, a monotone frontier, a FIFO stream, or direct index mapping. Then use one-time
  sorting plus a fold, a heap or ordered multiset for dynamic
tags:
- algorithmic-reduction
- greedy
- sorting
- heap
- best-first-search
- ordered-multiset
- binary-search
- counting
- extrema
- interval-arithmetic
triggers:
- The same collection is globally sorted inside a loop after only a small update.
- The operation repeatedly selects the current minimum or maximum.
- State is partitioned by history or level even though the next decision depends only on current value order.
- A Python list uses pop(0), repeated front deletion, or repeated full scans in a hot loop.
- Only the top K combinations are needed, but code constructs and sorts a large Cartesian product.
- A loop enumerates every integer in a range to test whether any value satisfies monotone inequalities.
- Sorted data is used only for a few extrema, middle values, or a fixed-rank prefix.
- A result depends only on aggregate values, residues, minima, maxima, or a small number of exceptional elements.
---

## When to use
- The same collection is globally sorted inside a loop after only a small update.
- The operation repeatedly selects the current minimum or maximum.
- State is partitioned by history or level even though the next decision depends only on current value order.
- A Python list uses pop(0), repeated front deletion, or repeated full scans in a hot loop.
- Only the top K combinations are needed, but code constructs and sorts a large Cartesian product.
- A loop enumerates every integer in a range to test whether any value satisfies monotone inequalities.
- Sorted data is used only for a few extrema, middle values, or a fixed-rank prefix.
- A result depends only on aggregate values, residues, minima, maxima, or a small number of exceptional elements.

## Steps
1. State the exact operation and invariant required by the output; ignore implementation-specific buckets, helper lists, or sort calls.
2. Classify the dependency: static sorted order, dynamic extremum, top-K monotone frontier, extrema or interval overlap, bounded value frequencies, aggregate formula, FIFO consumption, or direct index mapping.
3. Eliminate work that does not affect the result: repeated sorting, full Cartesian products, numeric-domain scans, redundant sets, temporary slices, unused storage, and repeated aggregate recomputation.
4. For repeated extremal updates, use a heap for extraction and reinsertion; use a sorted list with binary search only when operation counts are modest and insertion shifts are acceptable.
5. For top-K sums over sorted arrays, initialize the best index state, expand neighboring states with a heap, track visited states, and stop after K outputs.
6. For existence or counting conditions over intervals, replace enumeration with max/min boundary comparisons and closed-form differences.
7. For small bounded integer values, count frequencies and reconstruct order or compute counts directly instead of comparison-sorting.
8. For modular or aggregate objectives, maintain the total and the fewest necessary exceptional statistics in one pass.

## Complexity
- Time: (pattern dependent)
- Space: Prefer O(1) auxiliary space for extrema, aggregation, interval tests, and streaming, O(n) for one-time sorting or direct mappings, O(V) for frequency tables, O(n) for heaps or queues, and O(K) or O(K log-frontier) for top-K traversal

## Pitfalls
- Replacing a dynamic ordering problem with a sorted list without accounting for O(n) insertion shifts.
- Assuming a one-time sort plus fold is valid without proving that the greedy processing order reproduces the original state transitions.
- Using strict inequality when equality is also a valid action or threshold case.
- Generating duplicate heap states without a visited set.
- Stopping top-K frontier expansion without proving that all unexpanded neighbors are no better than the heap maximum.
- Using interval overlap logic without checking whether endpoints are open or closed and whether an integer witness is required.
- Applying counting sort when the value range is large or sparse enough to exceed comparison-sort cost.
- Sorting an entire array when only extrema, a few ranks, or a threshold-filtered subset are required.

## When not to use
- The required output genuinely needs the complete ordering or every Cartesian combination.
- Updates are not monotone and the proposed heap or frontier-neighbor expansion cannot prove completeness.
- The result depends on element identities, stable ordering, or full pair relationships rather than the stated aggregates.
- The value domain is too large or sparse for frequency counting.
- A sorted-list approach is used with many updates and a heap or balanced ordered structure is available.
- The greedy fold lacks a proof that processing sorted values preserves the original simulation result.

## Minimal example
Before:
```py
from itertools import combinations
intervals = [(1, 3), (2, 5), (4, 7), (6, 8), (7, 9)]
best = max((c for r in range(len(intervals) + 1) for c in combinations(intervals, r) if all(a[1] <= b[0] for a, b in zip(sorted(c), sorted(c)[1:]))), key=len)
print(best)
```
After:
```py
intervals = [(1, 3), (2, 5), (4, 7), (6, 8), (7, 9)]
chosen, end = [], float('-inf')
for start, finish in sorted(intervals, key=lambda x: x[1]):
    if start >= end: chosen.append((start, finish)); end = finish
print(chosen)
```
