---
skill_id: O022
type: operator
language: python
family: combinatorics
name: Bounded Arithmetic and Native Primitive Optimization
description: Optimize Python numeric hot paths by replacing handwritten implementations with optimized built-ins, keeping
  modular values bounded, eliminating redundant recomputation, and reformulating exact large-number arithmetic as factorized
  modular arithmetic. Typical applications include factorials, modular exponentiation, weighted sums, small-state dynamic
  programs, and expressions involving a global LCM under a prime
tags:
- python-optimization
- native-builtins
- modular-arithmetic
- bounded-integers
- big-integer-avoidance
- factorial
- modular-exponentiation
- prime-factorization
- lcm
- modular-inverse
triggers:
- A Python loop manually implements an operation already provided by a native standard-library primitive.
- A custom binary exponentiation routine or string-based bit scan computes a^b modulo M.
- The same exponent or other invariant quantity is recomputed inside a loop.
- A result is needed modulo M, but accumulators or products are reduced only at the end.
- Exact LCM, quotient, factorial, or power values grow far beyond the required modular result.
- A formula is expressed with repeated indexed terms that can be split into reusable weighted sums.
- A fixed-size DP repeatedly calls modular exponentiation or performs avoidable per-update work.
- Input uses eval or unbuffered parsing for plain numeric data.
---

## When to use
- A Python loop manually implements an operation already provided by a native standard-library primitive.
- A custom binary exponentiation routine or string-based bit scan computes a^b modulo M.
- The same exponent or other invariant quantity is recomputed inside a loop.
- A result is needed modulo M, but accumulators or products are reduced only at the end.
- Exact LCM, quotient, factorial, or power values grow far beyond the required modular result.
- A formula is expressed with repeated indexed terms that can be split into reusable weighted sums.
- A fixed-size DP repeatedly calls modular exponentiation or performs avoidable per-update work.
- Input uses eval or unbuffered parsing for plain numeric data.

## Steps
1. Identify the mathematical operation represented by the hot loop and check for a C-backed built-in or library primitive.
2. Use math.factorial for a complete factorial computation when materializing the full integer is acceptable; otherwise retain modular accumulation or use a problem-specific factorial method.
3. Use pow(base, exponent, modulus) for modular exponentiation instead of manual loops, recursion, binary strings, or pow(base, exponent) followed by modulo.
4. Preserve algebraic formulas while computing each independent modular term directly and normalize the final signed combination with % MOD.
5. Move invariant computations outside loops and replace repeated powers, coefficients, or state transitions with rolling updates or precomputed tables.
6. Reduce accumulators modulo MOD during accumulation when unreduced values could become large; group reductions when safe to lower modulo overhead.
7. Rewrite weighted pairwise expressions as directional or coefficient-weighted sums so each input element is processed once.
8. For expressions involving sum(LCM(values) / a_i) modulo a prime, factor each value, retain the maximum exponent of every prime, reconstruct the LCM modulo MOD, and replace exact division with modular inverses.

## Complexity
- Time: Native substitution generally preserves the mathematical asymptotic bound while reducing Python-level constants. Modular exponentiation is O(log exponent). Linear weighted scans and bounded modular DP remain O(n) times their fixed state
- Space: Built-in factorial may require memory proportional to the size of the full factorial before reduction, unlike a modular running accumulator. Built-in modular exponentiation uses O(1) auxiliary space. Weighted scans use O(1) extra space

## Pitfalls
- Assuming a native substitution improves asymptotic complexity; factorial replacement is usually a constant-factor speedup.
- Using math.factorial for inputs so large that constructing the unreduced factorial causes unacceptable memory usage.
- Computing pow(base, exponent) without a modulus and applying % MOD afterward, which can create enormous intermediate integers.
- Replacing built-in pow with a recursive or iterative Python implementation that has the same asymptotic complexity but worse constants.
- Applying modular inverses when a divisor is zero modulo MOD or when the modulus is not prime without using an appropriate inverse method.
- Building an exact global LCM before reducing modulo the target modulus.
- Confusing modular division with integer floor division; modular inversion preserves the congruence only under valid invertibility conditions.
- Reducing every scalar update unnecessarily when grouped reductions are safe and faster.

## When not to use
- Do not materialize a full factorial when n is large enough that its memory footprint is unsafe or when only a modular factorial is required.
- Do not use modular inverses unless all denominators are invertible under the chosen modulus.
- Do not apply the LCM factorization strategy when exact integer quotients are required as output.
- Do not build a full sieve when the value bound is too large or only a few factorizations are needed.
- Do not force modular reduction into a computation whose exact intermediate values are semantically required.
- Do not rewrite already efficient built-in modular exponentiation or closed-form expressions unless profiling identifies a real bottleneck.

## Minimal example
Before:
```py
# O022 focus: bounded
ans = 0
for x in range(1, n+1):
    for y in range(1, n+1):
        z = S - x - y
        if 1 <= z <= n: ans += f(x, y, z)
```
After:
```py
# optimized for bounded
ans = 0
for x in range(1, n+1):
    lo = max(1, S-x-n); hi = min(n, S-x-1)
    for y in range(lo, hi+1): ans += f_fast(x, y, S-x-y)
```
