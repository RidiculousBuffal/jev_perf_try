---
skill_id: O022
type: operator
language: cpp
family: dp
name: Compress String State into Linear Invariants
description: When a C++ solution repeatedly mutates strings, rescans prefixes, builds temporary buffers, or explores equivalent
  local decisions, derive the smallest sufficient state instead. Use counters for cancellation and run-counting problems,
  endpoint classes for concatenation effects, direct two-pointer checks for symmetric predicates, and closed-form parity or
  boundary invariants for reducible simulations. If the
tags:
- C++
- competitive-programming
- strings
- greedy
- state-compression
- invariant
- linear-scan
- dynamic-programming
- reconstruction
- simulation
triggers:
- A loop repeatedly deletes, erases, compacts, or rebuilds a string.
- The same prefix or suffix is rescanned after each operation.
- A stack or vector stores only unmatched occurrences whose exact identities are irrelevant.
- A temporary array or transformed string is created although only its length, count, or endpoints are used.
- The answer depends only on run boundaries, endpoint characters, character counts, or parity.
- A concatenation objective creates effects only across adjacent string boundaries.
- A full reverse, remap, copy, and compare is used for a symmetric predicate.
- A supposedly local wildcard replacement affects future score or feasibility.
---

## When to use
- A loop repeatedly deletes, erases, compacts, or rebuilds a string.
- The same prefix or suffix is rescanned after each operation.
- A stack or vector stores only unmatched occurrences whose exact identities are irrelevant.
- A temporary array or transformed string is created although only its length, count, or endpoints are used.
- The answer depends only on run boundaries, endpoint characters, character counts, or parity.
- A concatenation objective creates effects only across adjacent string boundaries.
- A full reverse, remap, copy, and compare is used for a symmetric predicate.
- A supposedly local wildcard replacement affects future score or feasibility.

## Steps
1. State the required observable result and discard intermediate objects that are never exposed.
2. Identify the invariant: unmatched count, run count, endpoint category, parity, last-character state, or another minimal sufficient summary.
3. Replace repeated deletion or stack mutation with a monotone one-pass counter; update the final value directly from matched pairs or transitions.
4. For run-length tasks, scan with one index and current-run counters; make bounds checks occur before every access and avoid open-ended loops.
5. For concatenation tasks, count internal contributions while reading each string and classify only the relevant first/last-character buckets.
6. For symmetry or involutive mappings, compare mirrored positions directly with two pointers and exit on the first violation.
7. For closed-form games or simulations, derive the terminal invariant such as parity plus endpoint relation and remove state mutation entirely.
8. When choices depend on history, define DP over position plus the smallest context state; memoize or iterate over the resulting constant-size state graph.

## Complexity
- Time: Usually O(N) for a single string or total input size, with O(1) extra-state greedy/invariant solutions. Finite-state DP with reconstruction remains O(N * S), where S is the small state count. Boundary-counting and closed-form decisions
- Space: Prefer O(1) auxiliary space when only counters or endpoints are needed. Use O(N) space when reconstruction, stored operations, occurrence positions, or a DP table is required. Avoid retaining all input strings when each can be classified

## Pitfalls
- Replacing an optimization problem with a fast but incorrect unconditional greedy substitution.
- Dropping a history bit that changes transition rewards or future feasibility.
- Using local greedy choices without proving the invariant or checking the limited necessary lookahead.
- Using a stack when only its size or one unmatched-symbol count matters.
- Building a compressed or transformed buffer when only its final length or a Boolean answer is required.
- Recomputing boundary formulas from raw indices instead of normalizing segment lengths once.
- Calling strlen on an unterminated output buffer or ignoring the declared input length.
- Writing conditions such as s[i] == c && i < n, which reads out of bounds because operands are evaluated left to right.

## When not to use
- Do not compress state unless the proposed invariant is proved to preserve every future-relevant distinction.
- Do not replace a genuine context-dependent objective with an unconditional character-wise greedy rule.
- Do not force a closed form when arbitrary transitions, weights, or constraints make the state nonlocal.
- Do not stream input if later decisions require random access, suffix lookahead, reconstruction, or offline sorting.
- Do not trade a safe standard container for a fixed buffer without a guaranteed bound and explicit termination handling.
- Do not optimize I/O or template size before eliminating quadratic mutation, rescanning, or exponential search.

## Minimal example
Before:
```cpp
string reduce(string s) {
    bool changed = true;
    while (changed) {
        changed = false;
        for (size_t i = 1; i < s.size(); ++i)
            if (s[i] == s[i - 1]) { s.erase(i - 1, 2); changed = true; break; }
    }
    return s;
}
```
After:
```cpp
string reduce(string_view s) {
    string state;
    for (char c : s)
        if (!state.empty() && state.back() == c) state.pop_back();
        else state.push_back(c);
    return state;
}
```
