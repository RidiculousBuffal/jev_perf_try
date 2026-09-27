---
skill_id: O025
type: operator
language: cpp
family: state_compression
name: Compress Repeated Search into Aggregate DP or Bitmask States
description: When brute force repeatedly constructs equivalent structures, rescans the same input, or recomputes transition
  data, identify the smallest state that preserves future feasibility and contribution. Replace explicit enumeration with
  memoized or iterative dynamic programming over aggregate counts, bounded sums, subset masks, component counts, or parity
  masks. Precompute reusable combinatorial, compatibility, distance
tags:
- dynamic-programming
- state-compression
- combinatorics
- bitmask-dp
- subset-enumeration
- memoization
- precomputation
- counting
- mod-arithmetic
- small-n-exponential
triggers:
- DFS stores indices or a construction sequence and rescans it only at leaves or in a separate checker.
- A recursive search calls a full validation or scoring pass at every node.
- Equivalent paths differ only by counts, multiplicities, processed levels, used sum, parity, or component count.
- A recurrence enumerates every split or submask while recomputing the same aggregate transition data.
- A helper such as a binomial, probability, distance, or compatibility calculation runs inside a hot nested loop.
- A temporary counter or accumulator array is cleared and rebuilt for every mask or state.
- The input has a tiny fixed domain, such as a small alphabet, a few counters, a short bit width, or a bounded circular state.
- A subset DP uses dense per-vertex or per-item tables although the underlying graph or relation is sparse.
---

## When to use
- DFS stores indices or a construction sequence and rescans it only at leaves or in a separate checker.
- A recursive search calls a full validation or scoring pass at every node.
- Equivalent paths differ only by counts, multiplicities, processed levels, used sum, parity, or component count.
- A recurrence enumerates every split or submask while recomputing the same aggregate transition data.
- A helper such as a binomial, probability, distance, or compatibility calculation runs inside a hot nested loop.
- A temporary counter or accumulator array is cleared and rebuilt for every mask or state.
- The input has a tiny fixed domain, such as a small alphabet, a few counters, a short bit width, or a bounded circular state.
- A subset DP uses dense per-vertex or per-item tables although the underlying graph or relation is sparse.

## Steps
1. Write down the information used by future transitions and discard path-specific details that do not affect it.
2. Choose the smallest suitable state: bounded sum and number of remaining variables, frequency/count vector, subset mask, parity mask, component count, or prefix length plus selected count.
3. Replace explicit construction with memoized recursion or bottom-up DP indexed by that compressed state.
4. Precompute binomial coefficients, factorials and inverse factorials, powers, PMFs/CDFs, compatibility tables, nearest-distance tables, subset edge counts, or generated denominations before hot transitions.
5. Use combinatorial multiplicities to count many equivalent branches in one transition instead of enumerating arrangements individually.
6. Fold deterministic propagation and validation together; after propagation, check only residual boundary or closure conditions.
7. For subset problems, pack fixed-width features into integer masks, use popcount and bitwise operations, and canonicalize submask splits with an anchor bit when partitions would otherwise be duplicated.
8. Exploit sparsity by traversing adjacency lists or active elements rather than scanning every vertex or every dimension for every transition.

## Complexity
- Time: Typical compressed bounded-state DP is polynomial in its state dimensions, often O(N^3) to O(N^4) for partition/composition-style states. Tiny-domain subset methods commonly require O(N·2^N), O(N·3^N), or O(N·K·2^K), with substantial
- Space: (pattern dependent)

## Pitfalls
- Compressing the state without proving that discarded information cannot affect future transitions or final multiplicity.
- Using subset DP when n is too large, or using a high-dimensional dense DP when the state space is sparse.
- Counting aggregate states but forgetting combinatorial factors for placements, permutations, repeated values, or equal elements.
- Recomputing binomial coefficients, powers, scans, or temporary arrays inside the innermost transition.
- Using std::pow for small integer exponents in a 3^n loop instead of table lookup or multiplication.
- Leaving invalid zero states in a generic convolution and paying for them until a late correction pass.
- Using floating-point comparisons for averages, probabilities, or ratios when cross-multiplication is available.
- Missing modulo operations after multiplication, causing signed overflow before reduction.

## When not to use
- The state cannot be summarized without losing information required by future choices.
- n or the bit width is too large for 2^n or 3^n enumeration and no stronger structural pruning exists.
- The DP dimensions are large or unbounded, making dense precomputation exceed memory or time limits.
- A direct greedy, sorting, formula, or classical polynomial algorithm already dominates the proposed DP.
- The graph or state relation is dense enough that sparse traversal provides no benefit.
- The number of queries is one and global precomputation costs more than a simple per-query computation.

## Minimal example
Before:
```cpp
// O025 focus: compress
vector<int> ans;
for (int x = 1; x <= MAXV; ++x) {
  bool ok = true;
  for (const auto& grp : groups) if (!binary_search(grp.begin(), grp.end(), x)) ok = false;
  if (ok) ans.push_back(x);
}
```
After:
```cpp
// optimized for compress
vector<int> freq(MAXV + 1, 0);
for (const auto& grp : groups)
  for (int x : grp) ++freq[x];
for (int x = 1; x <= MAXV; ++x)
  if (freq[x] == (int)groups.size()) ans.push_back(x);
```
