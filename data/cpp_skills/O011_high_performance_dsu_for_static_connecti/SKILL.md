---
skill_id: O011
type: operator
language: cpp
family: graph
name: High Performance DSU for Static Connectivity and Component Aggregation
description: 'Use a compact, rank/size-balanced Union-Find with path compression whenever operations consist of bulk undirected
  unions, connectivity checks, component sizes, or component-local aggregation. Build connectivity without expanding redundant
  cliques: union all members of each incidence bucket to one representative. After unions, compress roots once and replace
  global sorting or repeated graph searches with bucketed'
tags:
- disjoint-set-union
- union-find
- connected-components
- graph-connectivity
- offline-processing
- component-counting
- bucket-counting
- incidence-graph
- path-compression
- union-by-size
triggers:
- A find routine walks parent links but does not assign the compressed root back to the parent array.
- A DSU stores component sizes or ranks but does not use them to choose the surviving root.
- A union operation calls Same or find and then recomputes the same roots for size updates or parent assignment.
- An undirected edge is processed twice with unite(u, v) and unite(v, u).
- Component size is queried through a function that performs another find after the caller already has the root.
- Connectivity is built by generating every pair inside a shared-label bucket.
- A static graph is searched separately for many connectivity queries after all edges are known.
- A full sort of component-root tuples is used only to count equal keys.
---

## When to use
- A find routine walks parent links but does not assign the compressed root back to the parent array.
- A DSU stores component sizes or ranks but does not use them to choose the surviving root.
- A union operation calls Same or find and then recomputes the same roots for size updates or parent assignment.
- An undirected edge is processed twice with unite(u, v) and unite(v, u).
- Component size is queried through a function that performs another find after the caller already has the root.
- Connectivity is built by generating every pair inside a shared-label bucket.
- A static graph is searched separately for many connectivity queries after all edges are known.
- A full sort of component-root tuples is used only to count equal keys.

## Steps
1. Represent DSU state with flat arrays: parent plus size or rank; initialize parent[i] = i.
2. Implement find with path compression, preferably iteratively for stack safety in tight loops.
3. In unite, compute both roots exactly once, return if equal, and attach the smaller tree under the larger tree; update size only at the surviving root.
4. Cache roots in callers and allow unite to accept known roots or return the new root.
5. For static connectivity, process each undirected edge once and either maintain a live component count/max size or compress roots in one final pass.
6. For shared-label or hyperedge connectivity, store entities per label and union every member with the first member; never materialize all pairwise edges.
7. For two independent partitions, compress both roots, bucket vertices by one root, and count occurrences of the other root locally with reusable stamp and count arrays.
8. Replace sort-and-run-length grouping with direct bucket counting when only frequencies are required; preserve original indices for output.

## Complexity
- Time: Standard DSU operations take amortized O(alpha(n)) each with path compression and union by size/rank, for O((n + m + q) alpha(n)) total over unions and queries. Incidence-bucket construction costs O(I alpha(n)), where I is total
- Space: Flat DSU uses O(n) space. Incidence buckets or adjacency lists require O(n + m) or O(n + I) space. Bucketed pair counting uses O(n) auxiliary arrays; merge-forest DP uses O(n + m) space.

## Pitfalls
- Writing return x = find(parent[x]) instead of parent[x] = find(parent[x]), which disables path compression.
- Updating the rank or size of the child after attaching it instead of the new root.
- Calling find through Same, size, and unite repeatedly for the same endpoints.
- Counting components by stale parent values without calling find, or relying on incidental parent shape instead of maintaining a component counter.
- Generating a clique for every shared label, causing quadratic work in large buckets.
- Using a global sort when the task only needs equal-key frequencies and one DSU partition already supplies natural buckets.
- Using std::map or nested sets in hot counting loops when integer-root arrays with stamps suffice.
- Mixing graph semantics with a different bipartite or transitive relation and accidentally over-merging components.

## When not to use
- Do not use DSU when edges are deleted or connectivity must be maintained dynamically without an appropriate rollback or dynamic-connectivity structure.
- Do not use plain DSU when queries require shortest paths, traversal order, explicit paths, or other graph structure beyond equivalence classes.
- Prefer iterative DFS/BFS component labeling for a static graph when component IDs and adjacency traversal are needed and storing the graph is acceptable.
- Do not replace weighted DSU with ordinary DSU when constraints encode relative potentials or difference equations.
- Do not use local frequency counting unless the desired key is exactly the combination of component representatives being counted.
- Do not build a merge forest if intermediate union-time answers are required and cannot be reconstructed from the final structure.

## Minimal example
Before:
```cpp
vector<int> p(n), black(n), white(n);
iota(p.begin(), p.end(), 0);
function<int(int)> find = [&](int x){ while (p[x] != x) x = p[x]; return x; };
for (auto [u, v] : edges) { int a = find(u), b = find(v); if (a != b) p[b] = a; }
long long answer = 0; for (int i = 0; i < n; ++i) if (find(i) == i) answer += 1LL * black[i] * white[i];
```
After:
```cpp
vector<int> p(n), sz(n, 1), black(n), white(n);
iota(p.begin(), p.end(), 0);
auto find = [&](int x) { while (p[x] != x) x = p[x] = p[p[x]]; return x; };
for (auto [u, v] : edges) { int a = find(u), b = find(v); if (a == b) continue; if (sz[a] < sz[b]) swap(a, b); p[b] = a; sz[a] += sz[b]; black[a] += black[b]; white[a] += white[b]; }
long long answer = 0; for (int i = 0; i < n; ++i) if (find(i) == i) answer += 1LL * black[i] * white[i];
```
