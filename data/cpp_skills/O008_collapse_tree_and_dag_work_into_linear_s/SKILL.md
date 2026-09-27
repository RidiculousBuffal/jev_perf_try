---
skill_id: O008
type: operator
language: cpp
family: graph
name: Collapse Tree and DAG Work into Linear Structural DP
description: Recognize when a recursive, repeatedly recomputed, or over-generalized tree/DAG solution is solving a smaller
  structural problem. Replace it with direct adjacency traversal, explicit dependency order, bounded state, and linear-time
  aggregation. Typical reductions include two-sweep diameter computation, iterative BFS/DFS distance labeling, specialized
  two-pass rerooting, top-two neighbor aggregation, lowlink
tags:
- C++
- competitive-programming
- tree
- tree-dp
- rerooting
- diameter
- graph
- DAG
- topological-sort
- lowlink
triggers:
- A recursive traversal handles up to roughly 100000 or more vertices and can reach linear depth.
- A tree solution uses a custom parent/child/sibling representation even though the input is naturally an undirected adjacency
  list.
- A DFS computes an aggregate and then rescans the same children for a narrow correction predicate.
- A rerooting pass sorts neighbor candidates but needs only the best and second-best values.
- A global answer is actually a tree diameter, but the code only aggregates downward branches from one root.
- Two-source logic reuses one distance array for distances, visitation, pruning, or destructive state.
- Every candidate center performs a full traversal and then a full-array threshold scan, although only a bounded radius matters.
- A subtree merge uses maps, multisets, vectors, or repeated small-to-large structures while the meaningful rank or level
  range is logarithmically bounded.
---

## When to use
- A recursive traversal handles up to roughly 100000 or more vertices and can reach linear depth.
- A tree solution uses a custom parent/child/sibling representation even though the input is naturally an undirected adjacency list.
- A DFS computes an aggregate and then rescans the same children for a narrow correction predicate.
- A rerooting pass sorts neighbor candidates but needs only the best and second-best values.
- A global answer is actually a tree diameter, but the code only aggregates downward branches from one root.
- Two-source logic reuses one distance array for distances, visitation, pruning, or destructive state.
- Every candidate center performs a full traversal and then a full-array threshold scan, although only a bounded radius matters.
- A subtree merge uses maps, multisets, vectors, or repeated small-to-large structures while the meaningful rank or level range is logarithmically bounded.

## Steps
1. Write down the exact invariant and output quantity before optimizing; reject a faster formulation that computes a different metric.
2. Normalize the graph representation: store undirected trees bidirectionally, preserve edge IDs when edge answers are required, and use flat arrays or adjacency vectors.
3. Choose an explicit traversal order. Use iterative BFS/DFS for distances and stack safety; use a parent/order array followed by reverse order for bottom-up tree DP.
4. For a global longest path in a tree, run a traversal from any node, select a farthest endpoint, then run a second traversal from that endpoint and take the maximum distance.
5. For rerooting, compute downward values once, then propagate parent-side values in a second pass. Track top one and top two neighbor contributions instead of sorting.
6. For bounded-radius objectives, count covered nodes during depth-limited traversal, stop at the radius boundary, and optimize covered count rather than repeatedly counting uncovered nodes.
7. For fixed logarithmic state, replace dynamic subtree containers with a small fixed-width array; merge each child across the bounded range and maintain a canonical compressed state.
8. For equal-signature counting, update the global pair or frequency answer online as each postorder state is produced.

## Complexity
- Time: Usually O(N) for trees and O(N + M) for graphs or DAGs after structural preprocessing. Bounded-radius candidate enumeration may remain O(N^2) in the worst case but becomes proportional to the total visited radius-limited neighborhoods
- Space: Usually O(N) for trees and O(N + M) for graphs, including adjacency, metadata, explicit traversal stacks or queues, and a constant number of DP arrays. Fixed-width states use O(KN) with small constant K.

## Pitfalls
- Changing the algorithm without proving that the new invariant matches the required output; a linear solution can still solve the wrong subproblem.
- Using a diameter shortcut when the objective is not a true tree diameter or when edge weights can violate the assumptions behind farthest-node sweeps.
- Mixing zero-based and one-based indexing, especially when traversal starts at one convention and the final scan uses another.
- Keeping recursive DFS on adversarial chains; O(n) recursion is a practical C++ stack-overflow risk.
- Reusing one array for distance, visited status, pruning, and mutable deletion; use separate arrays with explicit semantics.
- Resetting only a few entries and relying on a traversal to overwrite everything; this is fragile under disconnected inputs, refactors, or multiple test cases.
- Using int for weighted path lengths or large subtree totals.
- Sorting all neighbors or allocating a temporary vector when only top one or top two values are needed.

## When not to use
- Do not replace a correct general rerooting or dynamic-tree method when queries include updates, arbitrary exclusions, or state interactions not captured by a fixed local recurrence.
- Do not use two-sweep diameter unless the graph is a tree and the objective is exactly the weighted or unweighted diameter under valid edge-weight assumptions.
- Do not use bounded-radius enumeration when the radius is large and neighborhoods overlap enough to retain quadratic work without another decomposition.
- Do not compress state to a fixed width unless the bound is mathematically guaranteed by the constraints and recurrence.
- Do not use topological processing unless acyclicity is guaranteed or cycles are explicitly handled.
- Do not replace connectivity queries with lowlink preprocessing when the graph is dynamic or the operation is not a static single-vertex decomposition.

## Minimal example
Before:
```cpp
vector<int> sub(n);
function<int(int,int)> dfs = [&](int u,int p){ int s=a[u]; for(int v:g[u]) if(v!=p) s+=dfs(v,u); return s; };
for(int u=0;u<n;u++) sub[u]=dfs(u,-1); // Recomputes overlapping subtrees
```
After:
```cpp
vector<int> sub=a;
vector<int> order={0};
for(int i=0;i<(int)order.size();i++) for(int v:g[order[i]]) if(v!=parent[order[i]]) parent[v]=order[i],order.push_back(v);
for(int i=n-1;i>0;i--) sub[parent[order[i]]]+=sub[order[i]]; // Linear tree DP
```
