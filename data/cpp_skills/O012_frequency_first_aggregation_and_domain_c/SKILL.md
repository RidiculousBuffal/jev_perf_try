---
skill_id: O012
type: operator
language: cpp
family: state_compression
name: Frequency First Aggregation and Domain Compression
description: Reusable optimization pattern distilled from weighted traces.
tags:
- frequency-counting
- histogramming
- sorting-elimination
- sparse-compression
- bounded-domain
- top-k-maintenance
- parity
- greedy
- monotone-queries
- suffix-sums
triggers:
- The code sorts values only to group equal elements or recover frequencies.
- A fixed-size frequency array exists, but the implementation still sorts the raw input or all zero-filled buckets.
- The answer depends only on counts, duplicate parity, the largest few pair candidates, or a small number of frequency buckets.
- A count array is scanned repeatedly to recover first, second, or top-k modes after updates.
- A dense bucket-pair enumeration tests monotone threshold predicates such as a1 + a2 >= K and b1 + b2 >= L.
- A sparse local-update problem materializes every affected state and sorts them before aggregation.
- A boolean visited or reachability array is also being used to encode duplicates or invalidity.
- A full auxiliary array or memset is used for state that can be derived online or represented by a compact list of active
  keys.
---

## When to use
- The code sorts values only to group equal elements or recover frequencies.
- A fixed-size frequency array exists, but the implementation still sorts the raw input or all zero-filled buckets.
- The answer depends only on counts, duplicate parity, the largest few pair candidates, or a small number of frequency buckets.
- A count array is scanned repeatedly to recover first, second, or top-k modes after updates.
- A dense bucket-pair enumeration tests monotone threshold predicates such as a1 + a2 >= K and b1 + b2 >= L.
- A sparse local-update problem materializes every affected state and sorts them before aggregation.
- A boolean visited or reachability array is also being used to encode duplicates or invalidity.
- A full auxiliary array or memset is used for state that can be derived online or represented by a compact list of active keys.

## Steps
1. Determine whether the result depends on order, or only on the multiset of values and their frequencies. If order is irrelevant, remove sorting from the primary plan.
2. Choose the representation: flat frequency array for a safe dense bounded domain, coordinate-compressed vector for sparse values, or a hash/map for online sparse updates.
3. Accumulate counts while reading whenever later logic needs only frequencies; avoid storing and reordering the full input unless reconstruction requires positions.
4. If sorting frequency values is necessary, extract only positive frequencies or the observed value interval; never sort structural zeros.
5. For duplicate or parity logic, track the exact semantic quantity directly. Use frequency parity, pair counts, or separate fields rather than overloading one boolean state.
6. If only the best few frequencies or candidates matter, maintain top-1/top-2 or top-k online, including the distinct-value conflict case explicitly.
7. For pair conditions that are monotone in multiple coordinates, replace all bucket-pair enumeration with per-element complement thresholds and a suffix-sum, Fenwick, or equivalent rectangle query.
8. For sparse constant-radius updates, update the affected key's current count and its histogram incrementally instead of storing all generated candidates and sorting them.

## Complexity
- Time: Typical transformations are O(n + V) time for dense bounded counting, O(n + d log d) for counting plus sorting d positive buckets, O(n + R log R) for sorting an observed interval of width R, expected O(n) or O(n log d) for sparse
- Space: Use O(V) for a dense bounded histogram, O(d) for compressed distinct frequencies, O(u) for sparse associative counts, O(E^2) for a small feature-grid suffix table, and O(1) extra space when a sorted array is already required and only

## Pitfalls
- Using a counting array without proving that every key is within bounds; switch to compression or hashing when values may be negative or large.
- Sorting n frequency slots when only d positive frequencies or an observed interval of width R is relevant.
- Assuming a dense-domain optimization is asymptotically better when the domain is large or sparse; choose storage based on min(domain size, active keys).
- Counting ordered pairs and dividing by two while forgetting self-pairs, duplicate removal, or threshold-satisfying same-bucket combinations.
- Clamping feature coordinates too early and then adding complicated corrective passes instead of querying exact complement requirements.
- Using one boolean for reachability, multiplicity, and invalidity; these states are not interchangeable.
- Maintaining only the best candidate and forgetting that a collision between two groups requires the runner-up.
- Allowing the same value to form two sides without verifying that at least four occurrences exist.

## When not to use
- The answer genuinely depends on sorted order, adjacency, inversions, ranks, medians, or positional relationships rather than multiplicities.
- The key domain is too large for direct indexing and the number of distinct keys is close to n, making sorting simpler or faster than hashing.
- Exact values or original positions are required later and cannot be reconstructed from frequencies.
- The feature grid is not small enough for a dense suffix table and no efficient sparse range-query structure is available.
- Input updates require deletions, online queries, or rollback semantics not supported by the proposed aggregate.
- A local greedy decision is not justified by a global exchange argument or frequency invariant.

## Minimal example
Before:
```cpp
// O012 focus: frequency
vector<int> ans;
for (int x = 1; x <= MAXV; ++x) {
  bool ok = true;
  for (const auto& grp : groups) if (!binary_search(grp.begin(), grp.end(), x)) ok = false;
  if (ok) ans.push_back(x);
}
```
After:
```cpp
// optimized for frequency
vector<int> freq(MAXV + 1, 0);
for (const auto& grp : groups)
  for (int x : grp) ++freq[x];
for (int x = 1; x <= MAXV; ++x)
  if (freq[x] == (int)groups.size()) ans.push_back(x);
```
