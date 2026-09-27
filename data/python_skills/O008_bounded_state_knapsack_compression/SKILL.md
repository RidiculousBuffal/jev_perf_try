---
skill_id: O008
type: operator
language: python
family: state_compression
name: Bounded State Knapsack Compression
description: Reusable optimization pattern distilled from weighted traces.
tags:
- dynamic_programming
- 0_1_knapsack
- subset_sum
- value_based_dp
- state_compression
- dimension_reduction
- bounded_state_space
- pseudo_polynomial
- tree_dp
- memory_optimization
triggers:
- A brute-force loop enumerates combinations of bucket counts, subsets, or group selections.
- A DP tracks two quantities whose acceptance condition is only a linear relation between them.
- A subset-average or ratio condition can be rewritten as a zero-sum or zero-balance condition.
- A DP dimension is sized from a target parameter or raw total even though item values impose a smaller bound.
- A full 2D or 3D DP transition depends only on the previous layer.
- A 0/1 knapsack recurrence is implemented with row copies, deep copies, circular shifts, or large temporary arrays.
- A Python DP uses sets or dictionaries for dense integer sums within a small known numeric range.
- Weights are close to a common base, so total weight decomposes into chosen_count times base plus a small offset.
---

## When to use
- A brute-force loop enumerates combinations of bucket counts, subsets, or group selections.
- A DP tracks two quantities whose acceptance condition is only a linear relation between them.
- A subset-average or ratio condition can be rewritten as a zero-sum or zero-balance condition.
- A DP dimension is sized from a target parameter or raw total even though item values impose a smaller bound.
- A full 2D or 3D DP transition depends only on the previous layer.
- A 0/1 knapsack recurrence is implemented with row copies, deep copies, circular shifts, or large temporary arrays.
- A Python DP uses sets or dictionaries for dense integer sums within a small known numeric range.
- Weights are close to a common base, so total weight decomposes into chosen_count times base plus a small offset.

## Steps
1. Write the exact state meaning and identify which quantities affect future transitions or final acceptance.
2. Algebraically remove redundant dimensions. For a condition such as sum_a * target_b == sum_b * target_a, track balance = sum_a * target_b - sum_b * target_a. For an average condition, track sum(value - target).
3. For tightly clustered weights, choose a base weight and represent total weight as chosen_count * base + offset_sum.
4. Choose the DP objective appropriate to the query: minimum cost for each state, maximum value for each state, count of ways, or feasibility.
5. Derive the tightest safe state bound from item limits, capacity, transformed-value range, or the current reachable prefix. Do not size the table from an unrelated target or oversized raw total.
6. Use an offset array for signed states and a sentinel suited to the constraint, such as capacity plus one for infeasible minimum-cost states.
7. For ordinary 0/1 transitions, update a one-dimensional array in descending index order. For signed transitions, use direction-specific iteration or a copied layer so the current item cannot be reused.
8. Compress layers whenever transitions depend only on the previous layer. Keep a full prefix dimension only when reconstruction or nonlocal dependencies require it.

## Complexity
- Time: (pattern dependent)
- Space: Usually O(R) with rolling or in-place one-dimensional DP, O(K * R) when count must be retained, and O(n * K * R) only when full history or reconstruction is required. Tree merges generally use O(C) temporary DP space plus O(n) adjacency

## Pitfalls
- Using an algebraic compression without proving that the compressed invariant is sufficient for both transitions and the final condition.
- Sizing the DP by a target average, raw total, or n-dependent heuristic instead of the true reachable bound.
- Updating a 0/1 DP in ascending order and accidentally allowing an item to be selected multiple times.
- Using an in-place direction that is unsafe when transformed contributions can be negative.
- Keeping redundant prefix, chosen-count, or resource dimensions after they have become derivable from other state variables.
- Replacing a multidimensional state with a scalar balance when the objective still depends on the original components.
- Using a fixed bound inferred from one implementation without verifying it against all valid input constraints.
- Treating a Python set as automatically efficient; dense bounded sums are usually faster and more predictable in arrays.

## When not to use
- The numeric capacity, value sum, or transformed balance range is too large for pseudo-polynomial memory or time.
- Input numbers are large in binary representation and no small numeric bound exists.
- The compressed invariant loses information needed by transitions, optimization, reconstruction, or tie-breaking.
- The problem requires arbitrary item multiplicities and the chosen 0/1 update order is not adapted to bounded or unbounded knapsack semantics.
- The state space remains sparse and huge, making hash-based sparse DP, meet-in-the-middle, branch-and-bound, or generating-function methods more appropriate.
- The main constraints are lexicographic, nonlinear, or nonadditive and cannot be represented by a bounded additive state.

## Minimal example
Before:
```py
from itertools import combinations

def count_target_average(weights, target):
    return sum(1 for r in range(1, len(weights) + 1)
               for subset in combinations(weights, r)
               if sum(subset) == target * r)
```
After:
```py
def count_target_average(weights, target):
    dp = {0: 1}  # balance: sum(weight - target)
    for weight in weights:
        delta = weight - target
        dp.update({b + delta: dp.get(b + delta, 0) + count for b, count in list(dp.items())})
    return dp.get(0, 0) - 1  # exclude the empty subset
```
