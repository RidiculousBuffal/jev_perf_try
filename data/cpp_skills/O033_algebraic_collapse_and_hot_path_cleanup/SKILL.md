---
skill_id: O033
type: operator
language: cpp
family: combinatorics
name: Algebraic Collapse and Hot Path Cleanup
description: Optimize already-correct or near-correct C++ solutions by first searching for mathematical identities, closed
  forms, direct feasibility conditions, and structural invariants before applying micro-optimizations. Replace bounded simulation,
  repeated probabilistic summation, brute-force reconstruction, and incremental threshold searches with exact formulas when
  the recurrence or equations permit it. Within loops that
tags:
- math
- closed-form
- algebraic-simplification
- constant-factor
- hot-loop
- common-subexpression-elimination
- simulation-elimination
- integer-arithmetic
- modular-arithmetic
- frequency-counting
triggers:
- A loop accumulates a sequence with a recognizable formula such as a triangular number or geometric series.
- A large fixed-count loop approximates an expectation or probability tail using multiplicative decay.
- A brute-force variable is only an algebraic unknown and all constructed values are affine expressions of it.
- The same pure expression, power, product, modulo, or array lookup is evaluated multiple times in one iteration.
- A condition is written through a derived temporary instead of the direct feasibility or comparison it represents.
- A formula contains repeated additions, subtractions, or expanded ceil/floor division that can be algebraically collapsed.
- A scan iterates over an entire domain even though only values occurring in the input can contribute.
- A previous-occurrence or state transition needs only the latest indexed value but uses binary search or a heavier structure.
---

## When to use
- A loop accumulates a sequence with a recognizable formula such as a triangular number or geometric series.
- A large fixed-count loop approximates an expectation or probability tail using multiplicative decay.
- A brute-force variable is only an algebraic unknown and all constructed values are affine expressions of it.
- The same pure expression, power, product, modulo, or array lookup is evaluated multiple times in one iteration.
- A condition is written through a derived temporary instead of the direct feasibility or comparison it represents.
- A formula contains repeated additions, subtractions, or expanded ceil/floor division that can be algebraically collapsed.
- A scan iterates over an entire domain even though only values occurring in the input can contribute.
- A previous-occurrence or state transition needs only the latest indexed value but uses binary search or a heavier structure.

## Steps
1. Establish the observable contract: input consumption, output order and formatting, equality behavior, valid ranges, and whether extra input must be consumed.
2. Inspect the recurrence, loop invariant, equations, and monotonicity before changing data structures or loop bounds.
3. Derive a closed form, direct threshold inequality, geometric expectation, triangular-number inverse, or algebraic reconstruction whenever possible.
4. Replace floating-point simulation with exact integer arithmetic when the result is mathematically integral; use long double only for an initial estimate and correct it with a small integer adjustment loop.
5. Collapse equivalent expressions and branches into direct formulas, such as triangular numbers, simplified ceil-division, direct product comparison, or explicit resource-feasibility tests.
6. Hoist loop-invariant values and cache common subexpressions, including powers, products, residual formulas, alternate output values, and branch decisions.
7. Reuse loop-carried state instead of recomputing it in loop conditions and bodies; update it once for the next iteration.
8. Use direct indexing for bounded domains and latest-occurrence tables; compress values or use a hash map only when bounds require it.

## Complexity
- Time: (pattern dependent)
- Space: (pattern dependent)

## Pitfalls
- Calling a wider loop or a larger search range an optimization when it only increases work and masks a brittle bound.
- Replacing an O(N) direct lookup with binary search, accidentally worsening the complexity to O(N log K).
- Adding pruning arithmetic, gcds, or fraction normalization whose overhead exceeds the saved iterations.
- Using floating-point pow, expectation accumulation, or final rounding when an exact integer formula exists.
- Assuming `% MOD` is free or repeatedly reducing operands that are already normalized.
- Changing iteration order or output buffering without preserving exact output order, separators, newlines, or required input consumption.
- Leaving equality cases uncovered when branching on the sign of a derived difference.
- Printing an uninitialized accumulator because no branch handles the zero-difference case.

## When not to use
- Do not force a closed form when the process is state-dependent, nonstationary, or lacks a provable invariant.
- Do not replace exact enumeration when the omitted states can contribute despite appearing sparse or zero under an invalid assumption.
- Do not use floating-point algebraic reconstruction for values requiring exact equality unless it is followed by integer verification.
- Do not trade O(N) direct access for a more complex structure when the value domain is safely bounded and dense.
- Do not add output buffering when memory is tight, output is small, or streaming is required by the interface.
- Do not prioritize micro-optimizations over a genuinely superior asymptotic algorithm when constraints make the current class infeasible.

## Minimal example
Before:
```cpp
// O033 focus: algebraic
long long ans = 0;
for (int x = 1; x <= n; ++x)
  for (int y = 1; y <= n; ++y) {
    int z = S - x - y;
    if (1 <= z && z <= n) ans += f(x, y, z);
  }
```
After:
```cpp
// optimized for algebraic
long long ans = 0;
for (int x = 1; x <= n; ++x) {
  int lo = max(1, S - x - n), hi = min(n, S - x - 1);
  for (int y = lo; y <= hi; ++y) ans += f_fast(x, y, S - x - y);
}
```
