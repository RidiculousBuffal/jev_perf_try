---
skill_id: O045
type: operator
language: python
family: state_compression
name: Collapse Geometric Expectation to an Exact Formula
description: Replace simulation or truncated summation of repeated independent trials with a closed-form expected value. When
  each attempt has a fixed cost C and an independent success probability p, the number of attempts until the first success
  follows a geometric distribution with expectation 1/p, so the total expected cost is C/p. Use exact arithmetic whenever
  p has an exact representation, such as p = 2^-m, yielding C * 2^m.
tags:
- expected-value
- geometric-distribution
- closed-form
- series-summation
- probability
- exact-arithmetic
- constant-time
triggers:
- A loop sums terms proportional to k * p * (1-p)^(k-1) or (k+1) * p * (1-p)^k.
- A fixed iteration limit approximates an infinite probabilistic series.
- A small epsilon or tail threshold terminates a geometrically decaying sum.
- The code repeatedly computes invariant probability powers inside a loop.
- Floating-point accumulation is followed by rounding to an apparently exact integer.
- The process consists of independent retries with identical success probability and fixed per-attempt cost.
---

## When to use
- A loop sums terms proportional to k * p * (1-p)^(k-1) or (k+1) * p * (1-p)^k.
- A fixed iteration limit approximates an infinite probabilistic series.
- A small epsilon or tail threshold terminates a geometrically decaying sum.
- The code repeatedly computes invariant probability powers inside a loop.
- Floating-point accumulation is followed by rounding to an apparently exact integer.
- The process consists of independent retries with identical success probability and fixed per-attempt cost.

## Steps
1. Identify the fixed cost C incurred by one attempt.
2. Derive the probability p that an attempt succeeds.
3. Verify that attempts are independent and identically distributed, and that the process stops at the first success.
4. Recognize the trial count as a one-based geometric random variable.
5. Apply E[trials] = 1/p.
6. Compute the expected total as C/p.
7. Algebraically simplify the result; for p = 2^-m, use C * 2^m.
8. Implement with integer or exact arithmetic, removing simulation, truncation, epsilon checks, and floating-point rounding.

## Complexity
- Time: O(1) arithmetic operations under the unit-cost model; O(log m) or output-sensitive bit complexity for computing and representing an exact power such as 2^m.
- Space: O(1) auxiliary space under the unit-cost model; output-sensitive space for the exact integer result.

## Pitfalls
- Using a finite cutoff for an infinite series and assuming the omitted tail is negligible.
- Confusing the geometric distribution's one-based and zero-based conventions.
- Applying 1/p when attempts are not independent or do not share the same success probability.
- Ignoring costs that vary between attempts or depend on previous failures.
- Recomputing invariant powers or using floating-point arithmetic for an exact power-of-two result.
- Overflow in fixed-width integer languages when the exact result grows exponentially.
- Calling the formula constant time without accounting for the bit complexity of constructing or printing a large integer.

## When not to use
- Success probabilities change after each attempt or depend on prior outcomes.
- Attempts are correlated, stopping conditions involve multiple states, or the process is not memoryless.
- Per-attempt costs vary with the attempt number or failure history.
- The required quantity is a distribution, percentile, variance, or tail probability rather than the mean.
- The success probability is unavailable in closed form and numerical computation is genuinely required.
- The process may never succeed with positive probability, making the expected stopping time infinite.

## Minimal example
Before:
```py
best = 0
for mask in range(1 << n):
    best = max(best, score(mask))
```
After:
```py
odd = sum(x & 1 for x in a)
# replace brute-force subset scan with parity/count closed form
best = closed_form_from_counts(len(a), odd)
```
