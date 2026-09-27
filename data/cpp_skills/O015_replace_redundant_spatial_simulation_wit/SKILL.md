---
skill_id: O015
type: operator
language: cpp
family: streaming
name: Replace Redundant Spatial Simulation with Aggregated Sweeps and Direct Construction
description: Reusable optimization pattern distilled from weighted traces.
tags:
- optimization
- grid
- simulation
- constructive
- counting
- precomputation
- state-compression
- coordinate-compression
- sweep-line
- periodicity
triggers:
- A candidate loop repeatedly rescans the same grid or array while changing only a small class, color, phase, or orientation
  assignment.
- A temporary array or expanded sequence is built and consumed exactly once in order.
- A 2D prefix or difference grid is used even though effects are periodic, separable, or change only at boundary events.
- A 3D canvas is incremented for every cell inside every box after coordinate compression.
- A recursive roll, cascade, deletion, or local compaction simulation is called once per operation and may traverse a long
  chain.
- A fixed-capacity grid is cleared or copied in full although only a sparse or thin active region is relevant.
- A hot loop repeatedly performs modulo, division, boundary checks, or mutually exclusive condition chains on predictable
  patterns.
- A run is first measured and then revisited solely to write the same value into each element.
---

## When to use
- A candidate loop repeatedly rescans the same grid or array while changing only a small class, color, phase, or orientation assignment.
- A temporary array or expanded sequence is built and consumed exactly once in order.
- A 2D prefix or difference grid is used even though effects are periodic, separable, or change only at boundary events.
- A 3D canvas is incremented for every cell inside every box after coordinate compression.
- A recursive roll, cascade, deletion, or local compaction simulation is called once per operation and may traverse a long chain.
- A fixed-capacity grid is cleared or copied in full although only a sparse or thin active region is relevant.
- A hot loop repeatedly performs modulo, division, boundary checks, or mutually exclusive condition chains on predictable patterns.
- A run is first measured and then revisited solely to write the same value into each element.

## Steps
1. Classify the true information carried by the slow representation: frequency by class, boundary events, orientation, parity, segment length, or a small finite state.
2. Separate mandatory work from avoidable work. Inspect whether every cell, candidate, box, operation, or path character must actually be materialized.
3. For additive objectives, aggregate by structural class. Build freq[class][original_state] or an equivalent compact count table.
4. Precompute reusable costs or transitions once, then enumerate only the small candidate domain. For three classes, use precomputed classCost[class][target] and enumerate distinct triples.
5. For coordinate-compressed geometry, deduplicate endpoint coordinates, store rank intervals, precompute cell volumes, and choose between painting and cell-versus-object tests based on density.
6. For periodic or separable 2D effects, normalize coordinates modulo the period, fix one boundary, accumulate one-dimensional buckets, and sweep the other boundary by applying entering/leaving event counts.
7. Replace per-box raster updates with one visit per compressed cell and containment tests when boxes are large or overlap heavily; use difference arrays or range updates when objects are sparse and spans are cheap.
8. Fuse one-shot expansion with placement. Keep remaining counts or the current state, advance past exhausted entries, and write directly to the final grid or output buffer.

## Complexity
- Time: Typical transformed complexity is O(N + S) for streaming or compact state transitions, O(grid_size + candidate_domain) for precomputed class costs, O(Rx*Ry*Rz*boxes) for compressed cell-versus-object testing, O(N*K) for a one-dimensional
- Space: Use O(number_of_classes * state_domain), O(N + K), or O(active_grid + padding) whenever the problem structure permits. Retain O(HW) only when storing the output or dense DP state is necessary. Replace duplicate full grids, temporary

## Pitfalls
- Do not assume a compact sweep is always asymptotically faster. Compare O(nk) with O(k^2), and compare cell-versus-box testing with painted-cell updates using actual density.
- Do not remove required output storage when the output itself is Theta(HW) or Theta(answer_size). The optimization is usually fewer intermediate buffers and passes, not sub-output memory.
- Deduplicate compressed coordinates and stop cell loops at unique_count - 1; otherwise zero-width cells, inflated bounds, and off-by-one accesses are likely.
- Do not use linear coordinate remapping inside hot loops when lower_bound or a direct value-to-rank map is available.
- Do not rely on stale global arrays, accidental zero initialization, toroidal modulo addressing, or synthetic sentinel states without documenting and enforcing the invariant.
- Clear all indices that can be read, including padding and n+1 sentinels, across test cases.
- Avoid in-place mutation when later computations interpret the original grid or neighboring state; preserve a source map or use separate output state.
- Do not replace structural validation with aggregate counts. Cell totals do not imply connectivity, contiguity, alignment, or a valid path.

## When not to use
- The candidate-dependent computation is genuinely non-additive or depends on interactions that class frequencies cannot represent.
- Objects are sparse and tiny, making direct painting substantially cheaper than testing every compressed cell against every object.
- The periodic sweep has O(NK) time but K is large enough that the original O(K^2) or another data structure is preferable.
- The full spatial history affects future operations, so local cascades cannot be summarized by a bounded state or event count.
- The state domain is not small enough for precomputed transitions or exhaustive candidate enumeration.
- The output requires online decisions or immediate interaction, preventing buffering or direct construction.

## Minimal example
Before:
```cpp
// O015 focus: replace
vector<long long> vals;
for (int x : data) vals.push_back(transform(x));
long long ans = accumulate(vals.begin(), vals.end(), 0LL);
```
After:
```cpp
// optimized for replace
long long ans = 0;
for (int x : data)
  ans += transform(x);
// single-pass aggregate
```
