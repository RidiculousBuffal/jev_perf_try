---
skill_id: O037
type: operator
language: cpp
family: graph
name: Offline Batch Restructuring with Contiguous Sorts and Compact Lookup
description: Optimize offline C++ workloads by matching the representation and data structure to the actual query pattern.
  Replace quadratic or repeated-pass ordering with one std::sort over contiguous records and preserve original indices for
  output. When ranking is independent by a categorical key, bucket records by group, sort each bucket once, and emit answers
  in original order. For offline distinct counting, prefer
tags:
- offline-processing
- sorting
- contiguous-data
- custom-comparator
- original-index-preservation
- grouped-ranking
- lexicographic-order
- deduplication
- hashing
- rolling-hash
triggers:
- A batch task uses bubble sort, repeated insertion, adjacent swaps, or repeated scans to produce a final ordering.
- The result requires sorted composite keys but output must refer to original positions.
- A second global sort exists only to restore input order.
- The required rank or answer depends only on records sharing a group key.
- A custom hash table has far fewer buckets than stored elements or covers a huge sparse key universe.
- The goal is offline distinct counting rather than online membership queries.
- A hot comparator repeats strcmp, string comparisons, or other expensive work for the same operands.
- A binary-search feasibility check performs many std::map operations or uses operator[] for read-only membership tests.
---

## When to use
- A batch task uses bubble sort, repeated insertion, adjacent swaps, or repeated scans to produce a final ordering.
- The result requires sorted composite keys but output must refer to original positions.
- A second global sort exists only to restore input order.
- The required rank or answer depends only on records sharing a group key.
- A custom hash table has far fewer buckets than stored elements or covers a huge sparse key universe.
- The goal is offline distinct counting rather than online membership queries.
- A hot comparator repeats strcmp, string comparisons, or other expensive work for the same operands.
- A binary-search feasibility check performs many std::map operations or uses operator[] for read-only membership tests.

## Steps
1. Read all input into a contiguous vector of lightweight records.
2. Store the original 0-based or 1-based index in each record when it is read.
3. Implement a strict weak ordering comparator using const references; compute each expensive key comparison once and apply numeric tie-breakers only when needed.
4. Call std::sort exactly once for a global ordering task, then output preserved original indices.
5. If ordering is only within groups, retain the original records separately, append each sortable value to a vector bucket keyed by the group, and sort each bucket independently.
6. Assign ranks while traversing sorted buckets when possible; otherwise use lower_bound per original record. Emit answers by iterating the saved input-order records.
7. For sparse exact-key membership, encode keys in one linear pass, use a compact separate-chaining or open-addressing table, reserve adequate capacity, and keep load factor low.
8. Use a prime-like bucket count for chained hashing or a power-of-two capacity with a strong integer mixer for open addressing. Handle empty sentinels, growth, and termination explicitly.

## Complexity
- Time: (pattern dependent)
- Space: Usually O(n) records plus O(number_of_groups) bucket metadata; grouped ranking uses O(n + G); compact hashing uses O(B + m) where B is bucket capacity and m is stored keys; rolling hashes and powers use O(n); explicit bounded substring

## Pitfalls
- Do not claim a big-O improvement when grouped sorting merely changes decomposition; worst-case time may remain O(n log n).
- Per-record lower_bound after bucket sorting can add unnecessary logarithmic work; assign ranks during a sorted traversal when duplicates and tie semantics permit it.
- Passing comparator arguments by value, using non-const references, or returning non-bool comparator results adds avoidable cost or weakens generic correctness.
- Calling strcmp, strlen, or string comparison multiple times inside std::sort or nested loops can dominate runtime.
- A direct-address table sized by the full encoded universe wastes memory when actual keys are sparse.
- An undersized hash table with linear bucket scans can degrade toward quadratic behavior despite a nominal hashing approach.
- Open-addressing tables require sufficient capacity, a valid empty sentinel, bounded probing, and rehashing before saturation.
- Do not use a sentinel that is also a valid key unless it has explicit escape handling.

## When not to use
- Do not replace a genuinely online or dynamically updated workload with offline sorting.
- Do not use sort-and-scan when queries require immediate insertion and membership responses.
- Do not bucket by group when cross-group ordering, global stability, or interactions between groups affect the answer.
- Do not use explicit substring materialization when nK or the resulting memory footprint is too large.
- Do not rely on rolling hashes when deterministic collision-free equality is mandatory unless hashes are verified.
- Do not switch from a proven linear prefix-function or suffix-structure algorithm to rolling-hash enumeration without measuring; the latter may be asymptotically worse.

## Minimal example
Before:
```cpp
// O037 focus: offline
vector<vector<int>> g(n, vector<int>(n, 0));
for (auto [u, v] : edges) g[u][v] = 1;
queue<int> q;
q.push(0);
```
After:
```cpp
// optimized for offline
vector<vector<int>> adj(n);
for (auto [u, v] : edges) adj[u].push_back(v);
deque<int> q{0};
auto ans = topo_dp(adj);
```
