---
skill_id: O016
type: operator
language: cpp
family: constant_factor
name: Profile First Hot Path Flattening
description: Reusable optimization pattern distilled from weighted traces.
tags:
- competitive-programming
- cpp-performance
- hot-path-optimization
- algorithmic-preprocessing
- data-structure-selection
- cache-locality
- constant-factor-optimization
- template-cleanup
- modular-arithmetic
- hashing
triggers:
- The slow and fast files are identical or truncated before solve(), main(), or the core loop.
- A large generic header, macro, or utility template dominates the visible source.
- Nested scans, repeated per-query recomputation, or repeated sorting may exist in the omitted body.
- map, set, PBDS, or other node-based containers appear in high-frequency operations.
- Hash-table lookup or insertion dominates profiling, especially with reallocation or long probe chains.
- Repeated modular inverse, exponentiation, division, primality, or digit-processing helpers occur inside loops.
- Circular-index macros repeatedly evaluate size() and modulo in tight loops.
- Large integer state spaces may fit in compact arrays, masks, or compiler bit intrinsics.
---

## When to use
- The slow and fast files are identical or truncated before solve(), main(), or the core loop.
- A large generic header, macro, or utility template dominates the visible source.
- Nested scans, repeated per-query recomputation, or repeated sorting may exist in the omitted body.
- map, set, PBDS, or other node-based containers appear in high-frequency operations.
- Hash-table lookup or insertion dominates profiling, especially with reallocation or long probe chains.
- Repeated modular inverse, exponentiation, division, primality, or digit-processing helpers occur inside loops.
- Circular-index macros repeatedly evaluate size() and modulo in tight loops.
- Large integer state spaces may fit in compact arrays, masks, or compiler bit intrinsics.

## Steps
1. Recover complete paired sources and locate the first semantic divergence; do not infer complexity from shared boilerplate.
2. Profile or count work in the solver: loop nesting, query scans, repeated searches, allocations, sorting, arithmetic, and container operations.
3. Classify the main transformation as repeated computation to preprocessing, online queries to offline sorting, nested scans to sweep or two pointers, tree containers to compressed arrays or vectors, or brute-force state traversal to DP or bitmask operations.
4. Hoist invariant calculations out of inner loops and cache repeated values, including modular powers, inverses, geometry predicates, hashes, and coordinate mappings.
5. For queries, build prefix or suffix aggregates, frequency tables, compressed indices, sorted orders, Fenwick or segment structures, monotone queues, or one-pass incremental state as appropriate.
6. Prefer contiguous vector or array storage; replace map/set with sort plus scan, coordinate compression, arrays, or unordered containers when ordering is unnecessary.
7. For primitive-key hash tables, reserve capacity, control load factor, use a robust rehash policy, and prefer cache-friendly open addressing when suitable.
8. Reserve vector and string capacity, avoid pass-by-value of heavy objects, use const references where appropriate, emplace objects, and reuse buffers.

## Complexity
- Time: Algorithm-dependent. Typical successful rewrites reduce repeated scans such as O(nq), O(n^2), or O(n^3) to O(n+q), O((n+q) log n), or O(n log n). Representation-only changes usually preserve the original Big-O while lowering constants
- Space: Algorithm-dependent. Preprocessing commonly uses O(n), O(n+q), or O(U) auxiliary space for arrays, compressed coordinates, prefix data, or hash tables; offline and sweep approaches may use O(n+q). Flat representations often reduce

## Pitfalls
- Claiming an O( ) improvement when the algorithm body is missing or identical in the visible excerpts.
- Optimizing macros, headers, or tiny helper functions while leaving quadratic, cubic, or per-query rescanning work unchanged.
- Replacing ordered containers with unordered containers when deterministic ordering, predecessor queries, or adversarial collision behavior matters.
- Eagerly default-constructing every slot of a large hash table when the value type is expensive.
- Using a sentinel key that is also a valid input key.
- Removing 64-bit arithmetic without proving bounds, or retaining global int-to-long-long promotion where it needlessly inflates arrays and register pressure.
- Performing signed multiplication before modulo and assuming overflow is harmless.
- Calling modular inverse, power, primality, or digit routines repeatedly when their results can be precomputed or reused.

## When not to use
- The solver is already asymptotically optimal and profiling shows no meaningful hot path.
- The workload is small enough that simpler containers and generic templates cannot affect the limit.
- Ordering, stability, exact arbitrary precision, or strict floating-point semantics are fundamental requirements.
- Hashing has adversarial guarantees that require a tree or deterministic structure.
- Memory limits make precomputation, coordinate compression, or table reservation too expensive.
- The proposed rewrite cannot be validated because the complete algorithm, constraints, or numeric bounds are unavailable.

## Minimal example
Before:
```cpp
inline int gain(int x) { return x > 0 ? x * 3 : 0; }
inline int score(const std::vector<int>& a) {
    int total = 0;
    for (int x : a) total += gain(x);
    return total;
}
```
After:
```cpp
inline int score(const std::vector<int>& a) {
    int total = 0;
    // Profiled hot path flattened: avoid per-element helper overhead.
    for (int x : a) if (x > 0) total += x * 3;
    return total;
}
```
