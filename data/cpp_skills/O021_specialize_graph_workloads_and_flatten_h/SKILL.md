---
skill_id: O021
type: operator
language: cpp
family: graph
name: Specialize Graph Workloads and Flatten Hot Path State
description: Optimize C++ graph code by first matching the algorithm to the exact predicate, then using the lightest representation
  that preserves required behavior. Replace general shortest-path or bounded-search machinery when the task is only a fixed-hop
  existence, neighborhood intersection, degree, parity, or streaming edge predicate. For genuinely general traversal, use
  one-pass BFS/DFS with persistent progress, explicit
tags:
- graph
- bfs
- dfs
- shortest-path
- reachability
- two-hop-detection
- adjacency-list
- set-intersection
- coordinate-compression
- data-oriented-design
triggers:
- Dijkstra is used although all edge weights are equal and only reachability or a small distance threshold is required.
- Acceptance depends only on a fixed-hop witness, such as a common neighbor of two terminals.
- Edges can be processed independently and the result is a count, parity, degree predicate, or endpoint-local condition.
- A helper repeatedly scans an adjacency list from its head for the same vertex.
- A search uses visited-only state but lacks dist[], best-label, or dominance checks.
- A separate visited array duplicates information already encoded by parent, distance, or answer sentinels.
- Maps, sets, coordinate pairs, or dynamic neighbor discovery occur in a fixed-degree graph hot path.
- A sparse adjacency list is accompanied by dense V×V auxiliary state.
---

## When to use
- Dijkstra is used although all edge weights are equal and only reachability or a small distance threshold is required.
- Acceptance depends only on a fixed-hop witness, such as a common neighbor of two terminals.
- Edges can be processed independently and the result is a count, parity, degree predicate, or endpoint-local condition.
- A helper repeatedly scans an adjacency list from its head for the same vertex.
- A search uses visited-only state but lacks dist[], best-label, or dominance checks.
- A separate visited array duplicates information already encoded by parent, distance, or answer sentinels.
- Maps, sets, coordinate pairs, or dynamic neighbor discovery occur in a fixed-degree graph hot path.
- A sparse adjacency list is accompanied by dense V×V auxiliary state.

## Steps
1. Write the acceptance predicate mathematically before optimizing; identify whether it is streaming, local, fixed-hop, general reachability, shortest path, or reconstruction.
2. Exploit the narrowest valid formulation. For a two-hop query, test intersection of terminal neighborhoods while reading edges instead of building a graph and running Dijkstra.
3. For edge-local predicates such as degree, parity, or neighbor-value invalidation, update flat arrays directly during input and avoid storing edges.
4. If general traversal is required, build adjacency once and traverse each adjacency entry once. Use BFS for unit weights and Dijkstra only for nonnegative varying weights.
5. Eliminate restart scans with DFS stack state, per-vertex cursors, or persistent edge indices; mark a vertex exactly once when discovered.
6. Use dist[] or best-label arrays for relaxation. Accept a state only when it improves the primary objective or its tie-break, and discard stale heap entries.
7. Compress coordinates or logical entities to integer IDs, prebuild adjacency, and replace map/set membership with arrays, byte markers, colors, or timestamps.
8. Choose storage by scale: vector<int> adjacency for simple sparse graphs, reserved vectors when degrees are known, or a flat head/to/next edge pool for maximum locality and predictable allocation.

## Complexity
- Time: Choose the narrowest valid bound: O(m) for one-pass endpoint or edge-stream predicates; O(n+m) for BFS/DFS and tree DP; approximately O((n+m) log n) for sparse nonnegative weighted shortest paths with a binary heap; O(n^3·S) or other
- Space: Use O(n) flat state for streaming and fixed-hop decisions; O(n+m) for ordinary adjacency-based traversal; O(n+m) or O(m) for flat edge pools; avoid O(n^2) auxiliary state unless n is demonstrably small and dense transitions are beneficial.

## Pitfalls
- Applying a specialized two-hop detector when the task actually asks for arbitrary reachability, exact distances, directed semantics, or longer paths.
- Ignoring reversed endpoint order in undirected edges.
- Using visited-only Dijkstra or first-pop finalization without a distance/best-label guard, causing duplicate inferior heap states.
- Treating a zero distance or parent value as unvisited when it is a valid source state.
- Rebuilding or rescanning adjacency from the beginning instead of retaining traversal progress.
- Assuming a linked adjacency structure is faster despite per-edge allocation and pointer chasing.
- Allocating dense V×V state for a sparse graph.
- Using map/set in a fixed-index hot path without a genuine ordering or dynamic-key requirement.

## When not to use
- Do not specialize away the graph when queries require arbitrary source-target reachability, exact shortest paths, path reconstruction, dynamic updates, or multiple future queries.
- Do not replace a correct streaming pass with adjacency construction merely to resemble a reference implementation.
- Do not use dense matrices or precomputed transition tables when n is large or the graph is sparse.
- Do not use flat custom edge pools when implementation complexity, dynamic mutation, or maintainability outweighs modest constant-factor gains.
- Do not remove a separate visited array if parent, distance, or answer values can legitimately equal the chosen unvisited sentinel.
- Do not rely on recursive traversal when stack depth may approach the vertex count.

## Minimal example
Before:
```cpp
bool reachable(const Graph& g, int s, int t) {
    std::unordered_set<int> seen; std::vector<int> work{ s };
    while (!work.empty()) { int v = work.back(); work.pop_back(); if (v == t) return true; if (seen.insert(v).second) for (int n : g[v]) work.push_back(n); }
    return false;
}
```
After:
```cpp
bool reachable(const Graph& g, int s, int t) {
    std::vector<char> seen(g.size()); std::vector<int> work{ s }; seen[s] = 1;
    while (!work.empty()) { int v = work.back(); work.pop_back(); if (v == t) return true; for (int n : g[v]) if (!seen[n]) seen[n] = 1, work.push_back(n); }
    return false;
}
```
