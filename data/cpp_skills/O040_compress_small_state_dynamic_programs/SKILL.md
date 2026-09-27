---
skill_id: O040
type: operator
language: cpp
family: digit
name: Compress Small State Dynamic Programs
description: When a C++ solution uses a large or repeatedly materialized DP for a process with a tiny finite state space,
  expose the true state invariant, remove redundant dimensions, and optimize the implementation around adjacent-layer transitions.
  Replace inflated digit, residue, orientation, carry, or bitmask states with the smallest sufficient automaton; use rolling
  arrays or scalar variables when only the previous layer
tags:
- dynamic-programming
- state-compression
- rolling-array
- finite-state-automaton
- digit-dp
- modulo-state-dp
- bitmask-dp
- counting
- memoization
- greedy-unranking
triggers:
- Every layer depends only on the immediately previous layer.
- A DP table stores positions or history that are never revisited.
- The state dimension is fixed and small, but the implementation uses nested vectors, oversized arrays, or full 2D history.
- Many states are impossible, equivalent, or differ only by a small mode such as carry, orientation, tightness, or remainder.
- A digit or string DP uses a tiny residue or automaton state and a long input.
- Hot loops repeatedly compute the same transition, modulo, comparison class, or bitmask update.
- Transitions write to an overflow bucket such as K+1 that is never queried.
- A queue or BFS is used only to obtain the k-th lexicographically or numerically ordered object.
---

## When to use
- Every layer depends only on the immediately previous layer.
- A DP table stores positions or history that are never revisited.
- The state dimension is fixed and small, but the implementation uses nested vectors, oversized arrays, or full 2D history.
- Many states are impossible, equivalent, or differ only by a small mode such as carry, orientation, tightness, or remainder.
- A digit or string DP uses a tiny residue or automaton state and a long input.
- Hot loops repeatedly compute the same transition, modulo, comparison class, or bitmask update.
- Transitions write to an overflow bucket such as K+1 that is never queried.
- A queue or BFS is used only to obtain the k-th lexicographically or numerically ordered object.

## Steps
1. State the invariant precisely: define what each DP state represents and identify which parts of history affect future transitions.
2. Construct the minimal sufficient state. Collapse equivalent digit identities, endpoint pairs, carry histories, or ordering classes into a small mode or automaton state.
3. Remove dimensions that are only used by adjacent layers. Replace full tables with two contiguous rows, one rolling buffer, or a few scalar variables.
4. Size arrays exactly to the reachable state domain; never retain unused sentinel columns or guessed capacity limits.
5. Precompute fixed transitions such as residue changes, digit-combination results, bitmask destinations, comparison classes, or powers of the base.
6. Separate fixed-character and wildcard transitions when the former has a single destination and the latter has bounded fanout.
7. Prune immediately when a count, sum, mask, or resource exceeds its allowed bound; avoid generating states that cannot contribute.
8. Use flat arrays or fixed-size stack/global buffers for known small dimensions instead of nested dynamic vectors.

## Complexity
- Time: Usually unchanged at O(nS A), where S is the minimal state count and A is transition fanout; common digit/residue cases are O(n * 13 * 10). State compression can reduce a constant-size O(n * 81) or O(n * 900) recurrence to O(n) with a
- Space: Use O(S) auxiliary space with rolling DP or scalar recurrence when only adjacent layers are required. Full memoization costs O(nS), and bitmask or weighted-sum DP costs O(number_of_masks * bound). Grouped transition processing can use

## Pitfalls
- Replacing an order-sensitive transition process with a closed form based only on a digit sum, total count, or digital-root-like quantity.
- Calling memoized recursion faster when it has the same recurrence but adds O(nS) memory, recursion overhead, and stack-depth risk.
- Materializing all position layers when only the previous layer is read.
- Using nested std::vector for tiny fixed dimensions, causing allocator overhead, pointer chasing, and poor cache locality.
- Updating states with count K+1 or another overflow bucket that is never consumed.
- Failing to clear a rolling destination row before accumulation.
- Assuming a fixed-digit transition is a permutation and omitting clearing without proving that every destination is written exactly once.
- Using an undersized static bound that silently rejects valid inputs or causes out-of-bounds access.

## When not to use
- Future transitions genuinely depend on multiple older layers or the complete history.
- The discarded DP dimension is required for reconstruction, path reporting, or later offline queries.
- The state space is sparse and dynamic, making a dense fixed array substantially larger than a hash-based representation.
- Transition precomputation would consume more memory than it saves or would be dominated by one-time work.
- The query asks for every generated object, so count-and-unrank cannot replace enumeration.
- A closed form has been formally derived from the exact transition algebra and independently verified across boundary cases.

## Minimal example
Before:
```cpp
std::vector<std::array<long long, 2>> dp(n + 1);
dp[0][0] = 1;
for (int i = 0; i < n; ++i) {
    dp[i + 1][0] = dp[i][0] + dp[i][1]; dp[i + 1][1] = dp[i][0];
}
return dp[n][0] + dp[n][1];
```
After:
```cpp
long long zero = 1, one = 0;
for (int i = 0; i < n; ++i) {
    long long next_zero = zero + one;
    one = zero; zero = next_zero;
}
return zero + one;
```
