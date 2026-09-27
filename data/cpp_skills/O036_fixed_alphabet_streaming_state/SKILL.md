---
skill_id: O036
type: operator
language: cpp
family: streaming
name: Fixed Alphabet Streaming State
description: Optimize string and small-universe checks by replacing sorting, pair materialization, repeated preprocessing,
  mutation, reversal, and indirect searches with direct-address tables and one-pass state machines. When the alphabet or encoded
  key universe is bounded, use std::array or correctly sized flat tables for predictable cache-friendly access. Express the
  actual invariant directly, validate mappings in both
tags:
- C++
- strings
- fixed-alphabet
- direct-addressing
- frequency-counting
- bijection-check
- streaming
- finite-state-scan
- early-exit
- constant-factor-optimization
triggers:
- The input symbols come from a small fixed alphabet relative to the string length.
- Sorting aligned character pairs is used only to group equal keys before checking consistency.
- A map, frequency signature, or lookup can be represented by an indexed table.
- A reverse, temporary buffer, or in-place character remapping exists only to simplify later comparison.
- Synthetic marker characters encode multi-character tokens before counting or scanning.
- The property depends on local adjacency, a bounded lookahead window, or a few running counters.
- A direct-address table is reused across multiple datasets without explicit clearing.
- Character values are used directly as array indices, especially when plain char may be signed.
---

## When to use
- The input symbols come from a small fixed alphabet relative to the string length.
- Sorting aligned character pairs is used only to group equal keys before checking consistency.
- A map, frequency signature, or lookup can be represented by an indexed table.
- A reverse, temporary buffer, or in-place character remapping exists only to simplify later comparison.
- Synthetic marker characters encode multi-character tokens before counting or scanning.
- The property depends on local adjacency, a bounded lookahead window, or a few running counters.
- A direct-address table is reused across multiple datasets without explicit clearing.
- Character values are used directly as array indices, especially when plain char may be signed.

## Steps
1. Identify the minimal invariant: frequency counts, source-to-target consistency, reverse injectivity, mirrored compatibility, or a small streaming automaton.
2. Exploit bounded domains with std::array<int, 26>, std::array<int, 256>, or another table sized from the actual universe; use maps only when the domain is genuinely large or sparse.
3. For character mappings, initialize integer tables to -1, index with static_cast<unsigned char>(c), and validate one direction at a time; reset and validate the reverse direction when bijection is required.
4. For frequency conditions, count in one pass and compare the direct invariant, such as max(counts) - min(counts) <= 1, instead of normalizing counts through indirect arithmetic.
5. Replace sorting-based grouping with direct table updates and immediate mismatch detection.
6. Replace synthetic-token preprocessing, reversal, and destructive mutation with a forward finite-state scan that recognizes multi-character tokens using lookahead.
7. Replace transformed-copy comparisons with direct mirrored or offset comparisons, scanning only the necessary half or valid index range.
8. Cache the input length once through std::string::size() or length(); avoid strlen when a string object already tracks the size.

## Complexity
- Time: (pattern dependent)
- Space: Typically O(1) auxiliary space for a fixed alphabet, using tables of size O(A) or O(256), with A independent of n. Direct-address encoded dictionaries use O(U) memory. Use O(n) only when storage is required by the problem or when a

## Pitfalls
- Do not claim an asymptotic improvement when replacing one linear implementation with another; the gain is usually constant-factor or correctness-related.
- Do not index arrays with plain char without converting to unsigned char; signed char can produce negative indices.
- Do not allocate 255 entries for a byte alphabet; use 256 entries or a wider domain-specific table.
- Do not read s[i + 1] or s[i + window] before proving the index is valid. Conditions must test bounds before data access.
- Do not rely on zero-initialized slack bytes, overwritten null terminators, or accidental buffer padding as implicit safety.
- Do not use a sentinel that can occur in valid input unless the state representation distinguishes it explicitly.
- Do not forget the reverse mapping check when the requirement is bijection rather than merely a functional source-to-target mapping.
- Do not silently ignore characters outside the assumed alphabet unless that behavior is specified and intentional.

## When not to use
- The alphabet or key universe is large, dynamic, or too sparse for a practical direct-address table.
- The task depends on global ordering, rank, or arbitrary comparisons where sorting is semantically necessary.
- Frequency signatures discard positional information required by the specification.
- A streaming automaton cannot retain enough state to represent the required history.
- A sentinel cannot be chosen outside the valid input domain or safe capacity cannot be proven.
- The table-clearing cost O(U) dominates and timestamped sparse resets or hash-based storage would be more appropriate.

## Minimal example
Before:
```cpp
// O036 focus: fixed
vector<long long> vals;
for (int x : data) vals.push_back(transform(x));
long long ans = accumulate(vals.begin(), vals.end(), 0LL);
```
After:
```cpp
// optimized for fixed
long long ans = 0;
for (int x : data)
  ans += transform(x);
// single-pass aggregate
```
