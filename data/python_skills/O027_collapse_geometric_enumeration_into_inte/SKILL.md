---
skill_id: O027
type: operator
language: python
family: streaming
name: Collapse Geometric Enumeration into Integer, Streaming, or Native Aggregation
description: Optimize geometry and pairwise numeric workloads by identifying separability, projection identities, invariant
  state, and static predicates before applying implementation-level acceleration. Replace 2D or pairwise contribution enumeration
  with 1D closed-form sums or transformed extrema when the metric permits; replace floating-point integrality checks with
  exact squared-integer predicates; replace repeated linear
tags:
- computational-geometry
- manhattan-distance
- euclidean-distance
- pair-counting
- nearest-neighbor
- coordinate-transform
- separability
- streaming-extrema
- perfect-square-check
- hash-set-membership
triggers:
- A symmetric grid or pairwise sum is computed by enumerating cells, rows, columns, or pairs even though the contribution
  separates by coordinate.
- A 2D Manhattan-distance extremum involves expressions such as x+y or x-y, or sorts points only to inspect extreme candidates.
- The output depends only on max(value)-min(value) for derived values stored in lists.
- A Euclidean distance is computed with sqrt or exponentiation only to determine whether it is integral.
- A hot loop scans all candidate integers, uses any( ), or repeatedly tests membership in a list.
- A fixed anchor determines candidate translations or transformations, followed by repeated exact point-existence checks.
- A full pairwise distance matrix is filled one scalar at a time in Python and then reduced with argmin or a similar operation.
- The computation is a regular dense numeric kernel with independent pair evaluations and vectorized native libraries are
  available.
---

## When to use
- A symmetric grid or pairwise sum is computed by enumerating cells, rows, columns, or pairs even though the contribution separates by coordinate.
- A 2D Manhattan-distance extremum involves expressions such as x+y or x-y, or sorts points only to inspect extreme candidates.
- The output depends only on max(value)-min(value) for derived values stored in lists.
- A Euclidean distance is computed with sqrt or exponentiation only to determine whether it is integral.
- A hot loop scans all candidate integers, uses any( ), or repeatedly tests membership in a list.
- A fixed anchor determines candidate translations or transformations, followed by repeated exact point-existence checks.
- A full pairwise distance matrix is filled one scalar at a time in Python and then reduced with argmin or a similar operation.
- The computation is a regular dense numeric kernel with independent pair evaluations and vectorized native libraries are available.

## Steps
1. State the exact invariant being computed: a separable sum, a transformed extremum, a static predicate, a membership query, or a row-wise reduction.
2. For Manhattan distance in two dimensions, use max(|x1-x2|+|y1-y2|) = max(range(x+y), range(x-y)); track four extrema while reading points.
3. For grid-wide pairwise Manhattan sums, split row and column contributions and aggregate by one-dimensional distance classes, such as sum over d of d*(L-d), then apply any unchanged combinatorial multiplier.
4. For integer Euclidean-distance predicates, accumulate squared coordinate differences as an integer and test perfect-square membership with isqrt: r = isqrt(dist2), valid iff r*r == dist2.
5. If bounds are fixed and known, precompute the relevant perfect-square set once; otherwise prefer integer square root over unsafe hardcoded ranges.
6. For translation or exact-transformation search, choose one stable anchor, derive each candidate offset from it, store the target points in a hash set, and verify translated source points with constant-time membership.
7. Remove sorting when only existence, frequency, extrema, or unordered pair counts are required.
8. For displacement-frequency counting, count pair-derived vectors directly in a dictionary and compute the required maximum frequency without copying dictionary values into a list.

## Complexity
- Time: Typical reduced forms are O(H+W) for separable grid aggregation, O(N) for streaming Manhattan extrema, O(N^2*D) for exact pair counting after removing per-pair scans, O(M*N) for translation verification with hash membership, and O(N*Q)
- Space: Reduced streaming or projection-extrema solutions use O(1) auxiliary space. Hash-based membership or displacement-frequency methods use O(U), where U is the number of stored distinct points or derived keys, potentially O(N^2). Pairwise

## Pitfalls
- Applying a Manhattan projection identity to a task that is not actually a global Manhattan diameter.
- Replacing unordered pairs with ordered pairs without correcting for self-pairs and double counting.
- Using floating-point equality to test whether a distance is integral, especially after sqrt or exponentiation.
- Precomputing a perfect-square table with an unjustified fixed bound that may not cover valid distances.
- Using a hash set when multiplicity matters; sets answer existence, not frequency.
- Keeping sorting merely to choose an anchor or inspect extrema when a first point or streaming min/max is sufficient.
- Materializing all points, transformed arrays, or distance matrices when only a few extrema or reductions are needed.
- Claiming an asymptotic improvement from vectorization when the operation count remains O(n*m) or O(n^2*d).

## When not to use
- Do not use projection-based Manhattan identities when the metric, objective, dimensions, or constraints invalidate the identity.
- Do not force a closed-form aggregation when contributions depend on obstacles, labels, local state, boundaries, or nonseparable interactions.
- Do not use dense vectorization or full distance matrices when inputs are too large for the required temporary memory.
- Do not replace a list or multiset with a set when duplicate counts, ordering, or multiplicity affect correctness.
- Do not retain quadratic pair enumeration if a spatial index, sweep line, FFT, convolution, hashing scheme, or problem-specific geometric algorithm can reduce the pair search itself.
- Do not precompute lookup tables when the numeric domain is unbounded or the table would be larger than direct integer arithmetic.

## Minimal example
Before:
```py
# O027 focus: collapse
vals = []
for x in data:
    vals.append(transform(x))
ans = sum(vals)
```
After:
```py
# optimized for collapse
ans = 0
for x in data:
    ans += transform(x)
# single-pass aggregate
```
