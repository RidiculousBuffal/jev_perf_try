---
skill_id: O015
type: operator
language: python
family: dp
name: Interval Aggregation, Sweep, and Batched DP Optimization
description: Replace explicit interval-domain simulation, repeated slot assignment, redundant range tables, and interpreter-heavy
  transitions with the smallest representation matching the required aggregate. Use min/max aggregation for a common intersection,
  difference arrays or event sweeps for coverage and concurrency, per-channel sweeps when categories must be merged independently,
  doubled coordinates for boundary-sensitive
tags:
- intervals
- difference-array
- imos
- prefix-sum
- sweep-line
- interval-intersection
- interval-overlap
- maximum-concurrency
- interval-dp
- range-sum
triggers:
- The code paints every coordinate in every interval or stores a dense category-by-time matrix.
- The output is a scalar aggregate such as union size, exact coverage count, maximum overlap, or number of points covered
  by every interval.
- The code computes max(left endpoints) and min(right endpoints), then scans the whole domain.
- Intervals are grouped by channel or category and overlapping intervals within one group should count once.
- Endpoint behavior differs for touching intervals, or continuous-looking boundaries are encoded with fractional sentinels.
- An interval DP has a split-point minimum and an additive range cost, with all equal-length states independent.
- A full two-dimensional range-sum table exists only to answer interval sums.
- A DP state repeatedly propagates contributions across future ranges or repeatedly queries contiguous predecessor ranges.
---

## When to use
- The code paints every coordinate in every interval or stores a dense category-by-time matrix.
- The output is a scalar aggregate such as union size, exact coverage count, maximum overlap, or number of points covered by every interval.
- The code computes max(left endpoints) and min(right endpoints), then scans the whole domain.
- Intervals are grouped by channel or category and overlapping intervals within one group should count once.
- Endpoint behavior differs for touching intervals, or continuous-looking boundaries are encoded with fractional sentinels.
- An interval DP has a split-point minimum and an additive range cost, with all equal-length states independent.
- A full two-dimensional range-sum table exists only to answer interval sums.
- A DP state repeatedly propagates contributions across future ranges or repeatedly queries contiguous predecessor ranges.

## Steps
1. First identify the exact semantic aggregate: sum with multiplicity, union, exact coverage, coverage threshold, common intersection, maximum concurrency, or category-wise presence.
2. Choose the lowest-dimensional representation that preserves that aggregate.
3. For a common closed integer intersection, stream intervals while maintaining max_left and min_right; return max(min_right - max_left + 1, 0).
4. For bounded-coordinate coverage, represent each inclusive update [l, r] with diff[l - 1] += 1 and diff[r] -= 1, prefix-scan once, and count positions satisfying the required coverage predicate.
5. For union coverage, count positive prefix coverage; for exact or threshold coverage, test equality or the threshold directly.
6. For maximum overlap, emit start and end events, prefix-sum them, and take the maximum active count instead of assigning intervals to explicit lanes.
7. When categories may overlap internally but contribute only once, maintain one difference timeline per category, clamp each category's active count to presence, then aggregate across categories.
8. When boundary rules depend on category equality or touching endpoints, encode them explicitly in event placement; use doubled coordinates when discrete inclusivity or adjacency needs unambiguous ordering.

## Complexity
- Time: (pattern dependent)
- Space: (pattern dependent)

## Pitfalls
- Replacing an interval-length sum with union or coverage logic without confirming the required semantics.
- Using a difference array when only the common intersection is needed, adding unnecessary time and memory.
- Using the intersection formula for a task requiring union size, exact coverage, or per-position results.
- Off-by-one errors for inclusive intervals, especially with updates at r versus r + 1.
- Incorrectly merging touching intervals across different categories or failing to merge them within the same category.
- Relying on floating-point sentinels such as start - 0.5 instead of defining discrete event ordering explicitly.
- Assuming a fixed maximum number of lanes, channels, or resources.
- Allocating a dense category-by-time matrix when intervals are sparse or coordinates are large.

## When not to use
- Do not collapse to min/max intersection unless every valid point must belong to every interval.
- Do not use a difference array when coordinates are unbounded and no compression or sparse event representation is available.
- Do not use dense per-category timelines when the category count or time universe makes C*T infeasible.
- Do not replace explicit scheduling with maximum-overlap counting if the actual output requires a valid assignment, identities, ordering, or reconstruction.
- Do not apply same-category endpoint merging unless the problem's boundary semantics explicitly allow it.
- Do not use vectorized interval DP when n is too large for O(n^2) memory or when a valid monotonicity optimization such as Knuth or divide-and-conquer DP applies.

## Minimal example
Before:
```py
intervals = [(3, 40), (10, 25), (20, 60), (35, 50)]
q = 2
coverage = [0] * 101
for left, right in intervals:
    for position in range(left, right + 1): coverage[position] += 1
answer = sum(count == q for count in coverage[1:])
```
After:
```py
intervals = [(3, 40), (10, 25), (20, 60), (35, 50)]
q = 2
diff = [0] * 102
for left, right in intervals: diff[left - 1] += 1; diff[right] -= 1
coverage = answer = 0
for position in range(1, 101): coverage += diff[position - 1]; answer += coverage == q
```
