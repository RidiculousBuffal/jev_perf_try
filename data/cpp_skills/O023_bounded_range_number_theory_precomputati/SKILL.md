---
skill_id: O023
type: operator
language: cpp
family: coprimality
name: Bounded Range Number Theory Precomputation and Factor Structure Reduction
description: When many operations involve primes, divisors, factorization, coprimality, or multiplicative functions over a
  known bounded value domain, replace repeated trial division, primality checks, divisor enumeration, and generic state scans
  with one-time dense preprocessing and direct mathematical aggregation. Use an Eratosthenes or linear sieve for primality
  and prime lists, an SPF table for repeated factorization
tags:
- number-theory
- prime-factorization
- sieve
- linear-sieve
- smallest-prime-factor
- precomputation
- prefix-sum
- divisor-counting
- gcd
- bounded-domain
triggers:
- The maximum input value is known or can be collected offline and a dense array fits memory.
- A hot loop repeatedly calls primality, divisor, factorization, or gcd-related helpers.
- The code performs many modulo or division operations against a fixed prime table.
- A hardcoded prime list near the square root of the value bound suggests repeated trial division.
- Many values must be factorized under one shared maximum.
- A direct-addressed boolean, byte, integer, SPF, frequency, or prefix array is feasible.
- Queries ask range counts for a predicate depending only on the queried value.
- The input is processed across multiple test cases or until EOF, allowing preprocessing reuse.
---

## When to use
- The maximum input value is known or can be collected offline and a dense array fits memory.
- A hot loop repeatedly calls primality, divisor, factorization, or gcd-related helpers.
- The code performs many modulo or division operations against a fixed prime table.
- A hardcoded prime list near the square root of the value bound suggests repeated trial division.
- Many values must be factorized under one shared maximum.
- A direct-addressed boolean, byte, integer, SPF, frequency, or prefix array is feasible.
- Queries ask range counts for a predicate depending only on the queried value.
- The input is processed across multiple test cases or until EOF, allowing preprocessing reuse.

## Steps
1. Determine the true numeric bound: use the maximum input/query value, the maximum needed square-root bound, or a safe problem-defined limit.
2. Choose preprocessing: use a byte/boolean Eratosthenes sieve for primality, a linear sieve when a prime list or SPF is needed, and an SPF array when many values require factorization.
3. Build preprocessing once. Store primes compactly and keep all domain-indexed metadata in contiguous arrays.
4. For each value x, factor through SPF with repeated lookup and division. Record a prime once per distinct factor and count exponents locally when needed.
5. Use direct-addressed seen or frequency arrays for bounded prime/value keys; otherwise coordinate-compress distinct keys before aggregation.
6. Replace composite candidate enumeration with distinct prime candidates whenever divisibility by a composite implies divisibility by one of its prime factors.
7. For repeated range queries, materialize the predicate for every value and build a prefix sum; answer each interval with prefix subtraction.
8. For coprimality classification, mark each distinct prime factor globally, maintain the running gcd, and distinguish pairwise, setwise, and non-coprime outcomes.

## Complexity
- Time: For maximum value M, preprocessing is O(M log log M) with Eratosthenes or O(M) with a linear SPF sieve. SPF factorization then costs O(number of extracted prime factors, counting multiplicity as divisions) per value, typically O(log x)
- Space: O(M) for sieve, SPF, flags, frequencies, or prefix sums, plus O(n) input storage when needed. A one-off unbounded factorization can use O(1) extra space aside from a small prime list. Prefer flat arrays over node-based containers whenever

## Pitfalls
- Using trial division up to x/2, x, or the entire prime table after the residual has become one or after p*p exceeds the residual.
- Confusing distinct prime factors with prime exponents; duplicate-prime detection should mark a factor once per input value.
- Checking repeated factors with a linear scan of previously seen primes when a bounded seen array or hash set would give direct lookup.
- Enumerating composite divisors in an optimization where a prime factor is always at least as good.
- Assuming SPF[x] is initialized for every x in the supported domain, especially x=1 and values beyond the sieve limit.
- Using i*i <= x without overflow protection; prefer i <= x / i when the value range may approach 64-bit limits.
- Using floating-point sqrt or pow in hot integer loops; use integer-safe bounds or precomputation.
- Building a prefix sum with incorrect endpoint or zero-index handling.

## When not to use
- The value domain is too large or sparse for O(M) memory and only a few isolated queries are made.
- There is no reusable bound and factorization must handle arbitrary large 64-bit integers; use bounded trial division, Pollard rho, Miller-Rabin, or another appropriate large-integer method.
- Only one small factorization is required and preprocessing cost dominates.
- The predicate depends on query state or history, so a static sieve or prefix sum cannot be reused.
- The mathematical reduction is not valid because composite candidates have a different objective or constraints than their prime factors.
- A generic DP has genuinely many relevant states rather than a small fixed divisor/exponent pattern.

## Minimal example
Before:
```cpp
bool pairwise = true;
for (int i = 0; i < n; ++i)
  for (int j = i + 1; j < n; ++j)
    if (std::gcd(a[i], a[j]) != 1) pairwise = false;
```
After:
```cpp
auto spf = build_spf(*max_element(a.begin(), a.end()));
vector<int> seen(spf.size(), 0);
for (int x : a)
  for (int p : distinct_prime_factors(x, spf))
    if (seen[p]++) pairwise = false;
```
