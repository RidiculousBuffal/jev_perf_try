---
skill_id: O014
type: operator
language: cpp
family: dp
name: Offline Sweep and Structure Matched Range Processing
description: Reusable optimization pattern distilled from weighted traces.
tags:
- offline-processing
- sweep-line
- intervals
- sorting
- bucketing
- coordinate-compression
- fenwick-tree
- segment-tree
- range-update
- point-query
triggers:
- The output is required for every index, divisor, time, coordinate, or threshold, but the implementation processes every
  interval or item independently.
- A nested loop repeatedly revisits earlier intervals, candidate states, or query positions.
- Intervals are activated according to length, endpoint, start time, or another bounded monotone key.
- A segment tree supports only range add plus point query; a Fenwick tree over a difference array is sufficient.
- A segment tree maintains only range add plus global maximum or minimum; the objective is a dynamic extremum over positions.
- A static read-only range query is implemented with a segment tree even though the aggregate is additive and prefix-decomposable.
- Boundary searches repeatedly ask for nearest smaller, larger, or equal values without updates.
- Sorted interval lists are intersected with nested scans that restart from the beginning.
---

## When to use
- The output is required for every index, divisor, time, coordinate, or threshold, but the implementation processes every interval or item independently.
- A nested loop repeatedly revisits earlier intervals, candidate states, or query positions.
- Intervals are activated according to length, endpoint, start time, or another bounded monotone key.
- A segment tree supports only range add plus point query; a Fenwick tree over a difference array is sufficient.
- A segment tree maintains only range add plus global maximum or minimum; the objective is a dynamic extremum over positions.
- A static read-only range query is implemented with a segment tree even though the aggregate is additive and prefix-decomposable.
- Boundary searches repeatedly ask for nearest smaller, larger, or equal values without updates.
- Sorted interval lists are intersected with nested scans that restart from the beginning.

## Steps
1. Identify the predicate or transition each interval contributes to and determine whether it is monotone in a threshold, endpoint, length, time, or answer index.
2. Reverse the loop order so the computation follows the required output dimension or a single monotone sweep.
3. Separate unconditional contributions from position-dependent contributions. Count guaranteed cases analytically and leave only the optimization delta in the data structure.
4. Bucket events by an integer activation key when its range is manageable; otherwise sort once by that key.
5. Maintain an explicit invariant such as 'all items with key less than the current sweep value are active'. Activate each item exactly once, typically after answering the current threshold.
6. Compress coordinates when only interval endpoints, query positions, or event boundaries matter.
7. Use a Fenwick tree with difference updates for range add and point query: add +v at l, -v at r+1, and read a prefix sum at x.
8. Use a lazy segment tree for range add with range minimum, maximum, or global-extremum queries; avoid storing sums or metadata not used by the objective.

## Complexity
- Time: Typical complexity is O((N+Q) log U) for one-time sorting or compressed range updates, or O(N + Q) when direct buckets, prefix sums, monotonic stacks, or two pointers apply. A divisor/multiple sweep usually adds O(U log U) structured
- Space: Usually O(N+Q) space, or O(U) when the coordinate domain is directly indexed. Coordinate compression, flat event buckets, Fenwick trees, and lazy segment trees should all be sized to the actual relevant domain rather than a speculative

## Pitfalls
- Activating items with key equal to the current threshold before answering when the invariant requires strictly smaller keys.
- Double-counting intervals that are handled both by an unconditional length or threshold argument and by explicit point probing.
- Using interval length r-l instead of inclusive length r-l+1, or mixing the two conventions across buckets and comparisons.
- Choosing a lazy segment tree for range add and point query, thereby paying recursive traversal, lazy propagation, subtree storage, and cache costs unnecessarily.
- Maintaining segment sums or complex summaries that are never queried.
- Using a Fenwick difference structure when range extrema, range queries, or non-additive updates are required.
- Using a monotonic stack without specifying strict versus non-strict comparisons, causing duplicate values to be counted multiple times or omitted.
- Compressing all records with the same endpoint into one representative when multiple intervals can independently affect the result.

## When not to use
- Queries or updates are genuinely online and future inputs are needed to determine the coordinate mapping or activation order.
- The operation is not monotone and cannot be represented by one-time activation or a stable sweep invariant.
- The data structure needs arbitrary interval queries, order statistics, or noncommutative state not supported by the proposed lightweight structure.
- The coordinate universe is tiny and dense enough that a direct table is simpler and faster.
- The input is too dynamic for static prefix sums, offline sorting, or one-pass pointer advancement.
- A full segment tree is justified because updates and queries require range aggregates, range assignment, range minima or maxima under complex compositions, or multiple independent fields.

## Minimal example
Before:
```cpp
for (auto& q : queries) {
    q.answer = 0;
    for (int i = q.left; i <= q.right; ++i) q.answer += (a[i] <= q.x);
}
```
After:
```cpp
vector<int> by_value(n), by_query(queries.size()); iota(by_value.begin(), by_value.end(), 0); iota(by_query.begin(), by_query.end(), 0);
sort(by_value.begin(), by_value.end(), [&](int i, int j) { return a[i] < a[j]; });
sort(by_query.begin(), by_query.end(), [&](int i, int j) { return queries[i].x < queries[j].x; });
Fenwick bit(n); int p = 0;
for (int id : by_query) { while (p < n && a[by_value[p]] <= queries[id].x) bit.add(by_value[p++], 1); queries[id].answer = bit.sum(queries[id].right) - bit.sum(queries[id].left - 1); }
```
