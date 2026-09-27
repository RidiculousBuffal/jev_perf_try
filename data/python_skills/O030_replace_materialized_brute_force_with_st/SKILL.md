---
skill_id: O030
type: operator
language: python
family: graph
name: Replace Materialized Brute Force with Structural Streaming Checks
description: Optimize string-heavy decision and construction code by exposing the underlying structural predicate, reducing
  candidates to only feasible cases, and validating through direct indexed scans, prefix/suffix checks, or incremental state.
  Avoid constructing strings, slices, repeated-count scans, parsed big integers, or symmetric candidate outputs when the result
  can be decided from lengths, ordering, local characters
tags:
- strings
- prefix-suffix-matching
- lexicographic-comparison
- early-exit
- allocation-reduction
- brute-force-reduction
- streaming-validation
- hash-set
- big-integer-comparison
- implementation
triggers:
- A loop repeatedly constructs slices, concatenations, transformed strings, or stepped substrings only to compare them.
- A predicate naturally decomposes into prefix agreement, suffix agreement, local adjacency, or indexed character equality.
- A fixed or short target is checked through nested enumeration of impossible split or deletion combinations.
- A loop contains list.count, membership tests on a list, or another full-container scan for every element.
- The code builds two symmetric candidate strings and applies min or max even though their ordering follows from simpler input
  properties.
- Sorted data is joined into strings solely for lexicographic comparison.
- Large decimal strings are converted to integers or subtracted only to determine ordering.
- A bulk transformation such as replace, filter, split, or join is used when only the first qualifying character or position
  matters.
---

## When to use
- A loop repeatedly constructs slices, concatenations, transformed strings, or stepped substrings only to compare them.
- A predicate naturally decomposes into prefix agreement, suffix agreement, local adjacency, or indexed character equality.
- A fixed or short target is checked through nested enumeration of impossible split or deletion combinations.
- A loop contains list.count, membership tests on a list, or another full-container scan for every element.
- The code builds two symmetric candidate strings and applies min or max even though their ordering follows from simpler input properties.
- Sorted data is joined into strings solely for lexicographic comparison.
- Large decimal strings are converted to integers or subtracted only to determine ordering.
- A bulk transformation such as replace, filter, split, or join is used when only the first qualifying character or position matters.

## Steps
1. State the exact predicate independently of the current implementation; identify what information is actually required for acceptance or ordering.
2. Derive length constraints before searching. Eliminate candidate splits, deletions, alignments, or repetition counts that cannot satisfy the target length.
3. Replace reconstruction with structural checks: use startswith, endswith, direct indexing, length comparison, or complementary prefix/suffix validation.
4. For fixed targets, iterate only over valid split positions and return immediately on the first successful check.
5. For repeated pattern matching, enumerate feasible starts and steps, compare characters by indexed access, abort on bounds failure or the first mismatch, and count each input item at most once.
6. For local constraints plus uniqueness, make one left-to-right pass; compare neighboring characters and maintain a set or frequency map of previously seen items.
7. For lexicographic comparisons, compare source sequences directly and stop at the first mismatch. If the common prefix ends, apply the correct length rule.
8. For non-negative decimal strings, compare lengths first and then corresponding digits; avoid integer conversion and subtraction when only order is needed.

## Complexity
- Time: Typically reduces repeated materialization and rescanning from quadratic or cubic-style practical cost to one-pass or structurally bounded scans. Prefix/suffix checks over a fixed target are O(n) with a constant number of checks; stateful
- Space: Usually O(1) auxiliary space for direct comparisons, prefix/suffix checks, indexed scans, and streaming output. Stateful uniqueness checks require O(n) expected space for a set or map. Sorting requires O(n + m) storage. Output

## Pitfalls
- Removing allocations without verifying that the rewritten predicate is logically equivalent.
- Checking all pairs of split positions instead of only complementary positions whose lengths sum to the target length.
- Using slicing in a hot loop, which still copies data even when the slice is immediately compared.
- Assuming a string is non-empty before indexing its final character.
- Using a suffix or prefix rewrite that changes behavior for unequal lengths or empty strings.
- Continuing to scan after a mismatch or after a successful existence check.
- Replacing list rescans with a set but forgetting to update the set incrementally.
- Counting duplicates indirectly through opaque arithmetic instead of maintaining explicit seen state.

## When not to use
- Do not replace a clear built-in operation when inputs are small and the operation is already implemented efficiently in native code.
- Do not use manual character loops when a library operation is both clearer and sufficiently fast.
- Do not use hash-based state when the domain is tiny and a simpler bounded representation is more appropriate.
- Do not avoid materialization when the complete transformed value is genuinely required later or must be returned.
- Do not infer numeric ordering from string length without canonical non-negative decimal representation and proper leading-zero handling.
- Do not reduce candidates using fixed-target assumptions unless the target length and transformation rules are guaranteed.

## Minimal example
Before:
```py
# O030 focus: replace
mat = csr_matrix((data,(u,v)), shape=(n,n))
comp = connected_components(mat, directed=True)
ans = solve_from_components(comp)
```
After:
```py
# optimized for replace
adj = [[] for _ in range(n)]
for u, v in edges: adj[u].append(v)
ans = topo_dp(adj)
```
