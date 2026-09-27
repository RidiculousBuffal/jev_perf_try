---
skill_id: O013
type: operator
language: cpp
family: dp
name: Compress Invariants and Specialize the Search
description: Recognize when a seemingly general optimization problem has a much smaller sufficient state or candidate set.
  Replace explicit geometric regions, repeated validation, generic containers, and heuristic iteration with boundary extrema,
  canonical signatures, closed-form candidates, exact convex search, or pruned enumeration. Preserve the unavoidable search
  when necessary, but make each transition and leaf evaluation
tags:
- computational-geometry
- optimization
- state-compression
- candidate-reduction
- branch-and-bound
- convex-search
- coordinate-compression
- sorting
- prefix-sums
- canonicalization
triggers:
- The result depends only on cumulative extrema, such as the intersection of axis-aligned half-planes.
- A brute-force loop scans a monotone variable with a piecewise-linear or separable objective.
- A fixed small domain makes exhaustive candidate enumeration viable, but repeated formulas or validations dominate.
- The objective is an L1 or Manhattan expression, suggesting medians or a small Cartesian product of median coordinates.
- The objective is a minimax over distances or another convex function, while the current implementation uses cooling, farthest-point
  descent, or a magic iteration cap.
- The search state is a subset, matching, or permutation and the leaf score repeatedly compares equivalent objects pairwise.
- A relation such as parallelism, equality of slopes, or equal ratios is checked through repeated cross products instead of
  canonical keys.
- A hot loop repeatedly calls sqrt, trigonometric functions, long-double geometry, or creates temporary point objects.
---

## When to use
- The result depends only on cumulative extrema, such as the intersection of axis-aligned half-planes.
- A brute-force loop scans a monotone variable with a piecewise-linear or separable objective.
- A fixed small domain makes exhaustive candidate enumeration viable, but repeated formulas or validations dominate.
- The objective is an L1 or Manhattan expression, suggesting medians or a small Cartesian product of median coordinates.
- The objective is a minimax over distances or another convex function, while the current implementation uses cooling, farthest-point descent, or a magic iteration cap.
- The search state is a subset, matching, or permutation and the leaf score repeatedly compares equivalent objects pairwise.
- A relation such as parallelism, equality of slopes, or equal ratios is checked through repeated cross products instead of canonical keys.
- A hot loop repeatedly calls sqrt, trigonometric functions, long-double geometry, or creates temporary point objects.

## Steps
1. Write the objective and constraints algebraically before optimizing the implementation; determine which input information can affect the final answer.
2. Compress the state to sufficient statistics: four rectangle bounds, scalar extrema, medians, counts, pointer positions, or a compact event frontier.
3. Separate structural special cases first, such as equal coordinates, empty intersections, zero-height observations, or impossible construction bounds.
4. For convex or unimodal continuous objectives, replace heuristic walks with a pure evaluator and nested ternary or binary search over a valid bounded domain.
5. If exhaustive enumeration is unavoidable, choose a canonical traversal to avoid duplicates, maintain incremental state, and prune using remaining capacity and the current best objective.
6. At expensive leaves, replace pairwise relation checks with canonical normalization and frequency counting; use gcd-reduced direction or ratio signatures where appropriate.
7. Precompute invariant values once when they are reused substantially, such as perfect squares, distances, overlap compatibility, or per-candidate expressions. Avoid tables when they merely add memory traffic.
8. Use global best bounds immediately in monotone scans and stop after the first feasible candidate when later candidates cannot improve the objective.

## Complexity
- Time: Usually reduces a redundant or over-modeled solution to O(n) or O(n log n) time and O(1) or O(n) auxiliary space. Closed-form reductions can reach O(1); precomputed pair checks typically become O(n^2*d) or O(n^2*d + n^2 log S)
- Space: Prefer O(1) working state for cumulative-bound problems, O(n) for point storage, DFS state, events, or preprocessing, and O(n^2) only when query volume or reusable tables justify it. Avoid multidimensional precomputation unless reuse

## Pitfalls
- Claiming an asymptotic improvement when the change only reduces constants or rewrites the same search space.
- Using exponential subset DFS on inputs where compressed-grid or prefix-sum enumeration has the safer worst-case bound.
- Precomputing a large multidimensional table that is read only once, thereby replacing arithmetic with memory bandwidth.
- Applying a fast specialized algorithm when the original problem lacks the ordering, dominance, or compatibility constraint that justifies it.
- Relying on heuristic convergence, arbitrary iteration caps, or magic cooling factors for an objective with an exact convex formulation.
- Using a positive observation or sentinel without handling the case where no such observation exists.
- Performing square checks with repeated sqrt, linear scans, or floating-point equality instead of integer squared-distance membership.
- Computing cross products, areas, or products in int before assigning to long long.

## When not to use
- Do not replace a proven linear scan with sorting, segment trees, or coordinate compression when the objective has no ordering or range constraint.
- Do not use branch-and-bound DFS when n is too large, pruning is weak, or a polynomial compressed formulation exists with a reliable worst-case bound.
- Do not precompute values that are used once or whose table causes more memory traffic than the original arithmetic.
- Do not use ternary search unless the evaluator is genuinely unimodal or convex on the searched interval and the domain bounds are valid.
- Do not discard explicit geometric state when constraints are not axis-aligned or the feasible region is not closed under four extrema.
- Do not canonicalize directions with floating-point slopes; use integer normalization only when the relation is exactly representable and gcd handling covers zero components.

## Minimal example
Before:
```cpp
// O013 focus: compress
vector<vector<int>> dp(n + 1, vector<int>(W + 1, 0));
for (int i = 1; i <= n; ++i)
  for (int w = 0; w <= W; ++w)
    dp[i][w] = max(dp[i - 1][w], w >= wt[i] ? dp[i - 1][w - wt[i]] + val[i] : 0);
```
After:
```cpp
// optimized for compress
vector<int> dp(W + 1, 0);
for (int i = 1; i <= n; ++i)
  for (int w = W; w >= wt[i]; --w)
    dp[w] = max(dp[w], dp[w - wt[i]] + val[i]);
```
