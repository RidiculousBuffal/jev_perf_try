---
skill_id: O029
type: operator
language: python
family: graph
name: Optimized Union Find for Large Connectivity Workloads
description: Upgrade or repair an existing disjoint-set union implementation without changing the connectivity algorithm.
  Use path compression and union by size or rank, link only roots, expose a consistent minimal API, and avoid full component
  reconstruction during query processing. For reverse offline queries, preserve reverse insertion, component-size invariants,
  and reversed output. Reduce Python overhead with buffered
tags:
- disjoint-set-union
- union-find
- dynamic-connectivity
- connected-components
- offline-reverse-processing
- path-compression
- union-by-size
- union-by-rank
- buffered-io
- amortized-optimization
triggers:
- A parent array represents roots by negative sizes or separate rank/size metadata.
- Repeated merge and same-component queries dominate runtime.
- The implementation follows parent links without path compression.
- Unions attach roots arbitrarily, by index, or directly modify non-root nodes.
- The code already uses reverse processing for deletions or maintains a running pair-count invariant.
- Component answers depend only on component sizes or the number of connected components.
- The DSU class has mismatched, missing, truncated, or obfuscated method names.
- Helpers enumerate members, roots, or groups during query processing.
---

## When to use
- A parent array represents roots by negative sizes or separate rank/size metadata.
- Repeated merge and same-component queries dominate runtime.
- The implementation follows parent links without path compression.
- Unions attach roots arbitrarily, by index, or directly modify non-root nodes.
- The code already uses reverse processing for deletions or maintains a running pair-count invariant.
- Component answers depend only on component sizes or the number of connected components.
- The DSU class has mismatched, missing, truncated, or obfuscated method names.
- Helpers enumerate members, roots, or groups during query processing.

## Steps
1. Identify the required operations and reduce the interface to find, union, same, and optionally a component counter.
2. Repair or replace inconsistent method names so every caller uses one coherent API.
3. Initialize each vertex as a singleton set.
4. Implement find with path compression, preferably iteratively in Python to reduce recursion overhead and recursion-limit risk.
5. Implement union by size or rank, always finding both roots before linking.
6. For a negative-size representation, keep sizes only at roots and merge the smaller tree into the larger tree.
7. Maintain a component counter initialized to the vertex count and decrement it only after a successful union.
8. For reverse offline processing, add edges in reverse order, update the invariant using the product of the two component sizes, append answers, and reverse them once for output.

## Complexity
- Time: O((n + q) * alpha(n)) amortized for initialization and q union/find operations, plus any unavoidable O(n) final scan. Reverse pair-count processing has the same bound.
- Space: O(n) for parent and rank/size metadata, plus O(a) for buffered answers if outputs are not streamed, where a is the number of emitted answers.

## Pitfalls
- Fixing external method names while leaving internal recursive calls pointed at nonexistent names.
- Linking arbitrary vertices instead of roots.
- Using union by node index, which does not control tree height.
- Assuming path compression alone provides the same practical robustness as path compression plus balancing.
- Recursively finding roots on potentially deep trees in Python.
- Recomputing component counts with repeated full scans or materialized group lists.
- Using a generic DSU helper that performs O(n) work for every query.
- Forgetting to decrement the component count only when two distinct roots merge.

## When not to use
- Edges or relations are deleted online and no reverse processing, rollback, or alternate dynamic-connectivity technique is available.
- Operations require shortest paths, distances, spanning-tree structure, explicit group membership, or path queries rather than only connectivity.
- The relation is directed and reachability cannot be represented by undirected components.
- The workload requires splitting components or undoing arbitrary unions without a rollback-capable structure.
- The graph is small enough that a simpler traversal is clearer and performance is not a concern.
- Component contents must be enumerated frequently; a structure designed for explicit membership may be more appropriate.

## Minimal example
Before:
```py
parent = list(range(n))
def find(x):
    while parent[x] != x: x = parent[x]
    return x
def union(a, b):
    ra, rb = find(a), find(b)
    if ra != rb: parent[rb] = ra
```
After:
```py
parent, size = list(range(n)), [1] * n
def find(x):
    while parent[x] != x: parent[x], x = parent[parent[x]], parent[x]
    return x
def union(a, b):
    ra, rb = find(a), find(b)
    if ra != rb:
        if size[ra] < size[rb]: ra, rb = rb, ra
        parent[rb], size[ra] = ra, size[ra] + size[rb]
```
