---
skill_id: O031
type: operator
language: cpp
family: dp
name: Structure Aware Knapsack DP Compression
description: Replace generic, heuristic, or over-dimensional knapsack implementations with a DP whose state matches the true
  constraint structure. Tighten bounds from loose capacity or value domains to actual reachable limits; reparameterize weights
  around a common baseline when item weights differ by only a small bounded offset; eliminate redundant reachability arrays,
  count dimensions, greedy reconstruction, and repeated
tags:
- dynamic_programming
- 0_1_knapsack
- bounded_knapsack
- subset_sum
- state_compression
- bound_tightening
- weight_normalization
- value_based_dp
- prefix_suffix_dp
- performance_optimization
triggers:
- A generic capacity-based DP scans a large W although n or another structural bound is small.
- Item weights are all close to a common base or belong to a few adjacent weight classes.
- A DP tracks both count and sum while accepting only states satisfying sum = count * K or another affine relation.
- A boolean reachability array duplicates information already represented by a value or cost array.
- The hot loop checks reachability and capacity bounds for every transition.
- A full loop over DP states is followed by another full loop over all items for greedy reconstruction.
- Repeated temporary vectors, object copies, or layer allocations occur inside the item loop.
- A 1D subset-sum DP is followed by interval arithmetic to recover order, frontier, or distinguished-last-item semantics.
---

## When to use
- A generic capacity-based DP scans a large W although n or another structural bound is small.
- Item weights are all close to a common base or belong to a few adjacent weight classes.
- A DP tracks both count and sum while accepting only states satisfying sum = count * K or another affine relation.
- A boolean reachability array duplicates information already represented by a value or cost array.
- The hot loop checks reachability and capacity bounds for every transition.
- A full loop over DP states is followed by another full loop over all items for greedy reconstruction.
- Repeated temporary vectors, object copies, or layer allocations occur inside the item loop.
- A 1D subset-sum DP is followed by interval arithmetic to recover order, frontier, or distinguished-last-item semantics.

## Steps
1. Identify the exact optimization invariant: best value for a capacity, minimum weight for a value, count by chosen cardinality and sum, or a frontier/order-aware state.
2. Derive the smallest safe state bounds from constraints and input totals; clamp every transition and loop to those bounds.
3. If weights are of the form base plus a small offset, represent total weight as chosen_count * base + extra_offset and DP only over the bounded extra offset.
4. If a target condition is affine, such as sum = count * K, subtract K from every selected item and reduce the condition to a zero-sum subset problem.
5. Group items into a small number of weight classes when useful; sort each class by value and build prefix sums for O(1) top-k value queries.
6. Choose the simplest valid transition: reverse in-place iteration for 0/1 DP, or two explicit layers when dependencies or semantic clarity require them.
7. Encode reachability with an INF or negative-INF sentinel instead of maintaining a parallel boolean array, provided sentinel arithmetic is safe.
8. Move capacity checks into loop bounds and iterate only valid source ranges; avoid per-state bounds branches.

## Complexity
- Time: (pattern dependent)
- Space: Use O(B), O(V), or O(D) with rolling 1D DP whenever only the previous layer is needed. Use O(N*B) or O(N*D) for prefix/suffix, frontier, or explicit-layer semantics. Multidimensional structural DP may require O(N^2*D) or O(B^2), but

## Pitfalls
- Do not compress away a dimension that determines correctness, such as an item frontier, next blocking item, or distinguished final choice.
- Do not use a zero-initialized max DP to represent unreachable states when negative values or invalid transitions could create false solutions.
- Do not use a negative-INF sentinel without ensuring adding an item value cannot overflow or turn unreachable into reachable.
- Do not update 0/1 knapsack capacities in ascending order; this reuses an item multiple times.
- Do not infer a fixed bound from one implementation; derive it from formal constraints and validate every index.
- Do not subtract a baseline without preserving the chosen-item count when the baseline contribution depends on count.
- Do not replace an exact DP with ratio sorting or local swaps merely because the capacity is small.
- Do not assume a larger asymptotic DP is faster; some structural rewrites improve correctness rather than big-O complexity.

## When not to use
- Do not use normalized-offset DP when weight deviations are large or their range scales with W; ordinary capacity DP, value DP, or another formulation may be smaller.
- Do not use dense DP when both capacity and value domains are huge and sparse-state methods, meet-in-the-middle, min-cost flow, or approximation are more appropriate.
- Do not use two-buffer or full prefix/suffix tables when a correct 1D reverse DP already captures the complete invariant.
- Do not use binary splitting when multiplicities are tiny or a specialized monotone-queue bounded-knapsack transition is more suitable.
- Do not use demand-driven memoization when nearly all states are reachable; bottom-up iteration usually has better locality and lower overhead.
- Do not remove an explicit state dimension solely for speed unless the resulting invariant proves that all merged states are equivalent.

## Minimal example
Before:
```cpp
bool subset_sum(const vector<int>& a, int target) {
    vector<vector<char>> dp(a.size() + 1, vector<char>(target + 1));
    dp[0][0] = 1;
    for (size_t i = 0; i < a.size(); ++i)
        for (int s = 0; s <= target; ++s) dp[i + 1][s] = dp[i][s] || (s >= a[i] && dp[i][s - a[i]]);
    return dp[a.size()][target];
}
```
After:
```cpp
bool subset_sum(const vector<int>& a, int target) {
    vector<char> dp(target + 1); dp[0] = 1;
    for (int x : a)
        for (int s = target; s >= x; --s) dp[s] |= dp[s - x];
    return dp[target];
}
```
