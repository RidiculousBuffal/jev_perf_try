---
skill_id: O012
type: operator
language: python
family: dp
name: Collapse Structured Brute Force into Invariant, Geometric, or Bounded State Computation
description: Optimize small or repetitive brute-force programs by first identifying mathematical structure, reusable witnesses,
  monotonicity, symmetry, locality, and bounded state dimensions. Replace numerical search or simulation with closed forms
  when possible; otherwise hoist candidate-independent work, restrict candidates to structural boundaries, use prefix or compressed
  counting for geometric queries, convert recursive
tags:
- optimization
- algebraic-simplification
- closed-form
- invariant-hoisting
- geometry
- coordinate-compression
- prefix-sums
- dynamic-programming
- state-compression
- sparse-enumeration
triggers:
- A general numerical optimizer is applied to a low-dimensional smooth objective with symmetry or a fixed-sum constraint.
- A brute-force candidate loop repeatedly scans input to derive a value that is independent of the candidate or derivable
  from one fixed witness.
- A permutation or route enumeration uses absolute differences on a line and appears to cover an interval.
- A scan over cut positions has a convex, monotone, symmetric, or piecewise-linear objective whose optimum must lie near balanced
  divisions or structural boundaries.
- A simulator repeatedly decrements, trims, copies, or recursively splits arrays while producing an area, envelope, or aggregate
  profile.
- A nested loop repeatedly sorts overlapping subsets or slices and the result depends only on rectangle membership or range
  counts.
- A profile is constrained by local slope changes and has a small bounded height or capacity dimension.
- A large coordinate domain contains only sparse marked objects and each object affects only a constant-size neighborhood.
---

## When to use
- A general numerical optimizer is applied to a low-dimensional smooth objective with symmetry or a fixed-sum constraint.
- A brute-force candidate loop repeatedly scans input to derive a value that is independent of the candidate or derivable from one fixed witness.
- A permutation or route enumeration uses absolute differences on a line and appears to cover an interval.
- A scan over cut positions has a convex, monotone, symmetric, or piecewise-linear objective whose optimum must lie near balanced divisions or structural boundaries.
- A simulator repeatedly decrements, trims, copies, or recursively splits arrays while producing an area, envelope, or aggregate profile.
- A nested loop repeatedly sorts overlapping subsets or slices and the result depends only on rectangle membership or range counts.
- A profile is constrained by local slope changes and has a small bounded height or capacity dimension.
- A large coordinate domain contains only sparse marked objects and each object affects only a constant-size neighborhood.

## Steps
1. State the objective and constraints mathematically before changing implementation.
2. Look for symmetry, equal-partition arguments, AM-GM, derivatives, interval-span identities, convexity, monotonicity, or divisibility shortcuts.
3. Prove whether the optimum is a direct formula, lies among a constant number of boundary candidates, or can be restricted to existing coordinates.
4. Separate candidate-independent preprocessing from candidate-dependent validation; hoist anchors, sorted data, prefixes, caps, and coordinate sets outside hot loops.
5. Use one stable witness to reconstruct candidate parameters, then perform a single early-terminating consistency pass.
6. For geometric membership objectives, compress distinct coordinates and use 2D prefix sums or inclusion-exclusion for constant-time range counts.
7. For recursive or layer-based simulations, identify the resulting static piecewise-linear envelope and accumulate its integral directly.
8. If local transitions change state only slightly and a value bound is small, use DP over position and bounded state with transitions such as decrease, hold, and increase.

## Complexity
- Time: Prefer O(1) closed forms when algebra permits. Otherwise reduce repeated work to one-time preprocessing plus a single validation pass per candidate, typically O(P + C*P) for C fixed candidates. Coordinate-compressed counting uses O(U^2)
- Space: Use O(1) for formulas and direct candidate evaluation, O(P) for stored observations or points, O(U^2) for compressed prefix tables, O(T*V) or O(V) for profile DP depending on whether path reconstruction is needed, and O(U) for sparse hash

## Pitfalls
- Applying a closed form without proving that variables are continuous or integral as required, or without checking nonnegativity and boundary optima.
- Assuming a formula for ordinary dimensions also covers one-dimensional, unit-sized, empty, or zero-capacity cases.
- Choosing an anchor that may be invalid, such as a zero-valued observation, or assuming valid input guarantees that are not present.
- Changing inclusive rectangle or neighborhood boundaries during coordinate compression.
- Ignoring duplicate discoveries in sparse local enumeration and failing to divide or otherwise correct multiplicities.
- Replacing exact half-step or trapezoid integration with a visually similar but semantically different area formula.
- Using floating-point comparisons for integer geometry or changing output numeric type and formatting unintentionally.
- Introducing sorting, slicing, list construction, NumPy, or generic optimizers inside hot loops.

## When not to use
- The objective lacks exploitable symmetry, locality, monotonicity, convexity, or a genuinely small state bound.
- Candidate values are numerous or data-dependent, making constant-candidate evaluation invalid.
- The coordinate universe is too large for the proposed prefix table or boundary enumeration.
- The height, capacity, or profile state is not small enough for bounded-state DP.
- A general numerical optimizer is necessary because the objective is irregular, nonconvex, high-dimensional, or has no derivable exact solution.
- The brute-force baseline is already comfortably within limits and the transformation would materially increase correctness risk.

## Minimal example
Before:
```py
# O012 focus: collapse
for i in range(n):
    dp[i] = max(dp[j] + 1 for j in range(max(0, i-w), i))
```
After:
```py
# optimized for collapse
for i in range(n):
    dp[i] = seg.query(lo(i), hi(i)) + 1
    seg.update(pos(i), dp[i])
```
