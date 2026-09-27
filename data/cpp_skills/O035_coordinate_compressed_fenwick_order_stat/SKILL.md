---
skill_id: O035
type: operator
language: cpp
family: dp
name: Coordinate Compressed Fenwick Order Statistics
description: Replace repeated scans, heavy ordered containers, or specialized selection structures with offline coordinate
  compression and flat Fenwick trees. Represent values, ranks, prefix balances, or derived permutations as 1-based indices,
  then answer prefix counts, weighted sums, inversion contributions, k-th queries, and dynamic median costs in O(log n) per
  operation. When feasibility is monotone in a threshold, combine
tags:
- coordinate-compression
- fenwick-tree
- order-statistics
- prefix-sums
- counting
- offline-processing
- online-queries
- binary-search-on-answer
- inversion-counting
- dynamic-median
triggers:
- A loop repeatedly scans prior elements to count values below, above, or within a threshold.
- Queries require prefix frequencies, weighted prefix sums, inversion counts, rank counts, or DP transitions over ordered
  values.
- Values are large, negative, sparse, or otherwise unsuitable for direct indexing.
- A dynamic multiset needs median or k-th selection together with sums or absolute-deviation costs.
- A monotone answer predicate asks whether a prior value exists in a threshold-dependent range.
- A permutation is formed by sorting on multiple keys and then requires repeated prior-rank counting.
- PBDS, map, multiset, or pointer-heavy trees are used only for prefix counts or sums.
- A separate special case handles the empty prefix or base prefix condition.
---

## When to use
- A loop repeatedly scans prior elements to count values below, above, or within a threshold.
- Queries require prefix frequencies, weighted prefix sums, inversion counts, rank counts, or DP transitions over ordered values.
- Values are large, negative, sparse, or otherwise unsuitable for direct indexing.
- A dynamic multiset needs median or k-th selection together with sums or absolute-deviation costs.
- A monotone answer predicate asks whether a prior value exists in a threshold-dependent range.
- A permutation is formed by sorting on multiple keys and then requires repeated prior-rank counting.
- PBDS, map, multiset, or pointer-heavy trees are used only for prefix counts or sums.
- A separate special case handles the empty prefix or base prefix condition.

## Steps
1. Identify the exact aggregate needed from processed state: frequency, prefix count, weighted sum, best DP value, inversion contribution, or existence.
2. Collect all relevant values before processing when offline compression is allowed; sort and unique them.
3. Map each value to a 1-based compressed rank. Preserve duplicate identity with a secondary key such as original position when order must be deterministic.
4. For frequency or weighted-sum queries, maintain one Fenwick tree for counts and, when needed, a second Fenwick tree for value sums.
5. For each item, query the required prefix or range using `query(r)` or `query(right) - query(left - 1)`, then publish its contribution with `add(rank, delta)`.
6. For inversion or permutation counting, derive the permutation through sorting, sweep it once, query prior ranks, and update the current rank.
7. For dynamic median queries, find the smallest rank whose cumulative count reaches the target order statistic, then combine left/right counts and sums around that rank.
8. For transformed prefix problems, build `pref[0] = 0`, include the empty prefix in compression, query prior balances with the correct inclusive or exclusive bound, then update.

## Complexity
- Time: Typically O(n log n) offline, including sorting and O(log n) Fenwick operations per element. Dynamic insertion/report workloads are O(q log q) after compression. Binary search on answer adds a factor of O(log U), giving O(n log n log U)
- Space: O(n) for compressed values, Fenwick arrays, prefix data, and optional auxiliary result arrays. Two Fenwick trees use O(n) total space.

## Pitfalls
- Do not use a Fenwick tree when a scalar running count or prefix sum answers the query; it can regress from O(n) to O(n log n).
- Include the empty prefix when counting subarrays; omitting it often forces fragile special-case branches.
- Check strict versus non-strict inequalities carefully: query rank(value - 1) for < and rank(value) for <=.
- Update only after querying when the current item must not count as a prior item.
- Use the actual compressed size in Fenwick loops, not the original n or a hardcoded maximum.
- Preserve duplicate ordering when converting pairs into ranks or permutations; compressing values alone may merge distinct elements incorrectly.
- Binary-search the answer only when the feasibility predicate is monotone, and search distinct input values when the answer can only change there.
- Do not replace a specialized heap with Fenwick trees merely for abstraction; rank-search and aggregate queries must justify the extra logarithmic work.

## When not to use
- The input key domain is small, dense, and direct frequency arrays are simpler and faster.
- The data is genuinely online and future keys cannot be collected for compression; use a balanced BST or dynamic coordinate structure.
- The input is already sorted and a two-pointer or linear prefix scan solves the task.
- The operation requires arbitrary interval updates or range minima/maxima rather than additive prefix aggregates; use a segment tree or another appropriate structure.
- The number of operations is small enough that sorting or direct scans are comfortably within limits.

## Minimal example
Before:
```cpp
// O035 focus: coordinate
vector<vector<int>> dp(n + 1, vector<int>(W + 1, 0));
for (int i = 1; i <= n; ++i)
  for (int w = 0; w <= W; ++w)
    dp[i][w] = max(dp[i - 1][w], w >= wt[i] ? dp[i - 1][w - wt[i]] + val[i] : 0);
```
After:
```cpp
// optimized for coordinate
vector<int> dp(W + 1, 0);
for (int i = 1; i <= n; ++i)
  for (int w = W; w >= wt[i]; --w)
    dp[w] = max(dp[w], dp[w - wt[i]] + val[i]);
```
