---
skill_id: O019
type: operator
language: cpp
family: combinatorics
name: Hoisted Modular Combinatorics and Incremental Hot Loop Optimization
description: When repeated modular combinations, inverses, powers, or equivalent arithmetic dominate a C++ solution, move
  invariant work out of hot loops and select the simplest matching formulation. Under a prime modulus, precompute factorials
  and inverse factorials once, answer binomial queries in O(1), and use iterative binary exponentiation only for the single
  required inverse seed or genuinely sparse queries. For sums
tags:
- combinatorics
- factorial-precomputation
- inverse-factorial
- binomial-coefficients
- modular-arithmetic
- prime-modulus
- incremental-recurrence
- dynamic-programming
- knapsack
- grid-distance
triggers:
- A loop calls modular exponentiation with exponent MOD-2 once per index, query, factorial, or DFS transition.
- A fixed prime modulus and many binomial or factorial-based queries are present.
- The same factorial products, inverse products, or combination coefficients are rebuilt inside a loop.
- Adjacent summation terms differ by an exponent of exactly one, a sign flip, or a simple coefficient ratio.
- Alternating signs are implemented as pow(-1, k) instead of parity or a sign toggle.
- A recurrence array is consumed in order and each state depends only on the previous state.
- A combinatorial DP groups equal values even though direct per-item 1D knapsack fits the bounds.
- A bounded value domain is handled with map/set lookup instead of a flat direct-address table.
---

## When to use
- A loop calls modular exponentiation with exponent MOD-2 once per index, query, factorial, or DFS transition.
- A fixed prime modulus and many binomial or factorial-based queries are present.
- The same factorial products, inverse products, or combination coefficients are rebuilt inside a loop.
- Adjacent summation terms differ by an exponent of exactly one, a sign flip, or a simple coefficient ratio.
- Alternating signs are implemented as pow(-1, k) instead of parity or a sign toggle.
- A recurrence array is consumed in order and each state depends only on the previous state.
- A combinatorial DP groups equal values even though direct per-item 1D knapsack fits the bounds.
- A bounded value domain is handled with map/set lookup instead of a flat direct-address table.

## Steps
1. Determine the maximum factorial argument required across all queries and allocate fact and ifact arrays only to that bound.
2. Build fact[i] forward with fact[i] = fact[i-1] * i mod MOD.
3. Compute ifact[MAX] once with iterative binary exponentiation: powmod(fact[MAX], MOD-2), assuming MOD is prime and the value is invertible.
4. Fill inverse factorials backward with ifact[i-1] = ifact[i] * i mod MOD.
5. Implement C(n, r) as a guarded O(1) lookup: return zero for n < 0, r < 0, or r > n.
6. If only a few combinations are needed, retain factorials and compute the few required inverses on demand instead of constructing a full inverse-factorial table.
7. Normalize combination parameters with r = min(r, n-r) when using partial products or sparse-query formulas.
8. For consecutive summands, precompute loop-invariant inverses and update powers by multiplication with the base inverse.

## Complexity
- Time: With full factorial/inverse-factorial preprocessing, O(N + log MOD) setup and O(1) per binomial query. Consecutive-term recurrences reduce a K-term sum from commonly O(K log MOD) or repeated O(K * coefficient-cost) to O(K) after setup
- Space: O(N) for factorial and inverse-factorial tables, with O(1) extra space per query. Rolling recurrences and one-dimensional knapsack use O(1) and O(S) auxiliary space respectively. Direct-address tables use O(value_range), coordinate

## Pitfalls
- Precomputing inverse factorials by calling modular exponentiation for every index, turning O(N) setup into O(N log MOD).
- Building full factorial and inverse tables for a single query when only a handful of coefficients are required.
- Assuming Fermat inversion works for a non-prime modulus or for a value divisible by the modulus.
- Forgetting 64-bit widening before multiplying two modulo-sized integers.
- Using a combination helper that returns one for invalid negative arguments instead of zero.
- Computing a remainder before proving the divisor is nonzero.
- Recomputing the same subexpression, such as a residual linear-equation term, several times per iteration.
- Using pow(-1,k) for parity or repeated pow(base, exponent) when exponents change by one.

## When not to use
- The modulus is composite or required inverses do not exist; use prime-factor methods, CRT, Lucas-type methods, or another modulus-appropriate technique.
- Only one or two small combination queries exist and partial products are clearly cheaper than allocating and filling large tables.
- The required factorial bound is too large for memory, or n exceeds the range where factorials modulo the chosen modulus are valid without additional number-theoretic handling.
- The problem requires combinations with n at or beyond the modulus and ordinary factorial tables would contain zero.
- A grouped-value DP has substantially smaller state complexity than processing every item, so direct per-item knapsack would be too slow.
- The value domain is large or sparse and cannot be safely direct-addressed without compression.

## Minimal example
Before:
```cpp
vector<long long> fact(MAXN + 1);
init_fact(fact, MOD);
long long ans = nCr(N + e - 1, N - 1, fact, MOD);
ans = ans * mod_pow(x, MOD - 2, MOD) % MOD;
```
After:
```cpp
int e = factor_exp(m, p);
long long ans = comb_small_k(N + e - 1, e, MOD);
ans = ans * mod_inv(x, MOD) % MOD;
// avoid oversized global factorial tables
```
