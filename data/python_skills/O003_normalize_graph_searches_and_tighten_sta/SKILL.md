---
skill_id: O003
type: operator
language: python
family: graph
name: Normalize Graph Searches and Tighten State Space Kernels
description: Optimize graph-heavy Python solutions by first matching the algorithm to the graph structure, then minimizing
  hot-loop overhead. Replace implicit layered searches with explicit shortest-path models such as BFS, 0-1 BFS, Dijkstra,
  or monotone relaxation; use dense all-pairs methods when the vertex set is small; and represent bounded expanded states
  with compact arrays and implicit transitions. Preserve brute force
tags:
- graph
- shortest-path
- dijkstra
- 0-1-bfs
- floyd-warshall
- all-pairs-shortest-path
- state-space-search
- resource-constrained-path
- modular-state-graph
- transitive-closure
triggers:
- A heap-based shortest-path implementation expands the same vertex or state after its heap entry has become obsolete.
- The state is a pair such as (vertex, bounded resource), and the resource range has a provable small cap.
- Transitions are generated eagerly for every expanded state even though only a few implicit moves are needed when a state
  is popped.
- The search uses a list queue with pop(0), repeated frontier rebuilding, or closure expansion under a free operation.
- All edge costs are 0 or 1, or the objective is the minimum number of expensive operations.
- The state naturally consists of residues modulo a small integer.
- A small graph is processed by many repeated Dijkstra or BFS runs, or a pure-Python triple-loop APSP dominates runtime.
- The required result depends on exact distances between every pair or between a small set of distinguished vertices.
---

## When to use
- A heap-based shortest-path implementation expands the same vertex or state after its heap entry has become obsolete.
- The state is a pair such as (vertex, bounded resource), and the resource range has a provable small cap.
- Transitions are generated eagerly for every expanded state even though only a few implicit moves are needed when a state is popped.
- The search uses a list queue with pop(0), repeated frontier rebuilding, or closure expansion under a free operation.
- All edge costs are 0 or 1, or the objective is the minimum number of expensive operations.
- The state naturally consists of residues modulo a small integer.
- A small graph is processed by many repeated Dijkstra or BFS runs, or a pure-Python triple-loop APSP dominates runtime.
- The required result depends on exact distances between every pair or between a small set of distinguished vertices.

## Steps
1. Identify the true state graph: vertices, implicit transitions, edge costs, resource dimensions, and terminal conditions.
2. Choose the simplest valid engine: ordinary BFS for unit costs, 0-1 BFS for binary costs, Dijkstra for nonnegative arbitrary costs, monotone worklist relaxation when states shrink and best-cost memoization is sufficient, or Floyd-Warshall/transitive closure
3. For modulo problems, use residues as states and encode each operation as an explicit edge with its actual cost. Maintain one distance per residue and use a deque for 0-1 BFS.
4. For heap-based searches, store the popped distance and immediately skip entries whose key is greater than the current recorded distance. Prefer lazy duplicate handling over a separate visited table.
5. Replace adjacency dictionaries and edge-ID lookups in hot loops with list-based adjacency containing complete edge tuples.
6. For monotone integer-state optimization, store best known cost per state, prune states against both best[state] and the current answer, and omit transitions that cannot improve the state.
7. For small dense graphs, initialize a distance matrix with zero diagonals, run APSP once, and classify original edges or answer queries from the resulting matrix rather than reconstructing arbitrary shortest-path trees.
8. When only a small subset of vertices matters, precompute distances between that subset and use direct matrix indexing; retain permutation enumeration only when the subset size makes factorial work acceptable.

## Complexity
- Time: Typical optimized bounds are O(V + E) for BFS, O(V + E) amortized for 0-1 BFS, O((V + E) log V) for guarded Dijkstra, and O((N + M)R log(NR)) for bounded resource-state Dijkstra with R resource levels. Dense APSP or transitive closure
- Space: Use O(V), O(N), or O(HW) for ordinary graph and grid searches; O(NR) for bounded resource-state searches; O(N^2) for dense APSP or transitive closure; and O(K) auxiliary space for lazy permutation enumeration. Prefer flat numeric arrays

## Pitfalls
- Using Dijkstra without nonnegative edge costs.
- Using 0-1 BFS when an edge cost is outside {0, 1}.
- Returning the raw shortest-path distance when the initial digit, action, or mandatory starting resource has a separate cost.
- Choosing a resource cap from a heuristic constant without proving that larger resource values are dominated.
- Using a visited set instead of best-cost memoization when a state can be reached with different costs.
- Expanding a state after a stale heap or deque entry has already been superseded.
- Adding redundant upward, refill, or self-worsening transitions, especially when a remainder is zero or the resource is already capped.
- Building the full expanded state graph when transitions can be generated implicitly.

## When not to use
- Do not use dense matrices or Floyd-Warshall when the graph is large, sparse, or only a few source-target distances are needed.
- Do not use 0-1 BFS unless all transition costs are exactly 0 or 1.
- Do not replace Dijkstra with FIFO relaxation unless state transitions are monotone enough that best-cost memoization guarantees practical or proven convergence.
- Do not cap a resource dimension without a rigorous dominance or shortest-simple-path argument.
- Do not preserve factorial enumeration when the relevant subset can grow beyond a very small bound; use subset DP, meet-in-the-middle, or a problem-specific polynomial formulation.
- Do not offload APSP to an external numerical library when dependencies are unavailable, input sizes are tiny, or conversion overhead dominates.

## Minimal example
Before:
```py
def shortest_path(graph, source, target):
    dist = {source: 0}; heap = [(0, source)]
    while heap:
        cost, node = heapq.heappop(heap)
        for nxt, weight in graph[node]:
            if cost + weight < dist.get(nxt, float("inf")):
                dist[nxt] = cost + weight; heapq.heappush(heap, (dist[nxt], nxt))
    return dist.get(target, float("inf"))
```
After:
```py
def shortest_path(graph, source, target):
    dist = {source: 0}; heap = [(0, source)]
    while heap:
        cost, node = heapq.heappop(heap)
        if cost != dist[node]: continue
        if node == target: return cost
        for nxt, weight in graph[node]:
            new_cost = cost + weight
            if new_cost < dist.get(nxt, float("inf")):
                dist[nxt] = new_cost; heapq.heappush(heap, (new_cost, nxt))
    return float("inf")
```
