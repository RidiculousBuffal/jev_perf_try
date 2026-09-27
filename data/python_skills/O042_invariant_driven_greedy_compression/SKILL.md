---
skill_id: O042
type: operator
language: python
family: graph
name: Invariant Driven Greedy Compression
description: Replace value-dependent simulation, repeated mutation, dynamic programming, or edge-by-edge greedy actions with
  a direct scan based on the smallest sufficient invariant. Look for contributions that decompose into positive adjacent rises,
  local extrema, consecutive relevant positions, or a scalar carried state. The resulting algorithm should count boundary
  events or process only structurally meaningful transitions
tags:
- greedy
- simulation-to-formula
- difference-scan
- adjacent-differences
- local-extrema
- state-compression
- run-length-counting
- fixed-points
- single-pass
- constant-space
triggers:
- A while-loop or nested scan repeats until values reach zero or a target state.
- Runtime depends on numeric magnitudes, heights, rounds, or unit operations rather than only input length.
- The simulation repeatedly decrements contiguous positive ranges or counts segments at successive levels.
- The answer depends primarily on transitions between neighboring values rather than intermediate array contents.
- A new operation begins when the current value exceeds the previous value.
- A process reacts to every profitable adjacent increase even though monotone stretches can be grouped into valley-to-peak
  segments.
- Only local extrema, fixed points, or consecutive relevant positions affect the result.
- A mutation or swap affects only adjacent positions and the final outcome depends on runs of relevant indices.
---

## When to use
- A while-loop or nested scan repeats until values reach zero or a target state.
- Runtime depends on numeric magnitudes, heights, rounds, or unit operations rather than only input length.
- The simulation repeatedly decrements contiguous positive ranges or counts segments at successive levels.
- The answer depends primarily on transitions between neighboring values rather than intermediate array contents.
- A new operation begins when the current value exceeds the previous value.
- A process reacts to every profitable adjacent increase even though monotone stretches can be grouped into valley-to-peak segments.
- Only local extrema, fixed points, or consecutive relevant positions affect the result.
- A mutation or swap affects only adjacent positions and the final outcome depends on runs of relevant indices.

## Steps
1. Identify what one simulated operation represents: a horizontal layer, a segment start, an adjacent gain, a local exchange, or a retained amount.
2. Find the minimal structural event that creates a new contribution, usually a positive rise, a turning point, a relevant fixed position, or a local feasibility boundary.
3. Replace a virtual baseline of zero when appropriate, so the first element contributes directly.
4. For height or segment-layer processes, compute the total as the first value plus every positive adjacent increase: a[0] + sum(max(0, a[i] - a[i-1])).
5. For monotone gain processes, collapse each nondecreasing run into one action at its valley and one action at its peak; handle final liquidation or the final boundary explicitly.
6. For adjacent local constraints, carry only the previous effective or surviving value and update it greedily instead of storing pairwise intermediate results.
7. For fixed-point or adjacency-based operations, collect or stream relevant positions, partition them into maximal consecutive runs, and count each run using the local pairing rule, such as ceil(length / 2).
8. Use exact tie-breaking and lookahead only where ambiguity is proven to matter; avoid broad heuristics.

## Complexity
- Time: Typically O(n) time. This removes dependence on height, total value, number of simulation rounds, interval enumeration, or repeated mutation. Local-extrema and run-counting variants remain linear, even when their main benefit is reasoning
- Space: Prefer O(1) auxiliary space by streaming the input and retaining only previous state, cash/holdings, or current run length. O(k) space is acceptable when storing sparse relevant positions is materially simpler; avoid O(n) temporary arrays

## Pitfalls
- Applying the positive-difference formula when operations are not contiguous, layered, or additive by boundary starts.
- Assuming adjacent rises can always be traded independently when fees, transaction limits, holding constraints, or other coupling exists.
- Ignoring plateaus, equal neighboring values, endpoint extrema, or the need to liquidate at the final position.
- Using local extrema without proving that intermediate trades and boundary choices are equivalent.
- Compressing state too aggressively and losing information needed for future feasibility or tie-breaking.
- Using one-step lookahead as an unproven heuristic rather than deriving the exact ambiguous-state rule.
- Accessing the first element without handling empty input.
- Materializing temporary arrays or lists when only a running previous value is required.

## When not to use
- The operation affects nonlocal elements or the answer depends on interactions beyond the retained local state.
- Intermediate states influence future choices in a way that cannot be summarized by a proven invariant.
- Costs, capacities, transaction limits, fees, or parity constraints invalidate additive local gains.
- The operation order changes feasibility or optimality and no exchange argument justifies reordering.
- A closed form has not been proven equivalent to the simulation; retain DP, graph search, or explicit simulation until equivalence is established.

## Minimal example
Before:
```py
# O042 focus: invariant
mat = csr_matrix((data,(u,v)), shape=(n,n))
comp = connected_components(mat, directed=True)
ans = solve_from_components(comp)
```
After:
```py
# optimized for invariant
adj = [[] for _ in range(n)]
for u, v in edges: adj[u].append(v)
ans = topo_dp(adj)
```
