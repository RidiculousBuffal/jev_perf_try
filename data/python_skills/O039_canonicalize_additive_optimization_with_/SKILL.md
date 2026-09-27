---
skill_id: O039
type: operator
language: python
family: dp
name: Canonicalize Additive Optimization with Unbounded DP and Structural Reduction
description: Recognize minimum-cost or counting problems over additive integer totals, especially when moves or item values
  can be reused. Replace recursive branching, repeated subtraction, explicit multiple-count enumeration, and opaque representation
  tricks with a direct recurrence over reachable sums. Generate usable denominations once, use one-dimensional unbounded-knapsack
  DP when the target is moderate, compress
tags:
- dynamic_programming
- unbounded_knapsack
- coin_change
- minimum_cost
- counting_combinations
- shortest_path_on_sums
- state_compression
- dimension_reduction
- precomputation
- greedy_invariant
triggers:
- A recursive minimization branches over alternative additive moves and revisits the same remaining totals.
- A loop repeatedly subtracts one item at a time while minimizing or counting the result.
- Allowed values form a reusable denomination set, including generated values such as powers or squares.
- The objective is minimum number of uniform-cost additions or the number of unordered combinations.
- A two-dimensional DP row depends only on the previous row and repeated use of the current item.
- An inner loop enumerates all multiples of one denomination.
- A nested enumeration checks whether several fixed denominations sum to a target.
- One variable is uniquely determined by the remaining target after other choices are fixed.
---

## When to use
- A recursive minimization branches over alternative additive moves and revisits the same remaining totals.
- A loop repeatedly subtracts one item at a time while minimizing or counting the result.
- Allowed values form a reusable denomination set, including generated values such as powers or squares.
- The objective is minimum number of uniform-cost additions or the number of unordered combinations.
- A two-dimensional DP row depends only on the previous row and repeated use of the current item.
- An inner loop enumerates all multiples of one denomination.
- A nested enumeration checks whether several fixed denominations sum to a target.
- One variable is uniquely determined by the remaining target after other choices are fixed.

## Steps
1. State the optimization precisely: define the target range, reusable values, whether order matters, and whether the objective is minimization or counting.
2. Derive the implicit item or move set from the original recursion or simulation; include a unit value when the base case permits arbitrary unit additions.
3. Generate each usable denomination once, stop when it exceeds the relevant maximum target, then deduplicate and sort it.
4. For minimum cost, define dp[0] = 0 and all other states as infinity. Use dp[s] = min(dp[s], dp[s - c] + 1) for every denomination c and s >= c.
5. Prefer a one-dimensional array for unbounded reuse, iterating sums increasingly when processing each denomination.
6. For counting unordered combinations, initialize dp[0] = 1 and process each denomination outermost, then iterate sums increasingly with dp[s] += dp[s - c].
7. Replace explicit multiple-count loops with the standard unbounded recurrence; this removes a redundant count dimension.
8. If only one variable remains in a target equality, compute the remainder directly, reject negative or non-divisible remainders, and enforce its bound.

## Complexity
- Time: For target N and M usable denominations, standard minimum-cost or counting DP takes O(NM) time and O(N) space. With generated geometric denominations, M is typically O(log N), giving O(N log N) time, often near-linear in practice. Offline
- Space: (pattern dependent)

## Pitfalls
- Assuming a greedy decomposition is optimal for arbitrary denominations; canonical-looking values do not guarantee the exchange property.
- Treating a specialized digit-sum identity as a general solution to additive optimization.
- Using a two-dimensional DP or explicit multiple-count expansion when a one-dimensional unbounded recurrence is sufficient.
- Iterating every denomination at every state when only a proven small predecessor set is needed.
- Enumerating a third count after the remaining target already determines it algebraically.
- Confusing combinations with permutations; loop order changes counting semantics.
- Iterating sums in the wrong direction, which can accidentally model 0/1 use instead of unlimited reuse or count order-sensitive sequences.
- Failing to deduplicate overlapping generated denominations, such as a shared unit value.

## When not to use
- Do not use unbounded coin-change DP when item supplies are bounded, item costs differ, ordering matters, or additional state dimensions affect feasibility.
- Do not replace a correct specialized O(N) or O(1)-space method with DP when memory limits are tight and the specialization is simple and provably correct.
- Do not use greedy decomposition without proving canonicality, an exchange argument, or an equivalent structural theorem.
- Do not use split enumeration when the target is too large for a linear scan and no faster convolution, number-theoretic, or optimization technique applies.
- Do not compress DP dimensions if future transitions require discarded rows, reconstruction, order information, or item-specific constraints.
- Do not apply algebraic elimination when the remainder can have multiple valid counts or when bounds, parity, or modular constraints are not fully checked.

## Minimal example
Before:
```py
# O039 focus: canonicalize
for i in range(n):
    dp[i] = max(dp[j] + 1 for j in range(max(0, i-w), i))
```
After:
```py
# optimized for canonicalize
for i in range(n):
    dp[i] = seg.query(lo(i), hi(i)) + 1
    seg.update(pos(i), dp[i])
```
