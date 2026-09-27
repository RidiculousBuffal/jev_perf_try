---
skill_id: O009
type: operator
language: python
family: graph
name: Invariant Driven Optimization and Data Structure Strengthening
description: Optimize implementations by first identifying the smallest state or exact combinatorial objective required by
  the output, then replacing fragile simulations, redundant arithmetic, repeated scans, mutable-list operations, and hash-heavy
  storage with structures aligned to the invariant. Typical upgrades include parity propagation on trees, iterative traversal,
  dense boolean marking, set-based membership, coordinate
tags:
- state-compression
- parity-propagation
- tree-traversal
- iterative-graph-processing
- dense-indexing
- coordinate-compression
- fenwick-tree
- order-statistics
- bipartite-matching
- maximum-flow
triggers:
- The output uses only a projection of maintained state, such as parity rather than full weighted distance.
- The input is a tree or otherwise has unique paths, allowing one traversal to propagate all required states.
- Recursive traversal, extreme recursion limits, or repeated full traversals appear in Python.
- A loop repeatedly performs membership checks against a list.
- Identifiers are dense integers in a known bounded range and the task only needs membership or overlap.
- A solution repeatedly removes elements from Python lists or rescans unmatched candidates.
- Each item can be used at most once and compatibility is a pairwise boolean relation.
- A greedy pairing exists, but local choices can affect the global maximum.
---

## When to use
- The output uses only a projection of maintained state, such as parity rather than full weighted distance.
- The input is a tree or otherwise has unique paths, allowing one traversal to propagate all required states.
- Recursive traversal, extreme recursion limits, or repeated full traversals appear in Python.
- A loop repeatedly performs membership checks against a list.
- Identifiers are dense integers in a known bounded range and the task only needs membership or overlap.
- A solution repeatedly removes elements from Python lists or rescans unmatched candidates.
- Each item can be used at most once and compatibility is a pairwise boolean relation.
- A greedy pairing exists, but local choices can affect the global maximum.

## Steps
1. Write down the exact output invariant and discard information that cannot affect it.
2. Choose an explicit representation matching that invariant: parity or color flags, boolean membership arrays, compressed ranks, matching edges, or lines.
3. For trees, root the structure and use iterative DFS or BFS with parent tracking; propagate parity with XOR of edge weight parity when only parity matters.
4. For weighted-distance queries, compute one reusable source-distance array iteratively and preserve the query formula without recomputing traversals.
5. For bounded integer identifiers, replace sets with boolean arrays and test overlap by direct indexed scanning without materializing intersections.
6. For nearest-allowed-value searches, convert forbidden values to a set, search candidates in the required distance order, and encode tie-breaking explicitly.
7. For pairwise one-to-one compatibility, build a bipartite graph and solve maximum cardinality matching with augmenting paths, Kuhn, or Dinic instead of mutating candidate lists.
8. For offline two-dimensional processing, sort by the primary coordinate, compress the secondary coordinate once into unique dense ranks, and reuse mapped indices.

## Complexity
- Time: Usually preserves linear or O(n log n) complexity while reducing constants; set-based bounded searches become O(R + n), dense overlap checks O(m + n), compressed Fenwick sweeps O(n log n), iterative tree preprocessing O(n + q), matching
- Space: Use O(n) for compressed states, iterative tree traversal, dense flags, and reusable distance arrays; coordinate-compressed Fenwick sweeps use O(n); explicit bipartite matching uses O(V + E), commonly O(n^2) for dense compatibility; Li

## Pitfalls
- Calling a behavior-preserving rewrite an asymptotic optimization when the dominant complexity is unchanged.
- Replacing full distances with parity without confirming that no later computation needs magnitudes.
- Using dense arrays when identifiers are sparse, unbounded, or too large for practical allocation.
- Relying on recursion limits for deep trees instead of using an explicit stack or queue.
- Using list membership or middle deletion inside a hot loop.
- Materializing an intersection when only non-emptiness is required.
- Assuming a greedy matching is optimal merely because it works on sorted examples.
- Building a matching graph when constraints are large enough to require a specialized dominance or flow optimization.

## When not to use
- Do not compress state if the discarded information is needed by later queries or output.
- Do not use dense boolean arrays when IDs are sparse, very large, or the active set is much smaller than the universe.
- Do not build a full matching or flow network when the graph is too large and a proven specialized greedy, sweep, or dominance algorithm is available.
- Do not use a Li Chao tree when monotone slopes and query order are guaranteed and a deque or head-index convex hull is simpler and faster.
- Do not replace a correct greedy algorithm merely for abstraction if constraints are tiny and implementation simplicity is more valuable.
- Do not stream input when later logic genuinely requires random access to all records.

## Minimal example
Before:
```py
from collections import defaultdict

def root_parity(n, edges):
    g = defaultdict(list)
    for u, v, w in edges: g[u].append((v, w)); g[v].append((u, w))
    dist = [0] * n
    def dfs(u, p):
        for v, w in g[u]:
            if v != p: dist[v] = dist[u] + w; dfs(v, u)
    dfs(0, -1); return [d % 2 for d in dist]
```
After:
```py
def root_parity(n, edges):
    g = [[] for _ in range(n)]
    for u, v, w in edges: g[u].append((v, w & 1)); g[v].append((u, w & 1))
    parity = [-1] * n; parity[0] = 0; stack = [0]
    while stack:
        u = stack.pop()
        for v, bit in g[u]:
            if parity[v] < 0: parity[v] = parity[u] ^ bit; stack.append(v)
    return parity
```
