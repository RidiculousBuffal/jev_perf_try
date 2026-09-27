---
skill_id: O043
type: operator
language: python
family: combinatorics
name: Incremental Constraint Propagating Search
description: Replace generate-and-test enumeration, repeated global lookups, or restart-heavy grid DFS with a direct state
  representation, one-time structural preprocessing, and incremental constraint checks. Represent only the information needed
  to make the next decision, apply fixed requirements before branching, reject invalid partial states immediately, and undo
  changes on backtracking. For fixed-size boards, use explicit
tags:
- backtracking
- constraint-satisfaction
- incremental-validation
- constraint-propagation
- pruning
- state-representation
- grid-search
- board-search
- simulation
- preprocessing
triggers:
- Permutations or full candidate generation are followed by validation only at complete assignments.
- A validator repeatedly scans the whole board or compares every pair at recursion leaves.
- Fixed or required positions are enforced only after a candidate is fully constructed.
- Rows, columns, diagonals, or other exclusion rules can be tracked with occupancy arrays, sets, or bitmasks.
- Recursive grid search starts independently from many cells and repeats exploration across the same component.
- Grid DFS marks and restores cells but uses little structural information for pruning.
- Repeated list.index, reverse lookup, or global token-index arithmetic is used for board queries.
- A small fixed board has explicit rows, columns, diagonals, or winning patterns that can be checked directly.
---

## When to use
- Permutations or full candidate generation are followed by validation only at complete assignments.
- A validator repeatedly scans the whole board or compares every pair at recursion leaves.
- Fixed or required positions are enforced only after a candidate is fully constructed.
- Rows, columns, diagonals, or other exclusion rules can be tracked with occupancy arrays, sets, or bitmasks.
- Recursive grid search starts independently from many cells and repeats exploration across the same component.
- Grid DFS marks and restores cells but uses little structural information for pruning.
- Repeated list.index, reverse lookup, or global token-index arithmetic is used for board queries.
- A small fixed board has explicit rows, columns, diagonals, or winning patterns that can be checked directly.

## Steps
1. Preserve the external input/output contract and identify the true decision variables.
2. Choose a compact state model, such as row-to-column assignments, occupancy markers, a visited mask, or direct board cells.
3. Separate immutable requirements from mutable search state; preprocess fixed positions, occupied resources, neighbor metadata, or winning lines.
4. Validate fixed requirements against one another before starting the search.
5. Order decisions so that each recursion level handles one logical unit, such as one row or one component.
6. Restrict candidates immediately when a variable has a forced value or when preprocessing identifies a forced or low-branching move.
7. Test all local constraints before descending: use O(1) membership checks, bit operations, or direct neighboring-cell tests.
8. Commit a candidate, update only the affected state, recurse, then undo the update exactly on backtrack.

## Complexity
- Time: For a generic constraint search, worst-case time remains exponential or factorial in the number of decisions, often O(b^d) or O(n!), but incremental legality checks are typically O(1) per candidate and early propagation greatly reduces
- Space: Typically O(n) to O(n^2) for assignments, occupancy markers, fixed constraints, and optional metadata; grid preprocessing uses O(HW). Recursive depth is O(n) or O(HW), excluding any explicit visited structure.

## Pitfalls
- Changing from permutations to backtracking without actually moving validation before recursion.
- Applying constraints incrementally but forgetting to undo every mutation on failure.
- Initializing occupancy from fixed placements without checking whether those placements already conflict.
- Allowing a free choice in a row or variable that has a predetermined value.
- Using mixed booleans, strings, and numeric sentinels in the same state arrays.
- Keeping a full mutable board when a compact assignment vector is sufficient.
- Continuing recursion after printing or finding the first acceptable solution.
- Assuming local degree information alone eliminates all repeated simple-path exploration in a general graph.

## When not to use
- The search space is already small, fully enumerated once, and validation is negligible.
- Constraints are global, nonlocal, or difficult to maintain incrementally, so local checks cannot safely establish correctness.
- The problem requires all solutions or complete candidate statistics and early termination is unavailable.
- Preprocessing costs more than repeated traversal for the actual input sizes.
- The grid graph has large, complex connectivity where local degree counts do not provide sound pruning.
- A closed-form or dynamic-programming formulation provides a stronger guaranteed improvement.

## Minimal example
Before:
```py
from itertools import permutations
n = 8
solutions = []
for p in permutations(range(n)):
    if all(abs(p[i] - p[j]) != j - i for i in range(n) for j in range(i + 1, n)):
        solutions.append(p)
```
After:
```py
n = 8
solutions = []
def search(row, cols, diag1, diag2, path):
    if row == n: solutions.append(tuple(path)); return
    available = ((1 << n) - 1) & ~(cols | diag1 | diag2)
    while available:
        bit = available & -available; available -= bit
        search(row + 1, cols | bit, (diag1 | bit) << 1, (diag2 | bit) >> 1, path + [bit.bit_length() - 1])
search(0, 0, 0, 0, [])
```
