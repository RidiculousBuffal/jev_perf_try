---
skill_id: O005
type: operator
language: python
family: dp
name: Collapse Repetitive Simulation into Arithmetic and Tight State Transitions
description: Replace loops that repeatedly subtract, add, round, or count fixed-size progress with direct integer arithmetic,
  usually quotient, remainder, ceiling division, or an algebraically derived invariant. When a closed form is unavailable,
  preserve the algorithm while removing avoidable allocations, copying, repeated container operations, and unnecessary state.
  Stream one-pass inputs when random access is not required
tags:
- simulation-to-formula
- closed-form
- ceiling-division
- integer-arithmetic
- invariant
- greedy
- state-compression
- constant-factor-optimization
- streaming
- allocation-reduction
triggers:
- A loop repeatedly subtracts or adds the same fixed amount and only the final count matters.
- The answer is the minimum integer k satisfying a linear threshold inequality.
- A loop counter equals a quotient, or an overshoot correction equals a remainder.
- The result depends only on grouped counts, weights, quotients, remainders, or the current scalar state.
- A modulo check followed by a conditional increment implements ceiling division.
- A list, slice, reverse, or temporary container is created only to be iterated once.
- A simulation repeatedly scans suffixes or prefixes and performs avoidable copying.
- A local greedy process mutates only adjacent positions and can be represented by a carry or leftover.
---

## When to use
- A loop repeatedly subtracts or adds the same fixed amount and only the final count matters.
- The answer is the minimum integer k satisfying a linear threshold inequality.
- A loop counter equals a quotient, or an overshoot correction equals a remainder.
- The result depends only on grouped counts, weights, quotients, remainders, or the current scalar state.
- A modulo check followed by a conditional increment implements ceiling division.
- A list, slice, reverse, or temporary container is created only to be iterated once.
- A simulation repeatedly scans suffixes or prefixes and performs avoidable copying.
- A local greedy process mutates only adjacent positions and can be represented by a carry or leftover.

## Steps
1. Write the loop invariant after k iterations.
2. Express the stopping condition as an inequality and solve for the smallest valid integer k.
3. Use integer-only arithmetic: `(x + y - 1) // y` for positive values, or `-(-x // y)` when sign behavior is intended.
4. Replace repeated subtraction with quotient and remainder; preserve residual state with `%` rather than overshoot-and-restore logic.
5. Aggregate fixed-denomination or grouped contributions directly from counts and weights.
6. For affine progress, derive the closed form before considering micro-optimizations.
7. If no closed form exists, remove inner-loop slicing, copying, reversal, and repeated allocations while preserving the recurrence exactly.
8. Use indexed traversal or range-based iteration over an existing sequence instead of materializing suffixes or filler lists.

## Complexity
- Time: Typically reduces value-dependent simulation from O(answer) or O(input magnitude) to O(1). For scans, greedy passes, and queue simulations, the asymptotic bound usually remains O(n), O(n + operations), or O(n^2); the optimization removes
- Space: Closed-form arithmetic uses O(1) auxiliary space. One-pass carry and streaming transformations generally use O(1) extra space beyond required input storage. Removing temporary query lists or slices can reduce space from O(n + q) to O(n)

## Pitfalls
- Using floating-point division with `ceil` for large integers when integer ceiling division is exact and simpler.
- Applying `(x + y - 1) // y` without confirming the divisor and domain are positive.
- Deriving a formula from the loop while ignoring initialization, strict versus non-strict thresholds, or off-by-one effects.
- Forcing a closed form when transitions depend on history, order, or nonuniform events.
- Replacing a correct O(n) or O(n + operations) algorithm with a custom data structure that has the same asymptotic cost and higher Python overhead.
- Creating slices, reversed copies, temporary query lists, or `[0] * n` comprehension drivers unnecessarily.
- Streaming data that is later needed for random access.
- Compressing state without preserving carry dependencies or mutation order.

## When not to use
- The loop has meaningful side effects, irregular increments, data-dependent transitions, or history-dependent behavior that cannot be summarized by a small invariant.
- Intermediate states are required for output, later queries, reconstruction, or correctness.
- The divisor may be zero, signs are mixed, or the arithmetic identity has not been validated for the full input domain.
- The workload is already constant-time and the proposed change is only a notation rewrite with no clarity or robustness benefit.
- The algorithmic bottleneck is genuinely asymptotic, such as repeated independent suffix computations under large constraints; removing slices alone is insufficient.
- A custom queue, node layout, or helper abstraction is not supported by profiling or performs worse than optimized built-ins.

## Minimal example
Before:
```py
# O005 focus: collapse
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
