---
skill_id: O005
type: operator
language: cpp
family: graph
name: Choose the Right Shortest Path Engine and Engineer the Hot Path
description: 'A reusable optimization skill for graph, grid, and implicit-state shortest-path code. First match the algorithm
  to edge semantics and query structure: use BFS for unit weights, 0-1 BFS only for weights exactly 0 and 1, Dijkstra for
  nonnegative weights, Bellman-Ford when negative edges or destination-relevant negative cycles are possible, and reversed
  single-source search when many queries share one target. Avoid'
tags:
- graph
- shortest_path
- bfs
- 0-1_bfs
- dijkstra
- bellman_ford
- floyd_warshall
- grid
- implicit_graph
- state_expansion
triggers:
- The implementation uses Dijkstra although transformed costs may be negative or unbounded improvement must be detected.
- A deque-based shortest-path traversal is used with weights other than exactly 0 and 1, or 0-1 BFS is available but generic
  Dijkstra is used.
- Floyd-Warshall computes every pair although the consumer reads only one target column or a small set of source/target distances.
- A shortest-path routine is called repeatedly from many cells or nodes on the same static graph.
- A priority queue contains duplicate states without a stale-entry check after pop.
- A custom linked queue, per-node allocation, nested vectors, VLAs, or pair-heavy state storage appears in a large BFS/grid
  hot path.
- A directional grid BFS rescans already reached corridors instead of stopping on a strictly better distance, equal-layer
  barrier, wall, or boundary.
- A state-space search repeatedly scans all resources when only set bits of a mask remain relevant.
---

## When to use
- The implementation uses Dijkstra although transformed costs may be negative or unbounded improvement must be detected.
- A deque-based shortest-path traversal is used with weights other than exactly 0 and 1, or 0-1 BFS is available but generic Dijkstra is used.
- Floyd-Warshall computes every pair although the consumer reads only one target column or a small set of source/target distances.
- A shortest-path routine is called repeatedly from many cells or nodes on the same static graph.
- A priority queue contains duplicate states without a stale-entry check after pop.
- A custom linked queue, per-node allocation, nested vectors, VLAs, or pair-heavy state storage appears in a large BFS/grid hot path.
- A directional grid BFS rescans already reached corridors instead of stopping on a strictly better distance, equal-layer barrier, wall, or boundary.
- A state-space search repeatedly scans all resources when only set bits of a mask remain relevant.

## Steps
1. Identify the actual state graph, including residue, mask, ticket, layer, or other augmented dimensions; estimate its state count rather than treating the original graph size as the whole problem.
2. Classify edge weights and required semantics: BFS for unit edges, 0-1 BFS for exactly binary weights, Dijkstra for nonnegative weights, Bellman-Ford for negative weights or negative-cycle influence, and Floyd-Warshall only for genuinely small dense APSP.
3. If maximizing rewards, sign-transform carefully and explicitly account for reachable negative cycles that can influence the destination.
4. If only distances to one target are queried, reverse directed edges and run one source search from that target. If a few terminals are involved, use forward and reverse Dijkstra runs instead of APSP.
5. For shortest-path counting, maintain distance and count together during relaxation; use two terminal searches and retain original edges for final vertex or edge classification.
6. Use stale-entry pruning immediately after every heap or deque pop, for example `if (d != dist[u]) continue;` or `if (d > dist[u]) continue;`.
7. Exploit early termination: stop BFS when the target state is dequeued, or Dijkstra when the target is popped with minimum distance.
8. For modulo or layered BFS, encode `(node, state)` compactly and use contiguous distance arrays. For bitmask searches, iterate set bits when the resource dimension is nontrivial.

## Complexity
- Time: Select by structure: BFS or 0-1 BFS is O(V + E); Dijkstra with a binary heap is O((V + E) log V); Bellman-Ford is O(VE) plus any destination-reachability propagation; Floyd-Warshall is O(V^3); dense array-based Dijkstra is O(V^2)
- Space: (pattern dependent)

## Pitfalls
- Choosing a faster-looking but mathematically invalid algorithm, especially Dijkstra with negative edges or a deque traversal with arbitrary weights.
- Calling a traversal correct because it eventually relaxes states while allowing unrestricted duplicate expansion; missing stale checks can cause severe constant-factor blowups.
- Replacing 0-1 BFS with Dijkstra merely for implementation simplicity and accidentally adding a logarithmic factor to a linear-time problem.
- Computing APSP when the final expression consumes only one column, a few terminal distances, or a single-source aggregate.
- Using `memset(array, 1, )` and assuming it stores integer one, or using an INF sentinel too small for path sums.
- Forgetting `dist[i][i] = 0`, failing to guard INF plus INF, or using a matrix smaller than input vertex ids.
- Indexing a special grid value such as -1 directly into a distance array.
- Using non-standard variable-length arrays on the stack for large grids or state tables.

## When not to use
- Do not replace a correct algorithm solely for constant factors when the input is small and the optimization increases proof or bug risk.
- Do not use 0-1 BFS unless every transition weight is exactly 0 or 1.
- Do not use Dijkstra when negative edges, negative-cycle effects, or nonstandard relaxation semantics are possible.
- Do not replace Floyd-Warshall when arbitrary all-pairs answers are required and the vertex count is genuinely small or the graph is dense.
- Do not use dense O(V^2) Dijkstra on a sparse graph where heap-based adjacency-list Dijkstra is clearly cheaper.
- Do not use a diameter-style BFS reduction or aggressive equal-distance pruning without a movement-specific correctness proof.

## Minimal example
Before:
```cpp
vector<int> d(n, INT_MAX); priority_queue<pair<int,int>, vector<pair<int,int>>, greater<>> pq;
d[0] = 0; pq.push({0, 0});
while (!pq.empty()) { auto [du, u] = pq.top(); pq.pop(); if (du != d[u]) continue;
  for (int v : graph[u]) if (d[v] > du + 1) d[v] = du + 1, pq.push({d[v], v}); }
```
After:
```cpp
vector<int> d(n, -1), q(n); int head = 0, tail = 0;
d[0] = 0; q[tail++] = 0;
while (head < tail) { int u = q[head++];
  for (int v : graph[u]) if (d[v] < 0) d[v] = d[u] + 1, q[tail++] = v; }
```
