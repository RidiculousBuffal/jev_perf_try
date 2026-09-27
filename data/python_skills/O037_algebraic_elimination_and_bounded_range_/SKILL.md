---
skill_id: O037
type: operator
language: python
family: combinatorics
name: Algebraic Elimination and Bounded Range Counting
description: Replace brute-force enumeration of bounded integer variables with algebraic feasibility checks, residual-variable
  elimination, interval counting, or closed-form aggregation. When one variable is uniquely determined by a linear constraint,
  solve for it and validate its bounds and divisibility. When many assignments share the same sum, count them by feasible
  intervals or the triangular distribution of bounded pair
tags:
- math
- combinatorics
- bounded-integer-solutions
- linear-constraints
- diophantine-feasibility
- loop-elimination
- range-counting
- brute-force-optimization
- constant-space
triggers:
- A fixed-sum or linear equation constrains several bounded integer variables.
- A nested loop enumerates a variable that is uniquely determined by the other variables.
- The innermost loop only checks whether a residual value is nonnegative, integral, or within a bound.
- A predicate has the form 0 <= target - a - b <= limit.
- Validity depends only on a pair sum or another aggregate rather than individual values.
- A brute-force feasibility search solves a small system of linear equations.
- Bounds are simple intervals or boxes, enabling algebraic pruning.
- The required output is a count or existence decision, not the actual assignments.
---

## When to use
- A fixed-sum or linear equation constrains several bounded integer variables.
- A nested loop enumerates a variable that is uniquely determined by the other variables.
- The innermost loop only checks whether a residual value is nonnegative, integral, or within a bound.
- A predicate has the form 0 <= target - a - b <= limit.
- Validity depends only on a pair sum or another aggregate rather than individual values.
- A brute-force feasibility search solves a small system of linear equations.
- Bounds are simple intervals or boxes, enabling algebraic pruning.
- The required output is a count or existence decision, not the actual assignments.

## Steps
1. Write the constraint explicitly and identify a variable that can be isolated.
2. For a counting equation, choose all but one variable, compute the residual, and test integrality, divisibility, and bounds instead of enumerating the final variable.
3. For an implied variable z = S - x - y, convert 0 <= z <= K into y bounds: max(0, S - x - K) <= y <= min(K, S - x).
4. Add the interval length max(0, upper - lower + 1) rather than scanning every candidate.
5. Restrict outer-loop ranges using necessary feasibility conditions such as max(0, S - 2K) <= x <= K.
6. When variables share [0, N] and validity depends on a pair sum, use pair_count(s) = s + 1 for 0 <= s <= N, pair_count(s) = 2N - s + 1 for N < s <= 2N, and zero otherwise.
7. For a small linear feasibility system, eliminate one variable and derive parity, integrality, and minimum/maximum attainable-value conditions.
8. Normalize arithmetic to integer comparisons: cross-multiply positive denominators and use modulo checks instead of floating-point division.

## Complexity
- Time: (pattern dependent)
- Space: O(1) auxiliary space when counts are accumulated directly; avoid O(N^2) storage for candidate states.

## Pitfalls
- Leaving the eliminated variable as an inner loop, preserving cubic or quadratic work unnecessarily.
- Using division or floating-point comparisons where integer multiplication and modulo provide exact semantics.
- Forgetting the residual variable's divisibility or integrality requirement.
- Checking only nonnegativity and omitting the residual upper bound.
- Using incorrect inclusive interval formulas; a valid integer interval contributes upper - lower + 1.
- Pruning with continue when a monotone break would skip the remaining impossible suffix.
- Scanning a full Cartesian product when the valid region can be represented by clipped ranges.
- Replacing iteration with a compact but opaque boolean or string-indexing expression.

## When not to use
- The eliminated variable has multiple valid values for a fixed choice of the others rather than being uniquely determined.
- Constraints are nonlinear, non-separable, or require state-dependent interactions that cannot be summarized by intervals.
- Variables have irregular domains or constraints that do not form contiguous feasible ranges.
- The task requires enumerating, reconstructing, or outputting every valid assignment.
- The derived formula is more complex than the input limits justify and risks introducing unverifiable boundary errors.
- Multiple queries or changing constraints require a different preprocessing, prefix-sum, dynamic-programming, or generating-function approach.

## Minimal example
Before:
```py
count = 0
for x in range(21):
    for y in range(21):
        for z in range(21):
            count += 3 * x + 5 * y + 7 * z == 100
print(count)
```
After:
```py
count = 0
for x in range(21):
    for y in range(21):
        rem = 100 - 3 * x - 5 * y
        count += rem >= 0 and rem % 7 == 0 and rem // 7 <= 20
print(count)
```
