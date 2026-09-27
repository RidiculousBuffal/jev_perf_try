---
skill_id: O021
type: operator
language: python
family: digit
name: Invariant Driven Square Root Candidate Enumeration
description: Replace indirect factorization, subset reconstruction, interval enumeration, or broad base searches with a proof-based
  candidate generator. Derive the relevant arithmetic invariant, enumerate only divisor or factor-pair candidates up to the
  square root, and validate or score candidates online. Use direct integer arithmetic, exploit pair symmetry, and avoid materializing,
  sorting, or recomputing structures that the
tags:
- number-theory
- divisors
- factor-pairs
- sqrt-enumeration
- math
- candidate-generation
- digit-sum
- counting
- optimization
- constant-space
triggers:
- The objective depends on factor pairs or divisors of one integer.
- A solution factorizes a number and then enumerates prime-factor subsets or reconstructs products.
- A fixed divisor-search bound may be smaller than floor(sqrt(N)).
- All relevant divisor pairs can be represented by checking d from 1 through floor(sqrt(N)).
- The code materializes and sorts all divisors even though only the minimum, maximum, or first feasible candidate is needed.
- A broad interval or base search can be rewritten using an arithmetic-series, divisibility, parity, or digit-sum identity.
- A loop repeatedly builds divisor lists or scans overlapping ranges for the same divisibility property.
- A candidate score is symmetric or monotone over a pair (d, N // d), especially when minimizing the larger factor or digit
  length.
---

## When to use
- The objective depends on factor pairs or divisors of one integer.
- A solution factorizes a number and then enumerates prime-factor subsets or reconstructs products.
- A fixed divisor-search bound may be smaller than floor(sqrt(N)).
- All relevant divisor pairs can be represented by checking d from 1 through floor(sqrt(N)).
- The code materializes and sorts all divisors even though only the minimum, maximum, or first feasible candidate is needed.
- A broad interval or base search can be rewritten using an arithmetic-series, divisibility, parity, or digit-sum identity.
- A loop repeatedly builds divisor lists or scans overlapping ranges for the same divisibility property.
- A candidate score is symmetric or monotone over a pair (d, N // d), especially when minimizing the larger factor or digit length.

## Steps
1. State the exact objective and identify whether it is defined over divisors, factor pairs, arithmetic representations, or candidate bases.
2. Derive the governing identity before changing the implementation; examples include N = d * (N // d), 2N = L * (2a + L - 1), and N - S = p * (b - 1).
3. Enumerate integer candidates only through floor(sqrt(X)) using an integer loop condition such as d * d <= X.
4. For every divisor hit, evaluate its complementary factor X // d immediately and update a running best, count, or feasibility result.
5. When minimizing a symmetric factor-pair metric, retain the closest pair to sqrt(X) or directly minimize the pair score.
6. For base-representation constraints, test small bases directly and derive large-base candidates from divisors of the residual expression, then validate each candidate with exact digit-sum computation.
7. For consecutive-sum counting, convert the arithmetic progression equation into factor pairs with the required parity and positivity conditions.
8. For arrays with a divisibility target, generate candidate divisors from relevant values or their total sum, compute remainders, sort once per candidate when necessary, and use prefix sums for feasibility.

## Complexity
- Time: Typically O(sqrt(X)) per integer query, or O(sqrt(X) * log X) when each candidate requires digit or representation validation. For divisor-driven array checks, typical cost is O(D * n log n), where D is the number of relevant divisors; a
- Space: O(1) auxiliary space for streaming factor-pair or base candidates; O(log X) recursion depth if digit evaluation is recursive. Array feasibility variants may require O(n) for residues or prefix sums, while range-wide divisor sieves require

## Pitfalls
- Assuming greedy balancing of prime factors optimizes a factor-pair objective; it is a heuristic and need not produce the best pair.
- Enumerating combinations of prime factors, which can be exponential and may generate duplicate products.
- Stopping at a hardcoded bound that does not cover floor(sqrt(X)).
- Using / instead of //, causing float conversion, precision loss, or incorrect exact comparisons.
- Using floating-point square roots for loop bounds without guarding perfect-square boundaries.
- Materializing and sorting every divisor when only an extremum or early feasible candidate is needed.
- Applying a large-base formula without separately covering small bases or validating reconstructed candidates.
- Forgetting parity, positivity, base-minimum, or exclusion constraints in factor-derived counting formulas.

## When not to use
- The input range is small enough that direct enumeration is simpler and comfortably fast.
- The objective depends on prime exponents or the complete divisor structure, not merely on divisor pairs or a derived candidate.
- The relevant number is too large for trial division and a faster factorization or advanced arithmetic method is required.
- The array operation is positional, such as removal or range queries, where prefix/suffix structures or segment trees directly match the objective.
- Candidate validation is expensive enough that scanning all values through sqrt(X) remains infeasible.
- The derived divisor formula is not proven to cover every valid candidate.

## Minimal example
Before:
```py
# O021 focus: invariant
ans = 0
for i in range(1, n+1):
    ans += len(str(i))
```
After:
```py
# optimized for invariant
ans = 0
for d in range(1, 19):
    L, R = 10**(d-1), min(n, 10**d - 1)
    if L <= R: ans += (R - L + 1) * d
```
