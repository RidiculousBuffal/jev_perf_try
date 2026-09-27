---
skill_id: O028
type: operator
language: python
family: graph
name: Compress Graph Connectivity and Greedy Aggregation
description: 'Replace object-heavy graph construction, repeated component relabeling, flood-fill, or expanded MST modeling
  with the smallest structure that preserves the required aggregate: DSU for streaming connectivity and component sizes, iterative
  coloring for bipartiteness, low-link DFS for edge-criticality, edge-list Kruskal for weighted spanning trees, and dimension-count
  formulas for regular repeated structures. Process'
tags:
- graph
- connectivity
- disjoint-set-union
- union-find
- connected-components
- bipartite-check
- bridge-detection
- minimum-spanning-tree
- kruskal
- grid
triggers:
- Only component membership, component count, or component size is needed after reading an undirected edge stream.
- A merge operation rewrites an entire O(V) component-label array.
- An adjacency list is built even though edges can be consumed once by DSU.
- Connectivity is tested after removing every edge.
- A graph is colored and then rescanned to detect conflicts.
- Traversal starts from one vertex although disconnected input may be possible.
- Recursive flood-fill risks recursion-depth failure.
- A grid has local fixed-size adjacency and only active cells matter.
---

## When to use
- Only component membership, component count, or component size is needed after reading an undirected edge stream.
- A merge operation rewrites an entire O(V) component-label array.
- An adjacency list is built even though edges can be consumed once by DSU.
- Connectivity is tested after removing every edge.
- A graph is colored and then rescanned to detect conflicts.
- Traversal starts from one vertex although disconnected input may be possible.
- Recursive flood-fill risks recursion-depth failure.
- A grid has local fixed-size adjacency and only active cells matter.

## Steps
1. Identify the exact required aggregate before choosing a representation: connectivity, component size, bipartite partition, critical edges, MST weight, or a separable cost total.
2. For streaming undirected connectivity, initialize DSU parent and size/rank arrays and union each edge immediately.
3. Use path compression plus union by size or rank; maintain component counts or sizes incrementally when possible.
4. For component queries, avoid adjacency construction and scan DSU roots or maintained sizes only at the end.
5. For bipartiteness, use one color array with an unvisited sentinel and iterative BFS/DFS; start a traversal for every unvisited vertex.
6. Detect same-color conflicts while traversing and maintain partition counts during the traversal instead of performing a second edge pass.
7. For edge-removal connectivity, recognize bridge detection and prefer one low-link DFS with discovery and low values; use per-edge recomputation only when constraints are small.
8. For weighted MSTs on ordinary edge lists, store each edge once, sort by weight, and apply Kruskal with DSU; stop after selecting V-1 edges when connectedness is guaranteed.

## Complexity
- Time: DSU edge streaming: O((V+E) alpha(V)); component-size queries add O(V). Iterative BFS/DFS and bipartite checking: O(V+E). Kruskal MST: O(E log E + E alpha(V)). Low-link bridge detection: O(V+E). Sparse grid DSU: O(L alpha(L)) for L active
- Space: DSU-only processing: O(V). Explicit adjacency traversal: O(V+E). Edge-list Kruskal: O(V+E). Low-link DFS: O(V+E) including adjacency and metadata. Sparse active-cell grid processing: O(L) plus optional coordinate/index maps. Compressed

## Pitfalls
- Using DSU for operations that require paths, distances, traversal order, or dynamic deletions without an appropriate offline strategy.
- Counting roots without applying find, or failing to maintain component sizes at representatives.
- Starting bipartite traversal from one vertex and silently misclassifying disconnected graphs.
- Using a bipartite product formula without accounting for all components or without subtracting existing edges correctly.
- Performing a separate conflict-validation pass after coloring when conflicts can be detected during traversal.
- Using recursive DFS on large graphs or grids in Python.
- Recomputing connectivity after every edge deletion when a low-link bridge algorithm gives a linear solution.
- Skipping a removed edge by endpoint value rather than by unique edge index when parallel edges may exist.

## When not to use
- The task needs shortest paths, actual paths, traversal order, subtree structure, or detailed adjacency queries.
- Edges are deleted online and answers are required after each deletion; use a suitable dynamic-connectivity or offline reverse-processing method instead.
- The graph is tiny and a simpler direct traversal is clearer and already within limits.
- The graph is highly dynamic with arbitrary insertions and deletions where static DSU cannot represent current state.
- The grid is dense and a well-implemented iterative flood-fill has lower overhead than DSU.
- The claimed regular cost symmetry or edge interchangeability has not been proven.

## Minimal example
Before:
```py
def largest_component(n, edges):
    graph = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v); graph[v].append(u)
    seen, best = set(), 0
    for start in range(n):
        if start not in seen:
            stack, seen = [start], seen | {start}; size = 0
            while stack:
                u = stack.pop(); size += 1
                for v in graph[u]:
                    if v not in seen: seen.add(v); stack.append(v)
            best = max(best, size)
    return best
```
After:
```py
def largest_component(n, edges):
    parent, size = list(range(n)), [1] * n
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    for u, v in edges:
        ru, rv = find(u), find(v)
        if ru != rv:
            if size[ru] < size[rv]: ru, rv = rv, ru
            parent[rv] = ru; size[ru] += size[rv]
    return max(size)
```
