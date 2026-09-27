---
skill_id: O006
type: operator
language: python
family: combinatorics
name: Collapse Structured Enumeration into Class Counts and Direct Top Candidate Selection
description: Reusable optimization pattern distilled from weighted traces.
tags:
- counting
- parity
- combinatorics
- closed-form
- frequency-counting
- bounded-domain
- top-2-selection
- prefix-sums
- suffix-counts
- simulation-to-formula
triggers:
- Nested loops enumerate pairs, triples, combinations, or a fixed-radius neighborhood while the predicate depends only on
  parity, color, category, or another small equivalence class.
- Constructed values are used only through a property such as parity; their exact magnitudes never affect the result.
- A result is obtained from len(list(combinations( ))) or similar materialization even though only the count is needed.
- A full grid simulation uses XOR/toggling or repeated local updates, and the final state appears to depend only on contributor-count
  parity or geometric regions.
- A generic DP transition looks back by a fixed small offset, especially two positions, suggesting parity-separated or segment-structured
  states.
- A total count minus structured exceptions formulation still performs expensive pair scans or repeated membership checks.
- A frequency map is inverted into buckets or fully sorted even though only the best one or two candidates matter.
- Values lie in a known small nonnegative domain, making direct-address arrays cheaper than hash tables.
---

## When to use
- Nested loops enumerate pairs, triples, combinations, or a fixed-radius neighborhood while the predicate depends only on parity, color, category, or another small equivalence class.
- Constructed values are used only through a property such as parity; their exact magnitudes never affect the result.
- A result is obtained from len(list(combinations( ))) or similar materialization even though only the count is needed.
- A full grid simulation uses XOR/toggling or repeated local updates, and the final state appears to depend only on contributor-count parity or geometric regions.
- A generic DP transition looks back by a fixed small offset, especially two positions, suggesting parity-separated or segment-structured states.
- A total count minus structured exceptions formulation still performs expensive pair scans or repeated membership checks.
- A frequency map is inverted into buckets or fully sorted even though only the best one or two candidates matter.
- Values lie in a known small nonnegative domain, making direct-address arrays cheaper than hash tables.

## Steps
1. Identify the smallest state that determines the predicate: parity class, color, presence, frequency parity, contributor count parity, or a small structural pattern.
2. Partition the domain into equivalence classes and count class sizes instead of constructing or scanning individual members.
3. Derive the direct formula using products for cross-class pairs, combinations such as x*(x-1)//2 for within-class pairs, or a compact case split for boundaries.
4. For simulations with toggles, count how many operations affect each target and keep only the parity; classify interior, edge, corner, and degenerate regions.
5. For structured sequence selection, replace generic DP tables with parity-specific prefix sums and enumerate only the small family of legal switch or gap layouts.
6. For ordered triple counting, precompute prefix or suffix counts so each endpoint pair contributes the number of valid third elements in O(1); subtract only explicitly characterized forbidden configurations.
7. For sparse local effects, store marked entities in a set and enumerate only the constant-size neighborhood of each entity, aggregating directly into the final counters.
8. For alternating-position frequency optimization, count values separately on each index class and retain only the top two candidates per class.

## Complexity
- Time: Typically O(1) after deriving a closed form; otherwise O(n), O(n + U), O(n + V), or O(n^2) with substantially lower constants. Here U is the number of distinct keys and V is a bounded value-domain size. Sparse local enumeration is O(N)
- Space: Typically O(1) for closed forms and case formulas; O(n) for prefix/suffix arrays or indexed positional data; O(U) for dictionary frequencies; O(V) for bounded-domain arrays; O(n) for sparse membership and candidate aggregation. Avoid

## Pitfalls
- Applying a parity shortcut without proving that the predicate depends only on parity.
- Using total-sum parity when feasibility actually depends on counts of odd elements or per-value frequency parity.
- Forgetting that a top-frequency solution needs a second-best candidate when the two index classes choose the same value.
- Assuming a generic DP and a structured prefix formulation are equivalent without checking fixed-cardinality or non-adjacency constraints.
- Counting ordered and unordered combinations inconsistently or double-counting symmetric color/order cases.
- Subtracting forbidden arithmetic-progressions or midpoint cases with incorrect index bounds.
- Ignoring degenerate dimensions and boundary contributor counts in grid formulas.
- Using dense arrays when the value universe is huge or sparse, causing excessive memory use.

## When not to use
- The predicate depends on exact values, distances, ordering, or interactions that cannot be summarized by a small number of classes.
- The feasible structures are genuinely arbitrary subsets or paths and no provable restricted pattern exists.
- The value domain is too large or sparse for direct-address arrays and hashing is more memory-efficient.
- The forbidden configurations are numerous or irregular enough that prefix/suffix counts cannot represent them in O(1) per candidate.
- The input is small enough that a straightforward implementation is clearer and performance is irrelevant.
- A closed form has not been rigorously derived or fails on boundary, tie, or degenerate cases.

## Minimal example
Before:
```py
from itertools import combinations
items = [('A', 10), ('A', 10), ('B', 7), ('B', 7), ('C', 3)]
k = 3
best = max(combinations(items, k), key=lambda xs: sum(score for _, score in xs))
print(best)
```
After:
```py
from collections import Counter
items = [('A', 10), ('A', 10), ('B', 7), ('B', 7), ('C', 3)]
k = 3
counts = Counter(label for label, _ in items); scores = dict(items)
best = [c for c in sorted(counts, key=scores.get, reverse=True) for _ in range(min(counts[c], k - len(best)))] if False else []
```
