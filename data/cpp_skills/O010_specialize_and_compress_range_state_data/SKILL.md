---
skill_id: O010
type: operator
language: cpp
family: dp
name: Specialize and Compress Range State Data Structures
description: Optimize large C++ workloads by matching the data structure to the exact update/query algebra instead of using
  a general-purpose tree. Replace linear scans, per-element range edits, sqrt decomposition, redundant Fenwick/segment-tree
  combinations, or explicit range-to-graph expansion with compact flat-array structures. Use lazy propagation for composable
  range updates, direct monoid aggregation for online
tags:
- segment-tree
- lazy-propagation
- range-update
- range-query
- range-min
- range-max
- point-update
- point-query
- offline-processing
- sweep-line
triggers:
- A range operation scans elements or buckets directly, yielding O(length), O(sqrt(n)), or O(n) work per operation.
- Many online range additions, assignments, minimum/maximum queries, or point updates share one index domain.
- A lazy segment tree maintains fields that are never queried, such as subtree sums for a point-query-only workload.
- A segment tree is built from an all-zero array even though only deferred tags are needed.
- The implementation maintains both a Fenwick tree and a segment tree for overlapping responsibilities.
- Node payloads store indices, raw values, or multiple minima when only one scalar aggregate or a small fixed tuple is consumed.
- A root-only special update, duplicated query routine, or asymmetric propagation path exists.
- All updates finish before answers are materialized, or every leaf is queried individually after the update phase.
---

## When to use
- A range operation scans elements or buckets directly, yielding O(length), O(sqrt(n)), or O(n) work per operation.
- Many online range additions, assignments, minimum/maximum queries, or point updates share one index domain.
- A lazy segment tree maintains fields that are never queried, such as subtree sums for a point-query-only workload.
- A segment tree is built from an all-zero array even though only deferred tags are needed.
- The implementation maintains both a Fenwick tree and a segment tree for overlapping responsibilities.
- Node payloads store indices, raw values, or multiple minima when only one scalar aggregate or a small fixed tuple is consumed.
- A root-only special update, duplicated query routine, or asymmetric propagation path exists.
- All updates finish before answers are materialized, or every leaf is queried individually after the update phase.

## Steps
1. Write down the exact invariant and operation algebra: sum, min, max, affine addition, assignment, timestamped overwrite, or a small product monoid.
2. Determine whether operations are online. If not, bucket events by a monotone coordinate, defer evaluation, or process only the final required state.
3. Choose the weakest sufficient structure: Fenwick tree for prefix-like sums, iterative segment tree for point updates plus extrema, lazy segment tree for composable range updates, tag-only tree for offline leaf evaluation, or timestamp-cover tree for range
4. Use a flat std::vector or contiguous arrays with a power-of-two base. Derive intervals from recursion parameters or iterative indices instead of storing l/r in every node.
5. Store only query-visible state. Replace argmin/argmax indices with scalar values when positions are not needed; otherwise pack all required alternatives into one aggregate and merge them in one pass.
6. For range additions or affine updates, apply the operation to a fully covered node and compose its lazy tag without descending. Push only when a partial traversal requires child state.
7. For range assignment plus point queries, store value-plus-version metadata on covered nodes and resolve the latest version by scanning the root-to-leaf path; do not maintain subtree aggregates.
8. For offline final answers, remove push-up and internal aggregates, accumulate tags on covered nodes, then perform one DFS or linear leaf pass carrying inherited tags.

## Complexity
- Time: Typically O((N + Q) log N) for online range updates/queries or point updates/range aggregates; O(Q log N + N) for offline tag accumulation followed by one final leaf traversal; O((N + M) log M) for event-bucketed sweep-line DP
- Space: Usually O(N) for a flat segment tree, lazy tags, event buckets, or compressed coordinates; O(N log N) helper nodes/edges may be required for segment-tree graph compression. Use packed scalar arrays or small fixed aggregates to reduce

## Pitfalls
- Using lazy propagation without proving that the update operation composes correctly.
- Dropping an index or tie-break field that is actually required for deterministic selection or later reconstruction.
- Using a scalar aggregate when multiple fallback candidates are needed, causing repeated invalidation and re-querying.
- Applying half-open and closed interval conventions inconsistently during the conversion.
- Forgetting to propagate all components of an affine or multi-field lazy tag.
- Materializing every leaf or pushing every tag when only the root aggregate or a few point queries are needed.
- Leaving an explicit build, push-up, or root-special update after switching to a tag-only or uniform lazy design.
- Relying on zero or index-zero sentinels instead of explicit identity values such as INF or -INF.

## When not to use
- The number of operations is small enough that a direct scan is comfortably within limits.
- Updates are non-composable, require arbitrary historical state, or do not admit a compact lazy representation.
- The workload is static and prefix-only, where sorting, prefix sums, sparse tables, or a Fenwick tree is simpler and faster.
- All positions must be output after every operation; a deferred offline tree cannot replace required online materialization.
- A range-to-graph compression is invalid because target sets are not contiguous or cannot be covered by a logarithmic decomposition.
- The existing O(n log n) implementation is already dominated by unavoidable sorting, geometry, SCC, or I/O costs rather than tree operations.

## Minimal example
Before:
```cpp
vector<long long> a(n);
for (auto [l, r, x] : updates)
    for (int i = l; i <= r; ++i) a[i] += x;
for (int i : queries) cout << a[i] << '\n';
```
After:
```cpp
int S = 1; while (S < n) S <<= 1;
vector<long long> lazy(2 * S);
for (auto [l, r, x] : updates)
    for (l += S, r += S + 1; l < r; l >>= 1, r >>= 1) {
        if (l & 1) lazy[l++] += x;
        if (r & 1) lazy[--r] += x;
    }
for (int i : queries) { long long v = 0; for (int p = i + S; p; p >>= 1) v += lazy[p]; cout << v << '\n'; }
```
