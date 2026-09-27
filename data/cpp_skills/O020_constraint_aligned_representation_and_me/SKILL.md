---
skill_id: O020
type: operator
language: cpp
family: coprimality
name: Constraint Aligned Representation and Memory Safe C++ Optimization
description: Preserve the proven algorithm while making its numeric model, storage layout, and hot-path representation match
  the real constraints. Eliminate undefined behavior, widen only overflow-prone arithmetic, narrow bounded state and container
  fields, use contiguous correctly sized storage, and replace brittle fixed-width tricks with transparent formulas when the
  input domain is wider. This skill commonly restores
tags:
- implementation
- correctness
- undefined-behavior
- integer-width
- overflow
- memory-layout
- cache-locality
- constant-factor
- dynamic-programming
- bit-counting
triggers:
- 'A solution uses #define int long long throughout the program.'
- Products, cumulative sums, LCMs, combinatorial counts, distances, or DP accumulators may exceed 32-bit range.
- The stored type is narrower than the input domain, or multiplication occurs before promotion.
- reserve() is followed by operator[] writes without resize() or push_back().
- A variable-length array or large local array is used for input-sized storage.
- Array dimensions, branch bounds, loop limits, or bitmask ranges disagree.
- A fixed bit width such as 20 is used although inputs are 64-bit or a paired implementation processes about 60 bits.
- Bit-packing constants encode a narrow lane width or other assumptions that do not cover the full domain.
---

## When to use
- A solution uses #define int long long throughout the program.
- Products, cumulative sums, LCMs, combinatorial counts, distances, or DP accumulators may exceed 32-bit range.
- The stored type is narrower than the input domain, or multiplication occurs before promotion.
- reserve() is followed by operator[] writes without resize() or push_back().
- A variable-length array or large local array is used for input-sized storage.
- Array dimensions, branch bounds, loop limits, or bitmask ranges disagree.
- A fixed bit width such as 20 is used although inputs are 64-bit or a paired implementation processes about 60 bits.
- Bit-packing constants encode a narrow lane width or other assumptions that do not cover the full domain.

## Steps
1. Infer actual bounds for every input, index, count, sum, product, DP state, bit position, and output value before changing code.
2. Delete global integer-width macros. Introduce explicit aliases such as int, int64_t, or long long and assign widths by semantic range.
3. Keep indices, dimensions, node IDs, small coordinates, frequencies, DP cells under a safe modulus, and compact container payloads narrow when proven safe.
4. Use 64-bit arithmetic end-to-end for cumulative sums, products, LCM/gcd intermediates, pair counts, answers, distances, and movement or scheduling totals.
5. Force promotion before multiplication with a 64-bit operand or cast, rather than widening only the destination variable.
6. Match input and output interfaces to the selected types, including scanf/printf format specifiers and stream types.
7. Replace VLAs and stack-heavy buffers with correctly sized vectors, static storage, or heap-backed contiguous arrays.
8. Remember that reserve() changes capacity only; use resize(), sized construction, or push_back() before indexed access.

## Complexity
- Time: Usually unchanged: O(n), O(n log n), O(nS), O(n2^k), or O(2^k k) depending on the preserved algorithm. Representation fixes reduce constants and restore predictable behavior. Full-width bit contribution is typically O(nB), with B about
- Space: Usually unchanged in asymptotic order, but often substantially smaller after selective narrowing and contiguous storage. Typical forms remain O(n), O(S), or O(2^k k). Full-width bit aggregation can use O(B) auxiliary counters or O(n + B)

## Pitfalls
- Widening only the result variable does not prevent overflow in an intermediate expression evaluated as int.
- Replacing every int with long long can increase memory traffic, cache misses, sort cost, container size, and register pressure.
- reserve() does not construct elements and cannot make a[i] valid.
- Out-of-bounds writes may appear as slowness, unstable timing, or corrupted data rather than an immediate crash.
- A fixed array bound must cover the maximum valid index, not merely the common case.
- A VLA may compile as a compiler extension but remains non-standard and risks stack exhaustion.
- Packed-lane arithmetic is fragile: lane width, masks, shifts, and overflow margins must all remain valid when constraints change.
- Do not divide by two in a pair-count formula if the direct formula already counts unordered pairs; do divide when accumulating ordered pairs.

## When not to use
- Do not apply selective narrowing without proven upper bounds for every use and intermediate expression.
- Do not replace a genuinely suboptimal algorithm with representation tuning; first fix an avoidable O(n2), exponential, or repeated logarithmic bottleneck.
- Do not use 32-bit modular storage when the modulus, unreduced states, or multiplication bounds exceed its safe range.
- Do not use fixed-size arrays when input limits are unknown or can exceed the allocated capacity.
- Do not use packed arithmetic when the value width, lane capacity, or overflow margin is uncertain.
- Do not add custom parsers, formatters, or compiler pragmas for tiny input or output workloads.

## Minimal example
Before:
```cpp
// O020 focus: constraint
bool pairwise = true;
for (int i = 0; i < n; ++i)
  for (int j = i + 1; j < n; ++j)
    if (std::gcd(a[i], a[j]) != 1) pairwise = false;
```
After:
```cpp
// optimized for constraint
auto spf = build_spf(*max_element(a.begin(), a.end()));
vector<int> seen(spf.size(), 0);
for (int x : a)
  for (int p : distinct_prime_factors(x, spf))
    if (seen[p]++) pairwise = false;
```
