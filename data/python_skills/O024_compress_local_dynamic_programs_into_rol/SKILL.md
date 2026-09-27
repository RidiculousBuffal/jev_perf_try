---
skill_id: O024
type: operator
language: python
family: dp
name: Compress Local Dynamic Programs into Rolling and Weighted Transitions
description: A reusable optimization pattern for dynamic programs whose states have local dependencies, small fixed dimensions,
  repeated transitions, sparse obstacles, or homogeneous runs. Replace full-history tables, dense transition matrices, repeated
  pattern enumeration, and pointwise scans with rolling state, sparse storage, precomputed local transition weights, closed-form
  combinatorial counts, or independent segment
tags:
- dynamic_programming
- state_compression
- rolling_array
- transition_precomputation
- sparse_transitions
- local_dp
- combinatorics
- segment_decomposition
- run_length_encoding
- bitmask_optimization
triggers:
- Each layer depends only on the immediately previous layer and possibly the current prefix or neighboring state.
- A DP table retains rows, columns, or dimensions that are never accessed again.
- The state dimension is tiny and fixed, such as a bounded count, pattern-prefix length, or residue class.
- A transition repeatedly sums over the same neighboring states or applies a mostly zero dense matrix.
- Transitions move only locally, such as stay, left, and right.
- The same transition structure is reused for every row, time step, or input position.
- Valid configurations are bitmasks with a local constraint such as no adjacent selections.
- A helper repeatedly enumerates the same combinatorial objects or recomputes identical counts.
---

## When to use
- Each layer depends only on the immediately previous layer and possibly the current prefix or neighboring state.
- A DP table retains rows, columns, or dimensions that are never accessed again.
- The state dimension is tiny and fixed, such as a bounded count, pattern-prefix length, or residue class.
- A transition repeatedly sums over the same neighboring states or applies a mostly zero dense matrix.
- Transitions move only locally, such as stay, left, and right.
- The same transition structure is reused for every row, time step, or input position.
- Valid configurations are bitmasks with a local constraint such as no adjacent selections.
- A helper repeatedly enumerates the same combinatorial objects or recomputes identical counts.

## Steps
1. Write the recurrence explicitly and identify the minimum predecessor information required for one update.
2. Remove unreachable or redundant state dimensions; retain only structural parameters that affect future transitions.
3. Separate transitions into carry, advance, and local-move components so the update is forward and branch-light.
4. If transitions are local, aggregate them into sparse coefficients such as stay, left, and right weights instead of applying a dense matrix.
5. If legal patterns repeat, precompute their effects once outside the main DP loop.
6. Replace repeated enumeration of constrained binary patterns with a recurrence or closed-form count, commonly a Fibonacci-like count for non-adjacent selections.
7. For sparse obstacles, sort and deduplicate barrier positions, measure open-run lengths, and multiply the independent segment contributions.
8. For run-based processes, identify boundary pairs and compute the final contribution directly from run lengths and parity rather than simulating every step.

## Complexity
- Time: Typically changes O(L*S*D) or O(L*S^2) implementations to O(L*S) when transitions have bounded local fan-in, and can change exponential repeated enumeration such as O(L*S*2^S) to O(L*S) after one-time precomputation. Segment factorization
- Space: Usually reduces full-history DP from O(L*S) or O(L*S*D) to O(S), O(D*S), or another rolling-state footprint. Sparse input storage can reduce a dense O(R*C) representation to O(K), where K is the number of nonzero updates. Precomputed

## Pitfalls
- Rolling an array in place without preserving old values needed by later transitions.
- Forgetting to reset state that is local to a row, segment, or phase.
- Using a closed-form transition count outside the width or parameter range for which it was derived.
- Recomputing supposedly precomputed combinatorial counts inside the hot loop.
- Replacing a sparse local transition with a dense matrix multiplication.
- Materializing every valid mask, tuple, permutation, or mapping when only aggregate effects are needed.
- Incorrectly treating blocked positions as independent when adjacent barriers make a segment impossible.
- Off-by-one errors in prefix, inter-barrier, and suffix segment lengths.

## When not to use
- Future transitions require arbitrary historical rows, not just a bounded recent window.
- The transition graph is genuinely dense and cannot be reduced to a small local neighborhood or reusable aggregate.
- The state dimension is large, irregular, or dependent on the full input history.
- Obstacles or updates are dense enough that sparse storage and gap processing provide no benefit.
- There is no valid closed-form or reusable aggregate for the enumerated configurations.
- Segment independence does not hold because paths or states can cross barriers or retain information across runs.

## Minimal example
Before:
```py
def count_paths(grid):
    rows, cols = len(grid), len(grid[0]); dp = [[0] * cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 0: dp[r][c] = (r == 0 and c == 0) + (dp[r-1][c] if r else 0) + (dp[r][c-1] if c else 0)
    return dp[-1][-1]
```
After:
```py
def count_paths(grid):
    cols = len(grid[0]); dp = [0] * cols; dp[0] = 1
    for row in grid:
        for c, blocked in enumerate(row):
            dp[c] = 0 if blocked else dp[c] + (dp[c-1] if c else 0)
    return dp[-1]
```
