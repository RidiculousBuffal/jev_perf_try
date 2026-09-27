---
skill_id: O018
type: operator
language: cpp
family: graph
name: Direct Graph Invariant and Residual Flow Reformulation
description: Reusable optimization pattern distilled from weighted traces.
tags:
- graph-reduction
- max-flow
- min-cut
- Dinic
- bipartite-matching
- bipartite-coloring
- parity
- dfs
- bfs
- tree-dp
triggers:
- A solution builds a spanning forest with DSU and later traverses or checks deferred edges, although the final result only
  needs connectivity, parity, bipartiteness, or component counts.
- A parity-DSU uses doubled vertices for a static graph whose only required property is one-time 2-coloring.
- A recursive DFS, pointer-heavy adjacency structure, repeated full-array clearing, or fixed edge pool is used at input sizes
  near 1e5 or larger.
- A matching routine repeatedly starts DFS augmentations from left vertices and rescans dense or already-failed adjacency.
- Dependencies form a closure or partial order, such as choosing an item forcing choices on related items, and the objective
  is additive.
- The objective is a weighted subset under implication or closure constraints, suggesting maximum closure and an s-t min-cut.
- A solver tracks only intervals, global parity flags, or heuristic conflicts but must output concrete values satisfying exact
  edge relations.
- Binary choices or endpoint selections create pairwise incompatibilities under a threshold, suggesting an implication graph
  checked inside binary search.
---

## When to use
- A solution builds a spanning forest with DSU and later traverses or checks deferred edges, although the final result only needs connectivity, parity, bipartiteness, or component counts.
- A parity-DSU uses doubled vertices for a static graph whose only required property is one-time 2-coloring.
- A recursive DFS, pointer-heavy adjacency structure, repeated full-array clearing, or fixed edge pool is used at input sizes near 1e5 or larger.
- A matching routine repeatedly starts DFS augmentations from left vertices and rescans dense or already-failed adjacency.
- Dependencies form a closure or partial order, such as choosing an item forcing choices on related items, and the objective is additive.
- The objective is a weighted subset under implication or closure constraints, suggesting maximum closure and an s-t min-cut.
- A solver tracks only intervals, global parity flags, or heuristic conflicts but must output concrete values satisfying exact edge relations.
- Binary choices or endpoint selections create pairwise incompatibilities under a threshold, suggesting an implication graph checked inside binary search.

## Steps
1. Identify the minimal invariant: color/parity, xor residual, interval plus parity, implication reachability, matching, or closure membership.
2. Choose the direct representation: flat adjacency arrays or vectors for static graphs, an explicit color array for bipartiteness, and an iterative stack or queue for traversal.
3. For static parity or bipartite tasks, insert every edge directly, traverse each component once, assign alternating colors, detect conflicts immediately, and accumulate component sizes while traversing.
4. For tree constraints, perform a bottom-up postorder merge. Intersect each parent interval with [child_left - 1, child_right + 1], propagate required parity, and fail immediately on an empty or parity-incompatible interval.
5. Run a top-down constructive pass after feasibility: choose a root value, then assign each child parent - 1 or parent + 1 whenever that value lies in the child's interval. Verify all edges if output safety matters.
6. For xor interval or boundary constraints, coordinate-compress endpoints, create one labeled graph edge per query, solve each component by DFS residual propagation, and select spanning-tree edges carrying nonzero residuals.
7. For binary threshold feasibility, model each alternative as complementary literals, add implication edges for forced choices and conflicts, and check satisfiability using compact adjacency and a binary search over the answer.
8. For bipartite matching, keep the original edge predicate, split vertices into left and right partitions, add source-to-left and right-to-sink capacity-1 edges, and add capacity-1 left-to-right edges for valid pairs.

## Complexity
- Time: Typical direct traversal, tree interval propagation, or xor solving is O(V + E) after adjacency construction. Coordinate-compressed interval graph construction is commonly O(n log n + m log n), followed by O(V + E) traversal. Dinic on a
- Space: O(V + E) for adjacency, coloring, implication, or residual networks; O(V) for tree intervals, assignments, and iterative traversal state. Weighted closure over divisibility-like relations commonly has O(N log N) edges. Flat residual pairs

## Pitfalls
- Do not replace a general dynamic connectivity problem with coloring; direct traversal is appropriate only when the graph is static and queries do not require online merges.
- Do not use an arbitrary large flow capacity without proving it exceeds every possible finite cut; use a safe bound based on total finite capacity.
- Do not add closure edges in the wrong direction. An implication from selecting u to requiring v must be represented as u -> v.
- In residual flow, update the referenced edge by reference and adjust its reverse edge through the stored reverse index; iterating by value silently breaks residual state.
- Use strict versus non-strict dominance or compatibility comparisons exactly as specified when generating matching edges.
- Do not infer a concrete tree assignment from interval endpoints or compare intervals heuristically; exact difference constraints require explicit parent-child values.
- When merging intervals, check both non-emptiness and the existence of a value with the required parity.
- A recursive DFS may pass small tests but overflow on a path-shaped graph; prefer iterative DFS/BFS or explicitly validate stack safety.

## When not to use
- The graph is dynamic with online edge insertions, deletions, or parity queries; DSU or a dynamic connectivity structure may be more appropriate.
- The graph is extremely sparse and matching is small enough that a simple augmenting-path implementation is clearly within limits.
- The objective or constraints are genuinely sequential and have a valid low-dimensional DP; a graph reduction would add complexity without reducing work.
- A closure implication is not one-way or cannot be represented by a cut-safe infinite-capacity edge.
- The required output depends on paths, ordering, or structural details discarded by component classification or aggregated parity.
- The graph has capacities or costs that invalidate a unit-capacity matching interpretation and no correct flow model has been established.

## Minimal example
Before:
```cpp
int maxflow(int s,int t){
  int f=0;
  while(bfs_matrix(s,t)) for(int v=t;v!=s;v=par[v])
    for(int u=0;u<n;u++) if(cap[u][v]&&par[v]==u) cap[u][v]-=1,cap[v][u]+=1,f++;
  return f;
}
```
After:
```cpp
struct Edge{int to,rev,cap;}; vector<vector<Edge>> g;
void add(int u,int v,int c){g[u].push_back({v,(int)g[v].size(),c});g[v].push_back({u,(int)g[u].size()-1,0});}
int dfs(int u,int t,int f){if(u==t)return f; for(int &i=it[u];i<(int)g[u].size();++i){auto &e=g[u][i]; if(e.cap&&level[e.to]==level[u]+1){int x=dfs(e.to,t,min(f,e.cap)); if(x){e.cap-=x;g[e.to][e.rev].cap+=x;return x;}}} return 0;}
int maxflow(int s,int t){int ans=0; while(bfs_residual(s,t)) {it.assign(n,0); for(int x; (x=dfs(s,t,INT_MAX)); ans+=x);} return ans;}
```
