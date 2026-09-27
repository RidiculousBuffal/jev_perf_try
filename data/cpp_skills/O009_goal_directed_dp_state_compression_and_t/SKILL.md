---
skill_id: O009
type: operator
language: cpp
family: dp
name: Goal Directed DP State Compression and Transition Optimization
description: 'A reusable optimization pattern for C++ dynamic programs: first identify the exact information required by future
  transitions and the final query, then reformulate the state around that information instead of enumerating historical identities,
  redundant dimensions, or unreachable values. Typical reductions include replacing predecessor-index states with elapsed
  distance or accumulated score, converting reachability'
tags:
- dynamic_programming
- state_compression
- rolling_array
- memoization
- transition_optimization
- bounded_knapsack
- unbounded_knapsack
- prefix_sums
- reachability
- game_dp
triggers:
- A DP state stores an index, split point, or last-action identity that affects the future only through distance, sum, count,
  wealth, or another derived quantity.
- Each layer depends only on the immediately previous layer, but the implementation retains the full table or updates one
  layer in place.
- A boolean reachable array duplicates information already represented by an INF or negative-infinity DP value.
- The program computes every state although only one target state or a narrow reachable subgraph is queried.
- Transitions scan all previous states except a small forbidden set, or repeatedly recompute the same aggregate.
- A fixed global bound is known, but the implementation sizes work by a dynamically growing answer or repeatedly allocates
  tables.
- A cleanup phase, repeated sorting, or reconstruction after selection suggests that the decision process can be encoded directly
  as transitions.
- A recurrence contains a small fixed state dimension, such as player turn, carry, activity, or machine mode.
---

## When to use
- A DP state stores an index, split point, or last-action identity that affects the future only through distance, sum, count, wealth, or another derived quantity.
- Each layer depends only on the immediately previous layer, but the implementation retains the full table or updates one layer in place.
- A boolean reachable array duplicates information already represented by an INF or negative-infinity DP value.
- The program computes every state although only one target state or a narrow reachable subgraph is queried.
- Transitions scan all previous states except a small forbidden set, or repeatedly recompute the same aggregate.
- A fixed global bound is known, but the implementation sizes work by a dynamically growing answer or repeatedly allocates tables.
- A cleanup phase, repeated sorting, or reconstruction after selection suggests that the decision process can be encoded directly as transitions.
- A recurrence contains a small fixed state dimension, such as player turn, carry, activity, or machine mode.

## Steps
1. Write the semantic definition of every DP dimension and list exactly which components future transitions read.
2. Remove dimensions that encode redundant symmetry, such as player identity in an impartial game, or replace historical identities with the derived quantity that determines future cost.
3. Choose a direction that matches the query: use top-down memoization for one or sparse target states, or bottom-up DP for dense layers and predictable memory access.
4. Use explicit sentinels: INF for unreachable minimization states, negative infinity for impossible maximization states, and -1 or a separate marker for uncomputed memo states.
5. If only one previous layer is needed, use rolling buffers; if transitions are 0/1, iterate capacities backward; if transitions are logically previous-layer-only, never mix old and new values in place.
6. Collapse redundant transition work algebraically: maintain a layer sum, prefix/suffix aggregate, monotone frontier, or precomputed segment cost instead of rescanning all predecessors.
7. Move feasibility checks out of the hot loop when safe: bound loop indices directly, retain partial states when they may help later, and update the answer online when possible.
8. For grouped choices, enumerate the meaningful multiplicity once per group and include bonuses, resets, skips, or discard costs directly in the transition.

## Complexity
- Time: (pattern dependent)
- Space: Use O(States) with rolling arrays for previous-layer recurrences, O(number_of_visited_states) for sparse top-down memoization, or O(Layers * States) only when reconstruction or cross-layer access requires it. Scalar or invariant

## Pitfalls
- Changing a state definition without proving that discarded history cannot affect any future transition.
- Using in-place updates when the recurrence requires the previous layer, causing newly written states to be reused in the same iteration.
- Iterating in the wrong direction and accidentally turning 0/1 knapsack into unbounded knapsack.
- Conflating unreachable, zero-valued, losing, and uncomputed states through default initialization or a boolean memo table.
- Pruning overweight or otherwise temporarily infeasible intermediate states when they may become useful after later transitions.
- Removing a dimension that is needed for reconstruction, multiplicity, parity, or a terminal condition.
- Assuming a fixed bound is safe without proving that every reachable state stays within it; conversely, scanning a large fixed bound when a tight bound is cheap and materially smaller.
- Replacing a full predecessor scan with an aggregate formula without accounting for excluded states, duplicate values, modular arithmetic, or overflow.

## When not to use
- The removed history genuinely changes future legal moves, costs, or feasibility.
- The state bound is too large for pseudo-polynomial indexing and no sparsity or coordinate compression is available.
- The query requires all intermediate states, many reconstructions, or full path-count information that rolling or goal-directed evaluation would discard.
- The transition lacks the algebraic structure needed for aggregation, prefix sums, monotone frontiers, or dominance pruning.
- The reachable state space is dense and the target query touches nearly every state, making memoization overhead worse than a cache-friendly bottom-up sweep.
- A greedy or scalar recurrence has no proof of dominance or optimal substructure beyond the current value.

## Minimal example
Before:
```cpp
// O009 focus: goal
vector<vector<int>> dp(n + 1, vector<int>(W + 1, 0));
for (int i = 1; i <= n; ++i)
  for (int w = 0; w <= W; ++w)
    dp[i][w] = max(dp[i - 1][w], w >= wt[i] ? dp[i - 1][w - wt[i]] + val[i] : 0);
```
After:
```cpp
// optimized for goal
vector<int> dp(W + 1, 0);
for (int i = 1; i <= n; ++i)
  for (int w = W; w >= wt[i]; --w)
    dp[w] = max(dp[w], dp[w - wt[i]] + val[i]);
```
