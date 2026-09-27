---
skill_id: O030
type: operator
language: cpp
family: dp
name: Ordered Transformed DP with Monotone Range Min Structures
description: Reusable optimization pattern distilled from weighted traces.
tags:
- dynamic-programming
- dp-optimization
- sorted-coordinates
- offline-processing
- range-minimum-query
- fenwick-tree
- segment-tree
- prefix-minimum
- suffix-minimum
- monotone-boundary
triggers:
- The recurrence has the form dp[i] = min_j(dp[j] + cost(j, i)) over sorted positions.
- A predecessor remains valid over a contiguous future interval or under a monotone distance threshold.
- The transition contains max, abs, or piecewise-linear terms that can be split into a small number of affine cases.
- A binary-search boundary, two-pointer boundary, or doubled-coordinate threshold moves monotonically with i.
- The implementation scans all predecessors, uses a size-based quadratic fallback, or has ad hoc branch-specific queue logic.
- A single rolling minimum or scalar summary is used even though different predecessor ranges or transformed cost families
  matter.
- A segment tree is used only for prefix or suffix minima, or a full-tree traversal is needed merely to extract the final
  minimum.
- An ordered set or map maintains a dominated skyline for repeated prefix-maximum or prefix-minimum queries.
---

## When to use
- The recurrence has the form dp[i] = min_j(dp[j] + cost(j, i)) over sorted positions.
- A predecessor remains valid over a contiguous future interval or under a monotone distance threshold.
- The transition contains max, abs, or piecewise-linear terms that can be split into a small number of affine cases.
- A binary-search boundary, two-pointer boundary, or doubled-coordinate threshold moves monotonically with i.
- The implementation scans all predecessors, uses a size-based quadratic fallback, or has ad hoc branch-specific queue logic.
- A single rolling minimum or scalar summary is used even though different predecessor ranges or transformed cost families matter.
- A segment tree is used only for prefix or suffix minima, or a full-tree traversal is needed merely to extract the final minimum.
- An ordered set or map maintains a dominated skyline for repeated prefix-maximum or prefix-minimum queries.

## Steps
1. Sort coordinates or verify that the input order already provides the required monotone state order.
2. Write the exact DP recurrence and identify every distinct predecessor class; do not collapse classes into one scalar until equivalence is proved.
3. Split piecewise costs into cases. For absolute distance, use dp[j] - pos[j] on the left and dp[j] + pos[j] on the right; for thresholded max costs, find the monotone cutoff.
4. Separate each transition into a simple function of the destination i plus a transformed value depending only on predecessor j.
5. Find the validity boundary with upper_bound, binary search, or a monotone pointer. Use two pointers when the boundary advances only forward.
6. Choose the lightest structure matching the query geometry: a monotone stack for one-directional frontier closure, a Fenwick tree for prefix/suffix minima or maxima, and a segment tree for arbitrary dynamic index ranges or multiple transformed families.
7. For suffix minima with a Fenwick tree, mirror indices or use reversed update/query directions; for prefix maxima/minima, use standard Fenwick traversal.
8. Initialize all structures explicitly to INF or the appropriate identity and seed only genuinely reachable base states.

## Complexity
- Time: Typically O((n + m) log n) after sorting or bucketing, with O(n + m) memory. Specialized monotone-stack or deque variants can reduce the post-sort sweep to O(n), yielding O(n log n) total when sorting dominates. A direct transformed-DP
- Space: O(n + m) using flat DP arrays, transformed-value arrays, event buckets, and one or two Fenwick trees or segment trees. Coordinate compression adds O(n) auxiliary storage.

## Pitfalls
- Using a single running minimum when the recurrence requires multiple transformed expressions or distinct dynamic index ranges; this can be fast but incorrect.
- Assuming a monotone pointer or stack is valid without proving sorted coordinates, one-directional reachability, and permanent candidate dominance.
- Applying Fenwick trees to arbitrary intervals or range updates when a segment tree or another structure is required.
- Forgetting that Fenwick min/max updates are generally one-way; they support point insertion or monotone improvement, not arbitrary deletion.
- Mixing inclusive and exclusive boundaries at the threshold split, especially around ceil(T/2), upper_bound results, and predecessor index offsets.
- Updating a structure with dp[i] before or after the wrong transition phase, accidentally allowing a state to transition to itself.
- Building an explicit graph and running Dijkstra when the state space is ordered and interval transitions can be processed offline.
- Using std::set for a prefix skyline when the actual operation is simply prefix maximum/minimum; node allocation, pointer chasing, and repeated searches are costly.

## When not to use
- The predecessor set is genuinely arbitrary and not ordered, interval-like, or decomposable into a small number of transformed minima.
- Queries require arbitrary deletions, non-monotone point changes, or complex range updates that a min/max Fenwick tree cannot represent.
- The recurrence has a proven valid O(n) monotone queue, stack, or two-pass envelope solution and no additional transition family is missing.
- The key domain is too sparse or dynamic for practical coordinate compression and the query structure needs order-statistics beyond prefix/suffix aggregates.
- The input is online and future sorting, bucketing, or offline event scheduling is unavailable.
- The number of states is small enough that a simple O(n^2) DP is clearer and comfortably within limits.

## Minimal example
Before:
```cpp
sort(x.begin(), x.end());
vector<long long> dp(n, INF); dp[0] = w[0];
for (int i = 1; i < n; ++i)
  for (int j = 0; j < i; ++j)
    dp[i] = min(dp[i], dp[j] + w[i] + abs(x[i] - x[j]));
```
After:
```cpp
sort(x.begin(), x.end());
vector<long long> dp(n); long long best = w[0] - x[0]; dp[0] = w[0];
for (int i = 1; i < n; ++i) {
  dp[i] = w[i] + x[i] + best;
  best = min(best, dp[i] - x[i]);
}
```
