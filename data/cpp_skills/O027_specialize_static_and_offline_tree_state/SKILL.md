---
skill_id: O027
type: operator
language: cpp
family: graph
name: Specialize Static and Offline Tree State
description: Replace repeated traversal, overgeneralized dynamic-tree structures, and scan-based discovery with the smallest
  data structure that matches the actual invariant. Preprocess static topology once, index derived keys or event times, and
  answer queries through binary lifting, Euler/RMQ, segment trees, DSU contraction, merge trees, or bit-parallel representations
  as appropriate. Preserve semantics while removing
tags:
- tree
- graph
- offline-queries
- ancestor-query
- lca
- binary-lifting
- euler-tour
- segment-tree
- rmq
- union-find
triggers:
- A DFS invokes other DFS/counting routines inside its edge loop or repeatedly rescans overlapping subtrees.
- A parent or ancestor find operation follows raw parent pointers inside a large query loop without compression or indexing.
- The result depends on both a node and operation time, so a single DSU representative is not stable across queries.
- The topology is static and queries only ask LCA, ancestry, path state, or threshold connectivity, but the implementation
  uses link-cut trees, splay trees, lazy path structures, or other dynamic machinery.
- Heavy-light decomposition repeatedly materializes path fragments, allocates vectors, or invokes std::function callbacks
  in hot paths.
- A sorted array is searched linearly for a deterministically derived key, especially with duplicate values and n near 1e5.
- The same aggregate metadata is preserved across two implementations while only the balanced-tree mechanism changes.
- Dense boolean or relation tables dominate memory and scalar row scans; n is small enough for bit-parallel O(n^2 / word_bits)
  processing.
---

## When to use
- A DFS invokes other DFS/counting routines inside its edge loop or repeatedly rescans overlapping subtrees.
- A parent or ancestor find operation follows raw parent pointers inside a large query loop without compression or indexing.
- The result depends on both a node and operation time, so a single DSU representative is not stable across queries.
- The topology is static and queries only ask LCA, ancestry, path state, or threshold connectivity, but the implementation uses link-cut trees, splay trees, lazy path structures, or other dynamic machinery.
- Heavy-light decomposition repeatedly materializes path fragments, allocates vectors, or invokes std::function callbacks in hot paths.
- A sorted array is searched linearly for a deterministically derived key, especially with duplicate values and n near 1e5.
- The same aggregate metadata is preserved across two implementations while only the balanced-tree mechanism changes.
- Dense boolean or relation tables dominate memory and scalar row scans; n is small enough for bit-parallel O(n^2 / word_bits) processing.

## Steps
1. Write down the exact observable operation: static LCA, nearest active ancestor, threshold connectivity, component contraction, sequence split/merge, path aggregate, or derived parent lookup.
2. Separate topology from changing state. Build static child/adjacency lists once and avoid recomputing structural relationships per query.
3. Choose the narrowest matching primitive: binary lifting or Euler/RMQ for static LCA; DFS-path plus segment tree for time-dependent ancestor state; DSU plus small-to-large adjacency merging for monotone contraction; link-cut trees only for genuine dynamic
4. For deterministic parent discovery, store sorted records as `(key, original_id)`, compute the target key from maintained metadata, and use lower_bound or an indexed map instead of suffix scans.
5. For repeated subtree counts or threshold predicates, precompute parent, depth, subtree sizes, representative ancestors, and transition metadata in one traversal; process label/time buckets offline and reuse DSU or range structures.
6. For static LCA, compute entry/exit times and the binary-lifting table, short-circuit ancestor cases, then lift from the highest power downward.
7. For time-dependent ancestor queries, bucket operations by node, traverse the original tree once with the current root-to-node path, activate events by operation index, and query a segment tree for the deepest valid path position.
8. For static threshold connectivity, run global shortest-path preprocessing if needed, sort edges by their monotone key, build a Kruskal reconstruction tree during DSU merges, and answer queries using LCA/RMQ.

## Complexity
- Time: (pattern dependent)
- Space: Usually O(n log n + q) for binary lifting or event-indexed structures, O(n + q) for basic offline traversal and DSU methods, O(n log n) for reconstruction-tree lifting, and O(n^2 / w) bits for packed dense relations. Pointer-heavy

## Pitfalls
- Replacing a linear scan with a map without preserving sorted-order semantics, duplicate-key behavior, or original vertex identity.
- Using lower_bound on values while forgetting to verify exact equality or to handle multiple equal descriptors correctly.
- Applying DSU path compression to a structure whose parent relation changes by cuts or whose answer depends on query time.
- Using link-cut or splay machinery for static LCA, thereby paying pointer chasing, rotations, lazy propagation, and metadata costs for unused capabilities.
- Using plain HLD when a path operation is genuinely dynamic, or replacing HLD with link-cut trees when the tree is static and only LCA is needed.
- Failing to update all inverse maps and aggregates after swaps, rotations, joins, cuts, or component representative changes.
- Forgetting to deactivate path-local events when DFS backtracks, causing marks from sibling subtrees to leak into queries.
- Assuming one final traversal is enough when updates require online answers, or performing a full traversal after every query.

## When not to use
- Do not replace a real dynamic forest when arbitrary link, cut, reroot, or path aggregate updates are required online.
- Do not use offline processing when answers must be produced online and future operations cannot be read or reordered.
- Do not use binary lifting or static RMQ if the topology changes.
- Do not use DSU contraction when components can split, edges must be selectively removed, or path-local information is required.
- Do not use splay trees merely for theoretical amortized bounds when a static array, Fenwick tree, segment tree, or simpler indexed sequence structure suffices.
- Do not add offline buckets and segment trees when a single linear tree DP or prefix accumulation already answers all outputs.

## Minimal example
Before:
```cpp
int lca(int u, int v) {
    while (depth[u] > depth[v]) u = parent[u];
    while (depth[v] > depth[u]) v = parent[v];
    while (u != v) u = parent[u], v = parent[v];
    return u;
}
```
After:
```cpp
constexpr int LOG = 17;
int up[LOG][N]; // built once by DFS: up[0][v]=parent[v], up[k][v]=up[k-1][up[k-1][v]]
int lca(int u, int v) {
    if (depth[u] < depth[v]) swap(u, v);
    for (int k = 0; k < LOG; ++k) if ((depth[u] - depth[v]) >> k & 1) u = up[k][u];
    if (u == v) return u;
    for (int k = LOG - 1; k >= 0; --k) if (up[k][u] != up[k][v]) u = up[k][u], v = up[k][v];
    return up[0][u];
}
```
