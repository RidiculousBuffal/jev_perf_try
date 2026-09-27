---
skill_id: O007
type: operator
language: python
family: combinatorics
name: Precompute Modular Combinatorics and Simplify Counting
description: Optimize repeated binomial-coefficient computations and combinatorial counting by replacing exact or per-query
  multiplicative construction with reusable factorial, inverse, and inverse-factorial tables under a prime modulus. When the
  count is constrained by a two-variable linear equation, enumerate one variable directly, solve the other with a divisibility
  check, and evaluate the contribution with O(1) binomial
tags:
- combinatorics
- binomial-coefficients
- modular-arithmetic
- prime-modulus
- factorial-precomputation
- inverse-factorials
- contribution-technique
- diophantine-enumeration
- sorting
- counting
triggers:
- A binomial helper loops over r or constructs numerator and denominator products for every query.
- A combination helper performs modular exponentiation or inversion on every call.
- Many outputs use combinations with a common maximum n and a prime modulus.
- Factorial tables are rebuilt per query or sized to a fixed bound unrelated to the actual constraints.
- A full inverse-factorial table is built using repeated modular exponentiation when one inverse and a reverse sweep would
  suffice.
- A counting formula contains a nested overlap or convolution-style summation despite only two bounded variables satisfying
  a linear relation.
- The code uses gcd/lcm transformations and branch-heavy feasibility logic where direct divisibility testing is possible.
- A sorted-array solution separately computes minimum and maximum contributions, creates ascending and descending copies,
  or repeats equivalent binomial queries.
---

## When to use
- A binomial helper loops over r or constructs numerator and denominator products for every query.
- A combination helper performs modular exponentiation or inversion on every call.
- Many outputs use combinations with a common maximum n and a prime modulus.
- Factorial tables are rebuilt per query or sized to a fixed bound unrelated to the actual constraints.
- A full inverse-factorial table is built using repeated modular exponentiation when one inverse and a reverse sweep would suffice.
- A counting formula contains a nested overlap or convolution-style summation despite only two bounded variables satisfying a linear relation.
- The code uses gcd/lcm transformations and branch-heavy feasibility logic where direct divisibility testing is possible.
- A sorted-array solution separately computes minimum and maximum contributions, creates ascending and descending copies, or repeats equivalent binomial queries.

## Steps
1. Determine the largest binomial top index required and choose a dynamic, constraint-derived, or shared global precomputation bound.
2. Under a prime modulus, build factorials with fact[i] = fact[i-1] * i modulo MOD.
3. Build inverse factorials either from one Fermat inverse of fact[max_n] followed by a reverse sweep, or by a linear modular-inverse recurrence followed by a forward pass.
4. Implement comb(n, r) with immediate zero for r < 0, r > n, or n < 0; otherwise return fact[n] * ifact[r] * ifact[n-r] modulo MOD.
5. Replace exact products, divisions, and per-query inversions with constant-time table lookups, reducing modulo during every accumulation.
6. For a constraint a*x + b*y = target, enumerate x over its valid bounded range, compute the remainder, require nonnegative divisibility by b, derive y, check its bounds, and add comb(n, x) * comb(n, y).
7. Remove auxiliary overlap loops, gcd/lcm case transformations, and redundant state reconstruction when direct enumeration covers all candidates.
8. For subset min/max contributions, sort once and use value[i] * comb(i, k-1) for maximum roles and value[i] * comb(n-1-i, k-1) for minimum roles; combine the signed sums directly.

## Complexity
- Time: With maximum required binomial index B and solve/output size S: O(B + S) after standard linear precomputation, or O(B + S log S) when sorting is required. Shared tables make repeated cases approximately O(S) each after one O(B) setup
- Space: O(B) for factorial, inverse, and inverse-factorial tables, plus O(S) for input storage or sorting. Contribution scans can use O(1) auxiliary space beyond the input and shared tables.

## Pitfalls
- Precomputing to an arbitrary oversized bound wastes startup time and memory; undersizing causes index failures.
- Using factorial or inverse-factorial formulas when n is at least the modulus is invalid without a different theorem or technique.
- Calling pow(value, MOD-2, MOD) inside a loop turns O(1) combination queries into O(log MOD) operations.
- Building inverse factorials with one terminal inverse and a reverse sweep is usually preferable to computing every modular inverse independently.
- Applying the modulus only after exact factorial or product construction creates expensive big integers.
- Returning a nonzero sentinel for an invalid combination can silently corrupt sums; invalid combinations should normally contribute zero.
- For linear equations, checking divisibility without checking remainder sign and variable bounds counts invalid solutions.
- A direct enumeration may still be linear, but the scan bounds should be restricted using coefficient signs and target bounds where possible.

## When not to use
- The modulus is composite or the required factorial range reaches or exceeds the modulus without an appropriate alternative method.
- There are only one or very few small combination queries where linear multiplicative evaluation is cheaper than table setup.
- Memory limits cannot accommodate O(B) tables and queries are too few to justify them.
- The problem requires exact large integers rather than values modulo a prime.
- The counting relation has many variables, non-linear constraints, or dependencies that cannot be reduced to one-variable enumeration.
- The input range is large but the value domain permits a more suitable frequency-based or generating-function method.

## Minimal example
Before:
```py
# O007 focus: precompute
cnt = 0
for a in range(1, n+1):
    for b in range(1, n+1):
        for c in range(1, n+1):
            if a + b + c == S: cnt += 1
```
After:
```py
# optimized for precompute
cnt = 0
for a in range(1, n+1):
    lo = max(1, S-a-n); hi = min(n, S-a-1)
    if lo <= hi: cnt += (hi - lo + 1)
```
