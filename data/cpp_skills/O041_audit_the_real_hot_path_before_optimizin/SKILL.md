---
skill_id: O041
type: operator
language: cpp
family: constant_factor
name: Audit the Real Hot Path Before Optimizing
description: A C++ optimization-audit skill for paired slow/fast snippets that are identical, truncated, or limited to template
  and macro scaffolding. Do not infer an algorithmic speedup from headers, pragmas, macros, typedefs, or compiler flags alone.
  First require the complete executable path, then compare asymptotics, data structures, allocation behavior, I/O, and debug
  code. Apply constant-factor tuning only after a genuine
tags:
- c++
- competitive-programming
- performance-audit
- incomplete-source
- paired-optimization
- hot-path-analysis
- debug-output
- fast-io
- container-choice
- compile-time-hygiene
triggers:
- The slow and fast snippets are identical in the visible region.
- The source is truncated before main(), solve(), input parsing, or algorithm-specific helpers.
- Only headers, typedefs, macros, debug utilities, or template boilerplate are visible.
- No loops, recursion, state transitions, container operations, sorting, traversal, or query processing can be inspected.
- The reported complexity change is unknown, unchanged, or unsupported by the supplied code.
- Debug macros, string formatting, stringstream, cerr/cout, or endl may be enabled in omitted hot paths.
- Heavy standard-library headers or PBDS/rope inclusions suggest compile-time bloat rather than runtime cost.
- Global widening such as defining int as long long may affect memory traffic, but its relevance depends on unseen data sizes
  and loops.
---

## When to use
- The slow and fast snippets are identical in the visible region.
- The source is truncated before main(), solve(), input parsing, or algorithm-specific helpers.
- Only headers, typedefs, macros, debug utilities, or template boilerplate are visible.
- No loops, recursion, state transitions, container operations, sorting, traversal, or query processing can be inspected.
- The reported complexity change is unknown, unchanged, or unsupported by the supplied code.
- Debug macros, string formatting, stringstream, cerr/cout, or endl may be enabled in omitted hot paths.
- Heavy standard-library headers or PBDS/rope inclusions suggest compile-time bloat rather than runtime cost.
- Global widening such as defining int as long long may affect memory traffic, but its relevance depends on unseen data sizes and loops.

## Steps
1. Reject any claimed runtime or asymptotic delta that is not visible in executable code.
2. Request or recover the complete slow and fast implementations, especially main(), solve(), input/output, core loops, helpers, and data-structure declarations.
3. Diff the first meaningful executable divergence rather than the shared template.
4. Compare asymptotics first: nested-loop elimination, repeated-query reduction, preprocessing, sorting plus binary search, prefix sums, hashing, heaps, offline processing, memoization, graph pruning, or DP state compression.
5. Compare data-structure and memory behavior next: vector or array versus map/set, unordered-container reservation, repeated sorting, allocation frequency, cache locality, copying, and iterator invalidation.
6. Audit repeated helper work such as linear modular-combination products, repeated scans, string construction, or recursive calls in hot loops; precompute or reuse results where valid.
7. Audit I/O: use ios::sync_with_stdio(false) and cin.tie(nullptr) for heavy iostream workloads, avoid mixing stdio and iostreams carelessly, and avoid endl or flushing in hot paths.
8. Compile-time-disable or remove debug logging from release paths. Avoid ostream formatting, stringstream, to_string, tokenization, and temporary string concatenation inside performance-critical loops.

## Complexity
- Time: (pattern dependent)
- Space: Not determinable from incomplete snippets. Header count and macro volume do not imply runtime memory usage. Compute space from the complete data structures, DP states, buffers, recursion depth, and preprocessing tables.

## Pitfalls
- Inventing an O(n^2) to O(n log n) improvement when the algorithm body is missing.
- Treating <bits/stdc++.h>, include changes, pragma optimize directives, or macro refactoring as algorithmic improvements.
- Confusing header and template bloat, which primarily affects compilation, with runtime complexity.
- Assuming debug macros are costly without verifying that they expand and execute on the hot path.
- Using unordered_map without considering worst-case behavior, hashing cost, reserve(), or key bounds.
- Replacing map with unordered_map or vector without preserving ordering, iterator, duplicate-key, or worst-case guarantees.
- Globally widening int to long long and overlooking cache density, memory traffic, or overflow requirements.
- Using fast-I/O settings inconsistently when mixing scanf/printf with cin/cout.

## When not to use
- The complete implementation and constraints are available and a concrete algorithmic pattern is already evident.
- The performance issue is proven to be external to the code, such as compiler configuration, hardware, or I/O environment.
- A profiler or benchmark already identifies a specific hot function and this skill would only repeat source-visibility checks.
- The task requires a domain-specific optimization whose correctness depends on problem semantics not represented in the source pair.

## Minimal example
Before:
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() { int n; cin >> n;
    for (int i = 0, x; i < n; ++i) { cin >> x; cout << "audit: " << x << endl; }
}
```
After:
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() { ios::sync_with_stdio(false); cin.tie(nullptr); int n; cin >> n;
    for (int i = 0, x; i < n; ++i) { cin >> x; cout << x << '\n'; }
}
```
