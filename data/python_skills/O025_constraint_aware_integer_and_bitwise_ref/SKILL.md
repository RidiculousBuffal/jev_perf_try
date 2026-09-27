---
skill_id: O025
type: operator
language: python
family: combinatorics
name: Constraint Aware Integer and Bitwise Reformulation
description: Replace representation-heavy, input-scaled, or redundant searches with direct integer arithmetic, bitwise contribution
  counting, mathematically justified bounds, incremental accumulation, and early termination. First identify the underlying
  invariant or monotone structure, then eliminate binary-string conversion, repeated scans, duplicated exponentiation, unnecessary
  state materialization, and avoidable I/O. Choose
tags:
- integer-arithmetic
- bitwise
- bit-length
- perfect-powers
- bounded-enumeration
- early-termination
- prefix-counting
- combinatorial-counting
- incremental-accumulation
- I/O-optimization
triggers:
- Binary strings are created only to obtain bit length, inspect bits, reverse bits, or find the least significant set bit.
- A loop repeatedly divides by two and later converts the iteration count into a power-of-two or all-ones result.
- A geometric sum such as 2^k - 1 is computed indirectly from a separately measured depth.
- A nested search enumerates bases and exponents even though powers grow monotonically and exceed the bound quickly.
- The minimum exponent is two, so any valid base must satisfy base^2 <= limit.
- A maximum-under-bound query builds, deduplicates, sorts, and searches a complete candidate list despite requiring only one
  extremum.
- The same exponentiation or aggregate count is evaluated repeatedly in a loop condition and update expression.
- A pairwise XOR-like aggregate decomposes independently by bit position.
---

## When to use
- Binary strings are created only to obtain bit length, inspect bits, reverse bits, or find the least significant set bit.
- A loop repeatedly divides by two and later converts the iteration count into a power-of-two or all-ones result.
- A geometric sum such as 2^k - 1 is computed indirectly from a separately measured depth.
- A nested search enumerates bases and exponents even though powers grow monotonically and exceed the bound quickly.
- The minimum exponent is two, so any valid base must satisfy base^2 <= limit.
- A maximum-under-bound query builds, deduplicates, sorts, and searches a complete candidate list despite requiring only one extremum.
- The same exponentiation or aggregate count is evaluated repeatedly in a loop condition and update expression.
- A pairwise XOR-like aggregate decomposes independently by bit position.

## Steps
1. State the mathematical quantity being computed independently of the current implementation.
2. Determine whether the result depends on bit length, individual bit contributions, monotone powers, a maximum under a bound, or repeated output structure.
3. Replace binary-string inspection with integer operations: bit_length(), shifts, masks, trailing-zero arithmetic, or running powers of two.
4. If a loop count is immediately transformed into a geometric expression, fuse counting and accumulation using a running term; include the terminal contribution explicitly.
5. For perfect-power search, initialize the answer to the smallest valid fallback, bound bases by floor_sqrt(limit) when exponents start at two, and break exponent growth as soon as the current power exceeds the limit.
6. Compute each candidate power once per iteration; preferably update it incrementally by multiplication rather than recomputing exponentiation.
7. If the documented input bound is genuinely tiny, replace input-scaled loops with constraint-derived fixed bounds, but retain early breaks and document the assumption.
8. For pairwise bitwise aggregates, count each bit independently. Use count_ones * count_zeros for XOR-like pair differences and multiply by the bit weight.

## Complexity
- Time: Typical improvements preserve the underlying bound while reducing constants: O(log n) for bit-length or halving processes, O(B) for fixed-width bit operations, O(nB) for bitwise array aggregates, and O(sqrt(n) log n) or tighter
- Space: Prefer O(1) auxiliary space for streaming arithmetic, bit decomposition, and bounded searches. Bitwise pair aggregation can use O(B) global counts; prefix/suffix formulations require O(nB). Batched structured output may use O(n) transient

## Pitfalls
- Using string conversion when bit_length(), shifts, masks, or trailing-zero operations suffice.
- Using floating-point logarithms or square roots for exact integer bounds without verifying rounding safety.
- Recomputing a**b in both a loop condition and the loop body.
- Replacing a general algorithm with fixed bounds without proving that the constraints guarantee those bounds.
- Assuming a prefix-count formulation is faster merely because it is more elaborate; it may have the same asymptotic time and substantially higher memory use.
- Using a fixed bit width that is too small, or deriving width from max(values) when negatives or a prescribed machine width are possible.
- Building and sorting all candidates for a single maximum query.
- Forgetting duplicate generation when the same perfect power has multiple base/exponent representations.

## When not to use
- Do not replace a clear general algorithm with fixed enumeration when input limits are unknown, variable, or potentially large.
- Do not use prefix tables when a global per-bit count gives the same result with less memory and simpler code.
- Do not force integer bit tricks when the task depends on textual formatting, arbitrary-precision digit semantics, or non-binary representations.
- Do not optimize representation overhead before addressing a genuinely superlinear algorithmic bottleneck.
- Do not batch output if the required interface depends on streaming, interactive feedback, or strict incremental flushing.
- Do not rely on fixed-width bit arithmetic without explicitly defining behavior for negatives and values beyond the chosen width.

## Minimal example
Before:
```py
# O025 focus: constraint
cnt = 0
for a in range(1, n+1):
    for b in range(1, n+1):
        for c in range(1, n+1):
            if a + b + c == S: cnt += 1
```
After:
```py
# optimized for constraint
cnt = 0
for a in range(1, n+1):
    lo = max(1, S-a-n); hi = min(n, S-a-1)
    if lo <= hi: cnt += (hi - lo + 1)
```
