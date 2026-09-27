---
skill_id: O017
type: operator
language: cpp
family: dp
name: Precompute Cumulative State and Sweep Monotonically
description: Convert repeated range walks, branch-heavy local formulas, redundant feasibility scans, and overfull DP transitions
  into reusable cumulative representations. Build prefix, suffix, residue-class, path-distance, or transformed best-prefix/best-suffix
  tables; then answer each query or candidate split with O(1) arithmetic or a single monotone sweep. When a special cell or
  constrained subproblem is the only semantically
tags:
- prefix-sums
- suffix-sums
- offline-preprocessing
- monotone-sweep
- two-pointers
- binary-search
- dynamic-programming
- state-pruning
- residue-class-decomposition
- path-cost
triggers:
- A query repeatedly walks the same additive path, interval, chain, or modulo-D sequence.
- A binary-search predicate contains a loop over a contiguous array segment.
- Adjacent binary-search probes revisit heavily overlapping ranges.
- A nested loop contains an index or pointer that only moves forward or backward.
- A per-position formula has many cases but only changes a constant number of adjacent edges or segments.
- The objective is evaluated over every split, pivot, or boundary using left and right aggregates.
- A sorted prefix or suffix must repeatedly maintain the best, largest-n, or smallest-n subset sum.
- A recurrence later becomes a prefix maximum, suffix maximum, or range-sum query.
---

## When to use
- A query repeatedly walks the same additive path, interval, chain, or modulo-D sequence.
- A binary-search predicate contains a loop over a contiguous array segment.
- Adjacent binary-search probes revisit heavily overlapping ranges.
- A nested loop contains an index or pointer that only moves forward or backward.
- A per-position formula has many cases but only changes a constant number of adjacent edges or segments.
- The objective is evaluated over every split, pivot, or boundary using left and right aggregates.
- A sorted prefix or suffix must repeatedly maintain the best, largest-n, or smallest-n subset sum.
- A recurrence later becomes a prefix maximum, suffix maximum, or range-sum query.

## Steps
1. Normalize indexing early; prefer consistent 0-based or sentinel-indexed arrays so residue, quotient, boundary, and prefix formulas are direct.
2. Identify the additive quantity: edge cost, element sum, count, rectangle weight, reward, or transformed feasibility contribution.
3. Build the smallest useful cumulative representation: one prefix array, prefix and suffix arrays, a flat residue-class table, modulo-class vectors, or separate 2D prefix planes.
4. For path or chain queries, accumulate each edge once and answer [L,R] with prefix[R] - prefix[L].
5. For split or pivot objectives, express the candidate from left and right aggregates, such as abs(total - 2 * prefix) or left_cost + bridge_cost + right_cost.
6. For binary-search feasibility, replace range loops with prefix-sum subtraction and then exploit monotonicity with a linear sweep or amortized pointer.
7. For two ordered prefixes under a budget, move the right pointer only in one direction while the left pointer advances.
8. For top-n or bottom-n prefix/suffix choices, maintain a heap and rolling sum; complete both directional passes before combining split states.

## Complexity
- Time: Usually O(N + Q) after linear preprocessing for additive range or path queries; O(N log N) when sorting, heaps, or binary search are required; O(N^3) may remain appropriate for dense interval DP when only constant factors are improved
- Space: Typically O(N) for prefix/suffix arrays, path distances, heap-DP states, or transformed values; O(N + D) for residue-class organization; O(HW) for grid coordinates and 2D prefixes; potentially O(K^4) for memoized rectangle states. Reduce

## Pitfalls
- Calling a solution 'fast' when it only changes layout or helper functions while preserving the same asymptotic work.
- Using modulo-class vectors without correctly mapping endpoints to the same class and local prefix positions.
- Mixing 0-based labels with 1-based quotient or residue formulas.
- Relying on zero-initialized global sentinels or reading a[i+1] past the logical end.
- Allocating a fixed prefix table smaller than the actual numeric domain, causing silent out-of-bounds corruption.
- Memoizing every rectangle or scanning every cell pivot when only special-cell-containing states matter.
- Keeping a tiny third dimension in a hot prefix table when separate arrays would eliminate branches and improve locality.
- Using VLAs or oversized stack arrays; prefer vector or appropriately sized static storage.

## When not to use
- The data is dynamic and updates invalidate cumulative tables unless a suitable Fenwick tree, segment tree, or rebuild strategy is available.
- Queries are not additive, do not share reusable structure, or depend on order-sensitive interactions that prefix subtraction cannot represent.
- The predicate is not monotone, so a two-pointer sweep or binary search is unjustified.
- The input domain is too large for the proposed full numeric-domain table; use coordinate compression or sparse structures instead.
- The required DP transitions genuinely depend on every pivot or cell and cannot be charged through a valid prefix-sum decomposition.
- A representation split or vector-of-vectors adds indirection without removing work; a flat contiguous array may be faster despite equivalent asymptotics.

## Minimal example
Before:
```cpp
// O017 focus: precompute
vector<vector<int>> dp(n + 1, vector<int>(W + 1, 0));
for (int i = 1; i <= n; ++i)
  for (int w = 0; w <= W; ++w)
    dp[i][w] = max(dp[i - 1][w], w >= wt[i] ? dp[i - 1][w - wt[i]] + val[i] : 0);
```
After:
```cpp
// optimized for precompute
vector<int> dp(W + 1, 0);
for (int i = 1; i <= n; ++i)
  for (int w = W; w >= wt[i]; --w)
    dp[w] = max(dp[w], dp[w - wt[i]] + val[i]);
```
