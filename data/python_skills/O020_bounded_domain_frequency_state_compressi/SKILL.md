---
skill_id: O020
type: operator
language: python
family: streaming
name: Bounded Domain Frequency State Compression
description: Replace repeated scans, sorting, general-purpose frequency structures, and unnecessary input or output materialization
  with a compact frequency state. Use direct-address arrays when values belong to a small known range; otherwise use a sparse
  map. Maintain only the aggregate invariant required by the output, such as a running sum, pair total, distinct count, parity,
  or cached per-value result. Process streams
tags:
- frequency-counting
- bounded-domain
- direct-address-array
- running-aggregate
- value-replacement
- query-processing
- state-compression
- streaming
- precomputation
- I/O-optimization
triggers:
- Values are small, nonnegative, and bounded by a known compact range.
- Queries replace or transfer all occurrences of one value to another.
- Only counts per value matter; element positions or slot identities do not.
- A query repeatedly scans dictionary keys, a small collection, or a list to find a frequency.
- The output depends on a global aggregate plus the frequency of the current value.
- A combinatorial helper is called with a fixed small parameter such as pair counting.
- Input can be consumed once without retaining the original sequence.
- Output is determined by a fixed ordered alphabet or numeric domain.
---

## When to use
- Values are small, nonnegative, and bounded by a known compact range.
- Queries replace or transfer all occurrences of one value to another.
- Only counts per value matter; element positions or slot identities do not.
- A query repeatedly scans dictionary keys, a small collection, or a list to find a frequency.
- The output depends on a global aggregate plus the frequency of the current value.
- A combinatorial helper is called with a fixed small parameter such as pair counting.
- Input can be consumed once without retaining the original sequence.
- Output is determined by a fixed ordered alphabet or numeric domain.

## Steps
1. Identify the minimal sufficient state: frequency, presence, parity, running sum, pair total, or another invariant.
2. Validate the value bounds and allocate a zero-initialized direct-address array when the domain is compact; otherwise use a sparse map.
3. Count values during the initial stream pass, simultaneously maintaining any simple aggregate such as total sum.
4. For global replacements from x to y, let moved = freq[x], update the aggregate by (y - x) * moved, then perform freq[y] += moved and freq[x] = 0.
5. For incremental transitions from x to x+1, decrement freq[x] and increment freq[x+1] while updating any multiplicative or modular aggregate.
6. For pair counts, use c * (c - 1) // 2 instead of factorial-based combinations.
7. When each output depends only on a value's frequency, compute and cache one result per distinct value, then reuse it.
8. When only presence or distinctness matters, replace exact frequencies with a presence marker and derive the required parity or count formula.

## Complexity
- Time: Typically O(n + q + V) with a dense domain of size V, or O(n + q + u) expected with a sparse map containing u distinct values. Repeated-scan implementations can degrade to O(nu), O(nk log k), or O(n^2); the state-compressed form makes
- Space: O(V) for a dense frequency or presence array, or O(u) for sparse counts and caches. Stream processing can avoid O(n) input storage; output buffering may add O(n) if batching is chosen.

## Pitfalls
- Using a dense array when the value range is huge or sparse, causing unnecessary memory and full-domain scans.
- Assuming bounded values without validating or documenting the bound.
- Forgetting to clear the source bucket after transferring its count.
- Updating counts but not updating the associated running aggregate.
- Recomputing the same per-value result for every duplicate element.
- Using factorials or generic combinatorial helpers for fixed small formulas.
- Retaining the full input when only frequencies or aggregates are needed.
- Sorting all frequencies when only the maximum and its ties are required.

## When not to use
- Values are unbounded, very large, or sufficiently sparse that dense direct addressing wastes memory.
- Queries depend on positions, order, individual identities, or the full reconstructed sequence.
- The required operation needs ordered keys, range queries, predecessor or successor queries, or other structure beyond exact-value lookup.
- The output requires a complete frequency ranking rather than only maxima or a simple aggregate.
- The aggregate cannot be updated from local bucket changes and must be recomputed from detailed state.
- Input size is small enough that general-purpose containers are clearer and performance is irrelevant.

## Minimal example
Before:
```py
values = [int(x) for x in input().split()]
for _ in range(int(input())):
    x, y = map(int, input().split())
    moved = sum(v == x for v in values)
    values = [y if v == x else v for v in values]
    print(sum(values))
```
After:
```py
MAX_VALUE = 100000
freq = [0] * (MAX_VALUE + 1)
total = 0
for value in map(int, input().split()): freq[value] += 1; total += value
for _ in range(int(input())):
    x, y = map(int, input().split()); moved = freq[x]
    total += (y - x) * moved; freq[y] += moved; freq[x] = 0; print(total)
```
