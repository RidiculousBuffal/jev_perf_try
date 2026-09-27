---
skill_id: O010
type: operator
language: python
family: constant_factor
name: Constant Time Predicate Simplification
description: A reusable skill for optimizing fixed-size Python programs whose executed logic is already O(1). Preserve the
  interface and semantics while simplifying boolean decision trees, replacing indirect or fragile expressions with explicit
  predicates, applying safe integer algebra, removing dead templates and unused imports, and avoiding unnecessary temporary
  allocations. Treat these as clarity, correctness
tags:
- micro-optimization
- constant-time
- predicate-simplification
- branch-reduction
- boolean-logic
- integer-arithmetic
- numeric-stability
- range-check
- fixed-input
- dead-code-elimination
triggers:
- Input consists of a fixed, tiny number of scalar values.
- The executed path has no data-size-dependent loops, recursion, searches, or repeated queries.
- The core operation is one equality, inequality, threshold, range, parity, or distinctness check.
- A dense boolean expression mixes and/or operators or relies on implicit precedence.
- Mirrored or nested branches repeat the same special-case logic.
- An inclusive interval test is expressed through negated comparisons instead of chained comparison.
- Integer inequalities use floating-point division unnecessarily.
- Small fixed-size data is wrapped in list, set, comprehension, or other containers without need.
---

## When to use
- Input consists of a fixed, tiny number of scalar values.
- The executed path has no data-size-dependent loops, recursion, searches, or repeated queries.
- The core operation is one equality, inequality, threshold, range, parity, or distinctness check.
- A dense boolean expression mixes and/or operators or relies on implicit precedence.
- Mirrored or nested branches repeat the same special-case logic.
- An inclusive interval test is expressed through negated comparisons instead of chained comparison.
- Integer inequalities use floating-point division unnecessarily.
- Small fixed-size data is wrapped in list, set, comprehension, or other containers without need.

## Steps
1. Identify the reachable behavior and ignore unrelated template code, unused helpers, and decorative scaffolding.
2. Record the exact input/output contract, comparison boundaries, special values, and numeric-domain assumptions.
3. Confirm that the existing algorithm is already O(1); do not claim an asymptotic improvement when none exists.
4. Reduce the logic to a small decision table or direct predicate before rewriting it.
5. Flatten nested or mirrored branches by checking equality and exceptional cases first, then applying the ordinary rule.
6. Replace equivalent negated bounds with chained comparisons such as lower <= value <= upper.
7. Use direct if/else or conditional expressions instead of boolean-indexed lists, slices, nested literals, or opaque one-liners.
8. Apply algebraic rewrites only when domain assumptions are valid; for positive integer denominators, replace a division threshold with cross-multiplication.

## Complexity
- Time: Usually O(1) before and after. Rewrites may reduce constant factors, allocations, branching, parsing overhead, or floating-point work, but do not change the asymptotic class. For a fixed-arity specialization, dynamic O(k) work can become
- Space: Usually O(1) before and after. Direct unpacking and removal of temporary lists, sets, or containers can reduce constant auxiliary memory.

## Pitfalls
- Mistaking cleanup or readability gains for an asymptotic optimization.
- Copying a large generic template whose imports and helpers add noise or startup overhead.
- Changing a predicate while assuming it is equivalent, especially comparison boundaries such as <= versus ==.
- Applying cross-multiplication without accounting for zero or negative denominators and inequality direction.
- Introducing integer multiplication where another language could overflow; Python integers do not have this issue.
- Changing string comparison to numeric comparison, or vice versa, without confirming intended semantics.
- Replacing explicit branches with clever indexing or precedence-sensitive expressions that are harder to audit.
- Using product parity or other algebraic identities without confirming the operands are integers.

## When not to use
- The input size is variable or large and the real bottleneck involves iteration, searching, sorting, dynamic programming, graph traversal, or repeated queries.
- The proposed rewrite depends on domain assumptions that are not guaranteed.
- A container or helper is required for extensibility, readability, validation, or downstream reuse.
- Input parsing or I/O dominates because the program processes substantial data; use workload-appropriate profiling first.
- The rewrite would trade clear, tested logic for a shorter but opaque expression.
- The reference implementation changes semantics, omits edge cases, or merely appears faster because of unrelated scaffolding.

## Minimal example
Before:
```py
# O010 focus: constant
import numpy as np
arr = np.array(a)
ans = np.sum(arr * arr)
```
After:
```py
# optimized for constant
ans = 0
for x in a:
    ans += x * x
```
