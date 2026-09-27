---
skill_id: O034
type: operator
language: cpp
family: graph
name: Invariant Driven Linearization and State Simplification
description: Recognize when an optimization implementation is already linear but obscured by repeated scans, branch-heavy
  casework, mutable rolling state, or unnecessary simulation. Derive the governing invariant or separable formula, then express
  the solution as a simple scan, prefix-sum query, sliding-window update, chain decomposition, cycle-index lookup, or constant-time
  arithmetic formula. Prefer deterministic control
tags:
- optimization
- invariants
- greedy
- math
- closed-form
- prefix-sum
- sliding-window
- single-pass
- state-machine
- sequence-segmentation
triggers:
- A nested scan only searches for the next unequal element or next direction change.
- The objective depends on adjacent comparisons, while equal neighbors are neutral.
- A mutable rolling state mixes window sums, positive contributions, and entering/leaving updates whose invariants are difficult
  to verify.
- A fixed-length contiguous segment is evaluated against its complement.
- The score can be separated into an inside-window term and prefix/suffix or outside-window terms.
- Sorted coordinates are processed with sign-specific cases around zero or another breakpoint.
- A monotonic queue or range-minimum structure is rebuilt for every candidate size even though successive states differ incrementally.
- A bounded precomputation loop accumulates a recognizable arithmetic, geometric, or expectation formula.
---

## When to use
- A nested scan only searches for the next unequal element or next direction change.
- The objective depends on adjacent comparisons, while equal neighbors are neutral.
- A mutable rolling state mixes window sums, positive contributions, and entering/leaving updates whose invariants are difficult to verify.
- A fixed-length contiguous segment is evaluated against its complement.
- The score can be separated into an inside-window term and prefix/suffix or outside-window terms.
- Sorted coordinates are processed with sign-specific cases around zero or another breakpoint.
- A monotonic queue or range-minimum structure is rebuilt for every candidate size even though successive states differ incrementally.
- A bounded precomputation loop accumulates a recognizable arithmetic, geometric, or expectation formula.

## Steps
1. First verify whether the baseline is already asymptotically optimal; do not label an I/O or cosmetic rewrite as an algorithmic speedup.
2. Write down the exact invariant and the minimal information needed to update or score the next candidate.
3. For local monotonic behavior, compute adjacent differences, ignore zero differences, retain only the last nonzero sign, and count reversals.
4. For fixed windows, use a rolling recurrence such as sum += entering - leaving; use a ring buffer only when full-array storage is unnecessary.
5. For window/complement objectives, build prefix sums for each independent quantity, such as raw values and positive parts, then evaluate every window in O(1).
6. For sorted interval selection, replace sign-based case splits with one endpoint formula and scan all contiguous K-length windows.
7. For repeated range minima, reuse the previous candidate state with persistent per-position minima instead of rebuilding a deque or queue.
8. For bounded mathematical precomputation, replace nested summation with a closed form and keep the main scan unchanged.

## Complexity
- Time: Typically O(n) time for scans, prefix sums, window evaluation, trend detection, chain decomposition, or cycle preprocessing; O(1) per test case when a parity, deficit, or piecewise-linear formula applies. Preserve O(n^2) only when all
- Space: Usually O(n) auxiliary space for prefix arrays, cycle metadata, or explicit input storage. Reduce to O(1) or O(k) when the computation is streamable and no arbitrary range or future access is needed.

## Pitfalls
- Assuming a code labeled fast is algorithmically better when both versions perform the same linear work.
- Replacing efficient sliding-window logic with a more complicated structure without removing an actual bottleneck.
- Recomputing a range sum or complement contribution inside every candidate loop.
- Forgetting that positive-only prefixes and raw-sum prefixes represent different quantities.
- mishandling zero differences, plateaus, or the first nonzero trend.
- Using sign-specific interval casework that misses all-negative, all-positive, or boundary windows.
- Resetting trend state incorrectly after a reversal and double-counting or missing a segment.
- Applying a closed form without proving the target feasibility, parity, or modular condition.

## When not to use
- Do not replace a correct simple O(n) algorithm with more elaborate invariant machinery when the constraints already make it sufficient.
- Do not force prefix sums when the objective is naturally streamable and O(k) memory matters.
- Do not collapse a search into a formula until the operation model, feasibility conditions, and edge cases are proven.
- Do not use endpoint-only window formulas unless the input ordering and objective guarantee contiguity and endpoint sufficiency.
- Do not reuse mutable state across candidate states when the transition is not monotone or the previous state does not contain all required information.
- Do not prefer branchless or custom-parser code when it reduces readability without measurable hot-path benefit.

## Minimal example
Before:
```cpp
// O034 focus: invariant
vector<vector<int>> g(n, vector<int>(n, 0));
for (auto [u, v] : edges) g[u][v] = 1;
queue<int> q;
q.push(0);
```
After:
```cpp
// optimized for invariant
vector<vector<int>> adj(n);
for (auto [u, v] : edges) adj[u].push_back(v);
deque<int> q{0};
auto ans = topo_dp(adj);
```
