---
skill_id: O001
type: operator
language: python
family: constant_factor
name: Python Hot Path and I/O Constant Factor Optimization
description: Reusable optimization pattern distilled from weighted traces.
tags:
- python-optimization
- constant-factors
- fast-input
- buffered-output
- allocation-reduction
- hot-loop
- greedy
- sorting
- array-scan
- range-query
triggers:
- The slow and fast variants use the same data structure, traversal count, and asymptotic algorithm.
- Numeric input is parsed with eval, exec, repeated conversions, or unbuffered input calls.
- Large inputs are processed with input() or repeated per-item parsing.
- Output is printed once per query or answer instead of being buffered.
- A hot path creates slices, reversed copies, sorted copies, tuples, or other temporary collections.
- A loop uses repeated pop, len, attribute lookup, function calls, or complex expression-level control flow.
- A generator, comprehension, or builtin is used in a performance-critical path where a simple scalar loop may be cheaper.
- Queries are stored eagerly even though each can be processed online.
---

## When to use
- The slow and fast variants use the same data structure, traversal count, and asymptotic algorithm.
- Numeric input is parsed with eval, exec, repeated conversions, or unbuffered input calls.
- Large inputs are processed with input() or repeated per-item parsing.
- Output is printed once per query or answer instead of being buffered.
- A hot path creates slices, reversed copies, sorted copies, tuples, or other temporary collections.
- A loop uses repeated pop, len, attribute lookup, function calls, or complex expression-level control flow.
- A generator, comprehension, or builtin is used in a performance-critical path where a simple scalar loop may be cheaper.
- Queries are stored eagerly even though each can be processed online.

## Steps
1. Confirm correctness and identify the true bottleneck before changing code; distinguish I/O, sorting, allocation, Python-loop overhead, output growth, and algorithmic cost.
2. Preserve the original invariant and algorithmic class unless a separately justified asymptotic improvement exists.
3. Replace eval(input()), int(eval( )), and exec-based parsing with direct int(), map(int, ), or a controlled bulk tokenizer.
4. For many small tokens, bind sys.stdin.readline or use sys.stdin.buffer.read().split() when bulk tokenization is memory-safe and appropriate.
5. Replace slice-based selection such as every-second-element slices with direct indexed accumulation or iteration over the required positions.
6. Avoid structural mutation and sentinel objects when explicit indices, counters, or pointers express the state more cheaply and clearly.
7. Precompute invariant quantities outside hot loops, including parsed scalars, squares, bounds, constants, and deterministic factors.
8. Rewrite opaque arithmetic control flow, repeated powers, boolean coercions, and redundant conversions as explicit branches and scalar updates.

## Complexity
- Time: Usually unchanged: preserve the original bound, commonly O(n), O(n log n), O((n + q) log n), or O((n + m) log(n + m)). The goal is lower constants; eliminate accidental quadratic behavior such as repeated immutable-container growth.
- Space: (pattern dependent)

## Pitfalls
- Assuming a file labeled fast is actually faster; a rewrite can regress from linear time to sorting time.
- Changing the greedy ordering, tie behavior, segment counts, or accumulation invariant while only intending a micro-optimization.
- Replacing a one-pass constant-space scan with list materialization and an extra pass.
- Using eval for convenience; it is slower, unsafe, and unnecessary for numeric input.
- Using sys.stdin.buffer.read().split() when input size makes token materialization exceed memory limits.
- Creating full copies through sorted, reverse slices, strided slices, comprehensions, or intermediate maps.
- Using tuple concatenation, string concatenation, or repeated print calls in large output loops.
- Over-optimizing builtins without measurement; explicit loops are not universally faster than sum, max, comprehensions, or generator expressions.

## When not to use
- The real bottleneck is an incorrect asymptotic algorithm, such as nested scans over large query and data sets.
- A valid asymptotic redesign, specialized data structure, vectorization strategy, or compiled implementation is required.
- Input is small enough that readability dominates performance concerns.
- Memory limits make bulk input tokenization, full arrays, or buffered outputs unsafe.
- The existing algorithm is already optimal and profiling shows no meaningful overhead in the targeted operation.
- A rewrite would add extra passes, sorting, or retained state without measured benefit.

## Minimal example
Before:
```py
import sys
n = int(eval(sys.stdin.readline()))
weights = sorted(eval(sys.stdin.readline()), reverse=True)
score = weights[0]
for i in range(2, n): score += weights[i // 2]
print(score)
```
After:
```py
import sys
values = list(map(int, sys.stdin.buffer.read().split()))
n, weights = values[0], sorted(values[1:1 + n], reverse=True)
score = weights[0]
for i in range(2, n): score += weights[i // 2]
sys.stdout.write(f"{score}\n")
```
