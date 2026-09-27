---
skill_id: O031
type: operator
language: python
family: coprimality
name: Bounded Domain Sieve and Prefix Lookup
description: Reusable optimization pattern distilled from weighted traces.
tags:
- precomputation
- sieve
- number-theory
- multiple-queries
- prefix-sum
- range-query
- dense-lookup
- predecessor-query
- offline-processing
- Python-performance
triggers:
- Many queries reuse the same bounded numeric universe.
- The queried predicate depends only on each value, not on query-specific state.
- Queries repeatedly scan overlapping intervals or retest the same values.
- A primality or divisibility helper is called inside a loop over many consecutive values.
- Each query asks for a cumulative aggregate such as a prefix count or prefix sum.
- Each query asks for the greatest valid value or event at or below a threshold.
- The implementation stores sparse qualifying values only to binary-search or linearly scan them later.
- The domain maximum is small or moderate enough to allocate arrays indexed by value.
---

## When to use
- Many queries reuse the same bounded numeric universe.
- The queried predicate depends only on each value, not on query-specific state.
- Queries repeatedly scan overlapping intervals or retest the same values.
- A primality or divisibility helper is called inside a loop over many consecutive values.
- Each query asks for a cumulative aggregate such as a prefix count or prefix sum.
- Each query asks for the greatest valid value or event at or below a threshold.
- The implementation stores sparse qualifying values only to binary-search or linearly scan them later.
- The domain maximum is small or moderate enough to allocate arrays indexed by value.

## Steps
1. Determine the true maximum required value from constraints or all query endpoints; ensure the preprocessing domain covers it.
2. Represent values directly by index, preferably with a bytearray or boolean array.
3. Build a standard batch classifier. For primality, use an Eratosthenes-style sieve and mark composites from p*p through the domain.
4. Express the target property as an indexed indicator array, reusing the precomputed base predicate for all derived checks.
5. For range counts, build pref[x] = pref[x-1] + indicator[x] and answer [l, r] with pref[r] - pref[l-1].
6. For cumulative sequence values, append the running aggregate when each qualifying value is discovered and answer by direct index lookup.
7. For predecessor or nearest-valid queries, scan values once while carrying the latest valid event and fill a dense best[x] table; answer each threshold with best[x].
8. Use binary search on a sparse sorted list only when the domain is too large for dense lookup or queries are too few to justify an auxiliary table.

## Complexity
- Time: Preprocessing is typically O(M log log M) for a sieve plus O(M) for classification or dense prefix construction. Query time is O(1) per range, cumulative-index, or dense predecessor lookup; sparse-list binary search costs O(log K). Total
- Space: O(M) for the base predicate and one or more prefix/answer arrays; compact byte-oriented storage can reduce constants. Sparse-list variants use O(M + K), where K is the number of qualifying values.

## Pitfalls
- Choosing a sieve limit based on an approximate expected count instead of the maximum possible query.
- Building a prime list, a derived special-value list, and then another lookup structure when one indexed table would suffice.
- Recomputing primality, classification, sums, or interval scans inside every query.
- Using prefix sums without allocating a sentinel entry, causing l=0 or l=1 boundary errors.
- Failing to clamp or validate query endpoints against the precomputed domain.
- Starting composite marking at 2*p instead of p*p, causing redundant writes.
- Using extended-slice assignment that repeatedly creates temporary lists and hidden copies in Python.
- Assuming a dense lookup is always better; large domains with sparse queries may favor a sorted list plus bisect.

## When not to use
- The predicate depends on query-specific state, updates, or changing data.
- Queries are mostly one-off and cover tiny intervals, making preprocessing more expensive than direct evaluation.
- The domain is unbounded or the maximum cannot be determined safely.
- The underlying operation is not decomposable into prefix aggregation or monotone predecessor lookup.
- Updates occur frequently; use a dynamic range-query structure instead of a static prefix table.

## Minimal example
Before:
```py
def twin_prime_count(l, r):
    return sum(is_prime(x) and is_prime(x - 2) for x in range(l, r + 1))

for _ in range(int(input())):
    l, r = map(int, input().split()); print(twin_prime_count(l, r))
```
After:
```py
q = int(input()); queries = [tuple(map(int, input().split())) for _ in range(q)]
limit = max(r for _, r in queries); prime = bytearray(b"\x01") * (limit + 1); prime[:2] = b"\x00\x00"
for p in range(2, int(limit ** .5) + 1):
    if prime[p]: prime[p*p:limit+1:p] = b"\x00" * (((limit - p*p) // p) + 1)
pref = [0] * (limit + 1)
for x in range(2, limit + 1): pref[x] = pref[x-1] + (prime[x] and prime[x-2])
for l, r in queries: print(pref[r] - pref[l-1])
```
