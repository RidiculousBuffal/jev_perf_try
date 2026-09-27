---
skill_id: O002
type: operator
language: cpp
family: dp
name: Normalize and Compress Dense Dynamic Programming
description: Reusable optimization pattern distilled from weighted traces.
tags:
- dynamic-programming
- dp-normalization
- rolling-array
- state-compression
- prefix-sums
- running-sums
- cache-locality
- contiguous-storage
- constant-factor-optimization
- recurrence-correction
triggers:
- A DP table has dimensions or layers that are never simultaneously needed.
- Each layer depends only on the previous layer, or a sequence recurrence depends only on the previous one or two states.
- The hot loop repeatedly sums nearly the same predecessor range or updates the same destination through many separate passes.
- A dense bounded state space is represented with maps, nested vectors, recursion, or fragmented containers.
- Boundary checks, obstacle checks, or state-gating branches are repeated inside an otherwise regular interior loop.
- The recurrence contains a source-data value confused with a DP value, or otherwise appears semantically inconsistent.
- Memoization uses a value-based validity test such as `memo[x] > 0` even though zero or negative answers are valid.
- A postprocessing step accumulates unused values, applies modular inverses, or normalizes a state that could directly represent
  the requested answer.
---

## When to use
- A DP table has dimensions or layers that are never simultaneously needed.
- Each layer depends only on the previous layer, or a sequence recurrence depends only on the previous one or two states.
- The hot loop repeatedly sums nearly the same predecessor range or updates the same destination through many separate passes.
- A dense bounded state space is represented with maps, nested vectors, recursion, or fragmented containers.
- Boundary checks, obstacle checks, or state-gating branches are repeated inside an otherwise regular interior loop.
- The recurrence contains a source-data value confused with a DP value, or otherwise appears semantically inconsistent.
- Memoization uses a value-based validity test such as `memo[x] > 0` even though zero or negative answers are valid.
- A postprocessing step accumulates unused values, applies modular inverses, or normalizes a state that could directly represent the requested answer.

## Steps
1. Write down the exact state meaning, predecessor set, answer state, and valid numeric range before changing the code.
2. Audit every recurrence operand: distinguish source data from accumulated DP values and correct malformed transitions before optimizing.
3. Handle minimal dimensions explicitly, especially N==1, N==2, empty inputs, first rows, first columns, and terminal adjustments.
4. Choose an explicit cache-validity mechanism: a separate `visited` array or an impossible sentinel such as `LLONG_MIN`; never infer visitation from positivity unless guaranteed.
5. Convert recursive linear or fixed-state DP to bottom-up iteration when dependencies are acyclic and local, avoiding call overhead and stack-depth risk.
6. Replace full tables with rolling layers when only the previous layer is read; reduce one- or two-step recurrences to a few scalar variables when possible.
7. Normalize transition direction into either pull style, where each destination reads predecessors, or push style, where each source writes successors; choose the form with fewer branches and more sequential access.
8. Fuse compatible passes so each destination is written once or each layer is scanned minimally. Move boundary cases outside the hot loop.

## Complexity
- Time: (pattern dependent)
- Space: Reduce storage from all layers to one or two rolling layers whenever dependencies permit: O(Layers * States) becomes O(States), and local one-dimensional recurrences can often reach O(1) auxiliary DP space. Dense multidimensional states

## Pitfalls
- Changing loop direction without confirming whether states represent 0/1 or unbounded item usage.
- Using a sentinel such as `-1` when valid answers can be negative, or using positivity as a visited marker when zero is valid.
- Copying a recursive 'fast' reference even though iterative tabulation has better locality and avoids stack overflow.
- Compressing a dimension while accidentally retaining a dependency on an older layer.
- Clearing only part of a rolling buffer without proving that every read cell is overwritten or initialized.
- Leaving boundary cases inside the hot loop, or moving them out without initializing the first row and column correctly.
- Reading `j-1` or `j+1` at state boundaries and relying on global zero-initialization to make the access appear harmless.
- Using a fixed array bound smaller than the real input-dependent dimension.

## When not to use
- The recurrence genuinely depends on many earlier layers or arbitrary historical states, so rolling storage would lose required information.
- The state space is sparse, irregular, or too large for direct addressing; maps or coordinate compression may then be appropriate.
- A transition aggregation cannot be derived algebraically and scanning all predecessors is required for correctness.
- The problem needs reconstruction of the full DP history and no compact parent representation is available.
- Bitset packing is unsuitable because states carry values rather than boolean reachability, or transitions are not representable as shifts and bitwise operations.
- The current implementation is already within limits and the proposed rewrite would add substantial complexity without measurable bottleneck evidence.

## Minimal example
Before:
```cpp
// O002 focus: normalize
vector<vector<int>> dp(n + 1, vector<int>(W + 1, 0));
for (int i = 1; i <= n; ++i)
  for (int w = 0; w <= W; ++w)
    dp[i][w] = max(dp[i - 1][w], w >= wt[i] ? dp[i - 1][w - wt[i]] + val[i] : 0);
```
After:
```cpp
// optimized for normalize
vector<int> dp(W + 1, 0);
for (int i = 1; i <= n; ++i)
  for (int w = W; w >= wt[i]; --w)
    dp[w] = max(dp[w], dp[w - wt[i]] + val[i]);
```
