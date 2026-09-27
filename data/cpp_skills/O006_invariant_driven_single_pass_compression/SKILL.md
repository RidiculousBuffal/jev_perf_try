---
skill_id: O006
type: operator
language: cpp
family: state_compression
name: Invariant Driven Single Pass Compression
description: Replace simulation-heavy, state-sprawling, or multi-pass C++ solutions with the smallest representation implied
  by the invariant. First identify whether the result depends only on adjacent state, aggregate counts, parity, positional
  mappings, or a monotone frontier. Then process input once when possible, fold uniform updates into a baseline, eliminate
  temporary arrays used only for reduction, and express local
tags:
- optimization
- greedy
- single-pass
- stream-processing
- state-compression
- invariant
- array-scan
- simulation-elimination
- space-reduction
- parity
triggers:
- A temporary array is written once and later reduced to one scalar.
- A full-array update applies the same constant to every element.
- The recurrence uses only the previous element, current element, or adjacent pair.
- A fix at index i changes only i and i+1, but the implementation repeatedly revisits earlier indices.
- A matching or pairing decision is non-overlapping and local, suggesting count-and-skip.
- A boolean flag or first-element state is carried through a tight loop only for setup.
- A large fixed buffer exists despite one-pass processing or per-test-case sizing being sufficient.
- A DP dimension is queried only by parity or another small equivalence class.
---

## When to use
- A temporary array is written once and later reduced to one scalar.
- A full-array update applies the same constant to every element.
- The recurrence uses only the previous element, current element, or adjacent pair.
- A fix at index i changes only i and i+1, but the implementation repeatedly revisits earlier indices.
- A matching or pairing decision is non-overlapping and local, suggesting count-and-skip.
- A boolean flag or first-element state is carried through a tight loop only for setup.
- A large fixed buffer exists despite one-pass processing or per-test-case sizing being sufficient.
- A DP dimension is queried only by parity or another small equivalence class.

## Steps
1. Write the final quantity or feasibility condition algebraically before changing data structures.
2. Classify the dependency: adjacent state, monotone frontier, frequency counts, positional mapping, parity class, or order-sensitive simulation.
3. Remove any intermediate array whose entries are consumed exactly once; accumulate directly in the producer pass.
4. Fold uniform initialization and global adjustments into one baseline, such as base + local_count + global_offset.
5. For adjacent recurrences, retain only previous/current scalars and stream the input.
6. For monotone greedy constraints, maintain the smallest sufficient frontier and update it immediately; never revisit finalized positions.
7. Hoist first-element initialization outside the hot loop and remove redundant continue branches or setup flags.
8. If the property is positional, read the sequence and build an inverse map or occurrence buckets; do not substitute a weaker input-order test.

## Complexity
- Time: Usually O(n) for scans, streaming reductions, local greedy passes, parity formulas, and sparse-count evaluation. Positional inversion or occurrence processing is typically O(n), while inversion-count helpers remain O(n log n)
- Space: Use O(1) auxiliary space when only adjacent or aggregate state is needed. Use O(n) space for inverse mappings, occurrence lists, reconstruction, or required random access. Prefer per-test-case, constraint-sized contiguous storage over

## Pitfalls
- Assuming a linear implementation is optimal when it performs unnecessary full-array writes, reads, or clearing.
- Replacing a correct order-sensitive process with a formula based only on aggregate frequencies.
- Compressing DP by value when feasibility depends on relative positions between values.
- Forcing a streaming solution when an inverse permutation or occurrence-position representation is required for correctness.
- Using vector erase, repeated searching, or reset-and-rescan logic in a problem with a local greedy rule.
- Breaking input processing early and leaving the current test case unread.
- Reading an uninitialized tail element as an implicit sentinel; initialize it explicitly.
- Using non-standard variable-length arrays or oversized stack buffers in C++.

## When not to use
- Do not stream when later logic requires arbitrary random access, reconstruction, sorting, or positional relationships.
- Do not replace simulation with a closed form without proving that move order and intermediate states cannot affect the result.
- Do not compress DP dimensions unless both transitions and the queried output are invariant under the proposed projection.
- Do not apply count-and-skip when matches overlap or when selecting one pair changes nonlocal eligibility.
- Do not remove arrays that encode future dependencies, suffix information, or values needed after the current pass.
- Do not use a fixed sentinel unless its value is valid for every boundary condition and its storage is initialized.

## Minimal example
Before:
```cpp
// O006 focus: invariant
vector<int> ans;
for (int x = 1; x <= MAXV; ++x) {
  bool ok = true;
  for (const auto& grp : groups) if (!binary_search(grp.begin(), grp.end(), x)) ok = false;
  if (ok) ans.push_back(x);
}
```
After:
```cpp
// optimized for invariant
vector<int> freq(MAXV + 1, 0);
for (const auto& grp : groups)
  for (int x : grp) ++freq[x];
for (int x = 1; x <= MAXV; ++x)
  if (freq[x] == (int)groups.size()) ans.push_back(x);
```
