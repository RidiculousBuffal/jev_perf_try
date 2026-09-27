---
skill_id: O032
type: operator
language: python
family: coprimality
name: Reduce, Factor, and Aggregate Prime Structure Directly
description: Replace indirect divisor enumeration, repeated trial factorization, redundant factorization of related inputs,
  and dense factor state with direct arithmetic structure. First reduce shared-factor problems using gcd. Factor only the
  necessary value, preferably with SPF or a reusable prime table for bounded multi-query inputs, and count exponents or distinct
  primes while dividing the residual in place. Aggregate the
tags:
- number-theory
- prime-factorization
- gcd-reduction
- smallest-prime-factor
- sparse-aggregation
- greedy-counting
- multiplicative-functions
- single-query
- multi-query
- constant-factor-optimization
triggers:
- The output depends on common divisibility or shared prime structure of two integers.
- The code factors multiple related values even though only common factors matter.
- A loop scans every integer up to sqrt(n), including composite candidates.
- A list of repeated prime factors is later deduplicated or folded in a second pass.
- A dense array indexed by numeric value stores sparse prime-exponent state.
- Many bounded input values are factorized independently with trial division.
- The result depends only on prime exponents, distinct prime factors, divisor count, divisor sum, or an LCM exponent maximum.
- An exponent loop repeatedly consumes 1, 2, 3, or checks triangular-number thresholds.
---

## When to use
- The output depends on common divisibility or shared prime structure of two integers.
- The code factors multiple related values even though only common factors matter.
- A loop scans every integer up to sqrt(n), including composite candidates.
- A list of repeated prime factors is later deduplicated or folded in a second pass.
- A dense array indexed by numeric value stores sparse prime-exponent state.
- Many bounded input values are factorized independently with trial division.
- The result depends only on prime exponents, distinct prime factors, divisor count, divisor sum, or an LCM exponent maximum.
- An exponent loop repeatedly consumes 1, 2, 3, or checks triangular-number thresholds.

## Steps
1. Identify the minimal arithmetic object that determines the answer; for shared-factor queries compute g = gcd(a, b) before factorization.
2. Avoid materializing divisor sets or repeated factor lists unless the interface explicitly requires them.
3. Choose factorization strategy by workload: direct trial division for a small one-off value, prime-only trial division when useful, SPF preprocessing for many bounded values, and advanced factorization for very large integers.
4. Maintain a residual value and repeatedly divide out each discovered prime, recording only the needed exponent, distinct-prime count, or aggregate contribution.
5. Stop when the residual reaches 1 or when the trial divisor exceeds the residual square root.
6. If the residual is greater than 1 after the loop, treat it as one remaining prime factor with exponent 1.
7. Use sparse maps for prime-exponent state; avoid arrays sized by the maximum numeric value unless dense access is genuinely required.
8. Fuse factorization with multiplicative aggregation when intermediate factors are not externally needed.

## Complexity
- Time: Direct trial division is O(sqrt(x)) worst case for one target x, with lower practical work when the residual shrinks. After gcd reduction, the target is x = gcd(a,b), giving O(log min(a,b) + factorization(x)). Prime-only trial division
- Space: Direct one-off factorization uses O(1) auxiliary space or O(k) for k distinct factors if stored. Sparse aggregation uses O(k) space, where k is the number of observed primes. SPF preprocessing uses O(M) space and sparse aggregate state

## Pitfalls
- Factoring both original inputs when only gcd(a, b) matters.
- Enumerating all divisors and re-factorizing them to detect prime powers.
- Generating a full sieve for a single small query where direct factorization is cheaper.
- Using SPF or a large sieve without accounting for preprocessing and memory costs.
- Scanning composite trial divisors instead of primes or a suitable wheel.
- Forgetting to count a residual prime greater than 1.
- Counting repeated prime occurrences when only distinct primes are required.
- Storing sparse exponent data in a dense max-value array.

## When not to use
- Do not build an SPF sieve for a single small input when its preprocessing and memory cost exceed direct factorization.
- Do not reduce to gcd when the answer depends on factors unique to each input rather than their shared structure.
- Do not discard full factor lists or divisor sets when the output explicitly requires their order, multiplicity, or enumeration.
- Do not use basic trial division for very large hard composites or cryptographic-scale integers; use a robust primality test and Pollard-Rho-style factorization.
- Do not replace a genuinely necessary divisor search with exponent aggregation unless the result is provably determined by prime exponents.
- Do not fuse aggregation into factorization when intermediate factors are needed by later independent computations.

## Minimal example
Before:
```py
def common_prime_count(a, b):
    def factors(n):
        out = []
        for p in range(2, int(n ** 0.5) + 1):
            while n % p == 0:
                out.append(p)
                n //= p
        if n > 1: out.append(n)
        return set(out)
    return len(factors(a) & factors(b))
```
After:
```py
from math import gcd

def common_prime_count(a, b):
    g = gcd(a, b)
    count = 0
    p = 2
    while p * p <= g:
        if g % p == 0:
            count += 1
            while g % p == 0: g //= p
        p += 1 if p == 2 else 2
    return count + (g > 1)
```
