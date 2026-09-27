---
skill_id: O028
type: operator
language: cpp
family: combinatorics
name: Expose Algebraic Structure, Precompute Reuse, and Transform Hot Convolutions
description: A reusable optimization pattern for C++ solutions whose slow path repeatedly recomputes algebraically identical
  values, scatters DP transitions, or simulates structured power sequences one step at a time. First derive the invariant
  or closed form, then tabulate bounded quantities, replace repeated range scans with prefix aggregates, and recognize pairwise
  index-combination loops as polynomial convolution. Use NTT
tags:
- dynamic-programming
- generating-functions
- polynomial-convolution
- NTT
- FFT
- FWT
- combinatorics
- modular-arithmetic
- precomputation
- prefix-sums
triggers:
- A DP transition contains an inner loop of the form dp[target + offset] += source[target] * kernel[offset].
- The same bounded power, inverse, binomial, probability, or subtree-size expression is recomputed inside a hot loop.
- A helper scans an entire interval for every query even though its result depends only on endpoints, parity, minima, maxima,
  or prefix aggregates.
- Nested loops combine all pairs of values and contribute only by their sum, difference, or total degree.
- A state evolves as value *= base across every exponent or time step, producing a sequence of field power sums.
- The modulus is NTT-friendly, or the required transform length is a manageable power of two.
- Tree formulas repeatedly call modular exponentiation or inversion with arguments drawn from a small bounded domain such
  as subtree sizes.
- A hot loop performs repeated modular inverses, binary exponentiation, or division-based modulo reductions.
---

## When to use
- A DP transition contains an inner loop of the form dp[target + offset] += source[target] * kernel[offset].
- The same bounded power, inverse, binomial, probability, or subtree-size expression is recomputed inside a hot loop.
- A helper scans an entire interval for every query even though its result depends only on endpoints, parity, minima, maxima, or prefix aggregates.
- Nested loops combine all pairs of values and contribute only by their sum, difference, or total degree.
- A state evolves as value *= base across every exponent or time step, producing a sequence of field power sums.
- The modulus is NTT-friendly, or the required transform length is a manageable power of two.
- Tree formulas repeatedly call modular exponentiation or inversion with arguments drawn from a small bounded domain such as subtree sizes.
- A hot loop performs repeated modular inverses, binary exponentiation, or division-based modulo reductions.

## Steps
1. Write down the mathematical meaning of the repeated computation and identify which arguments actually vary.
2. Derive a closed form or direct endpoint/parity formula before optimizing loops.
3. For small bounded domains, build iterative power tables, factorials, inverse factorials, binomial tables, probability tables, or size-keyed memo tables once.
4. Build prefix sums over the reusable dimension so interval aggregates become O(1) range differences.
5. Reindex DP transitions by target total when that exposes the reusable contribution and yields a convolution.
6. Represent pairwise sum or degree aggregation as dense coefficient/frequency arrays.
7. Choose an exact convolution method: NTT under a suitable prime, FFT with careful rounding, or FWT for XOR-like operations.
8. Pad to a power-of-two length that prevents cyclic wraparound unless cyclic convolution is intended.

## Complexity
- Time: Typical improvements are from O(N*M), O(K^2), or repeated O(log MOD) work per state to O(L log L) convolution, O(B^2 + DP), O(U log MOD + traversal), or O(1) table/prefix queries after O(B^2) or O(B) preprocessing. NTT/FFT convolution
- Space: Usually O(L) per transform plus O(B^2), O(B), or O(n) tables and rolling DP layers. Prefer reusable scratch buffers and two DP layers when prior layers are not needed. Dense precomputation is appropriate only when the bounded domain fits

## Pitfalls
- Applying NTT or FFT when the coefficient domain is too small; a direct O(B^2) method may be faster for small bounds.
- Choosing an insufficient transform length and accidentally introducing cyclic aliasing.
- Using an incompatible modulus, primitive root, or inverse-transform normalization.
- Forgetting to preserve zero-frequency, zero-element, or boundary terms when reindexing algebraically.
- Dividing by a singular transform component caused by conservation or sum-to-one constraints; keep that component symbolic or solve the affine system separately.
- Changing DP update order incorrectly when converting an in-place transition to rolling layers.
- Failing to normalize negative prefix differences or modular subtraction.
- Recomputing transform roots, bit-reversal permutations, factorials, or inverse tables for every layer or query.

## When not to use
- The input is a single tiny query where preprocessing dominates.
- The transition kernel is sparse, irregular, non-separable, or does not depend only on an aggregate index.
- The coefficient range is too small for transform overhead to amortize, or too large for the available transform modulus and memory.
- The modulus is not transform-friendly and a safe multi-modulus or CRT implementation is unjustified.
- The problem requires exact arbitrary-precision values and floating-point FFT rounding is unsafe.
- A direct closed-form O(1) or linear scan already fits comfortably; do not replace it with factorial tables or transforms.

## Minimal example
Before:
```cpp
for (int sum = 0; sum <= K; ++sum) {
    for (int len = 0; len <= sum; ++len)
        ndp[sum] = (ndp[sum] + 1LL * dp[sum - len] * kernel[len]) % MOD;
}
```
After:
```cpp
vector<int> ndp = atcoder::convolution(dp, kernel);
ndp.resize(K + 1);
for (int &x : ndp) x %= MOD;
```
