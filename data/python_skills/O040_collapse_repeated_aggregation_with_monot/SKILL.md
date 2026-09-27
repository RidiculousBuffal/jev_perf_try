---
skill_id: O040
type: operator
language: python
family: streaming
name: Collapse Repeated Aggregation with Monotone Prefix Sum Scans
description: Recognize when repeated slice sums, pair enumeration, small-state dynamic programs, or boundary rebalancing can
  be rewritten as prefix/suffix aggregates and monotone scans. Precompute or maintain cumulative totals, exploit nonnegative-value
  monotonicity for binary search and early termination, and replace local rolling logic with explicit reusable states when
  this improves correctness. Preserve streaming O(1) space
tags:
- prefix-sums
- suffix-sums
- rolling-aggregates
- dynamic-programming
- greedy
- binary-search
- two-pointers
- monotonicity
- pairwise-sums
- pairwise-differences
triggers:
- A loop repeatedly calls sum() on prefixes, suffixes, or slices.
- Candidate answers are formed by choosing a single cut, turn position, or boundary.
- A small-state DP recurrence repeatedly aggregates the same left or right ranges.
- A pairwise expression can be grouped by each element's contribution against a running prefix or suffix.
- Values are nonnegative or positive, so cumulative sums are monotone.
- A feasibility query asks for the largest prefix under a remaining budget.
- The valid candidates form a suffix or prefix, and failures cannot be repaired by later scanning.
- A moving split or balancing pointer advances monotonically.
---

## When to use
- A loop repeatedly calls sum() on prefixes, suffixes, or slices.
- Candidate answers are formed by choosing a single cut, turn position, or boundary.
- A small-state DP recurrence repeatedly aggregates the same left or right ranges.
- A pairwise expression can be grouped by each element's contribution against a running prefix or suffix.
- Values are nonnegative or positive, so cumulative sums are monotone.
- A feasibility query asks for the largest prefix under a remaining budget.
- The valid candidates form a suffix or prefix, and failures cannot be repaired by later scanning.
- A moving split or balancing pointer advances monotonically.

## Steps
1. Identify the repeated aggregate and express each candidate in terms of prefix, suffix, or running totals.
2. Choose between a streaming formulation and explicit tables: maintain totals for O(1) extra space, or build prefix/suffix arrays for random access across many cuts.
3. For a single transition position, compute the left prefix and right suffix incrementally and evaluate every position once.
4. For pairwise products, add each new value times the sum of preceding values, then update the running sum.
5. For pairwise distances on ordered values, replace sorting and pair enumeration with adjacent gaps, prefix gap distances, and left/right pair multiplicities.
6. For budgeted prefixes, build cumulative sums, use bisect_right on the other cumulative array, and convert the insertion index to an item count.
7. Before each binary search, stop when the current cumulative sum exceeds the budget; monotonicity proves later states are infeasible.
8. When the answer is a maximal valid suffix, scan from the right and break at the first failed boundary instead of resetting a left-to-right counter.

## Complexity
- Time: Typically O(n) after ordered input and cumulative preprocessing; O(n log n) if sorting is necessary; O(n log m) for scanning one prefix array with binary searches into another, reduced in practice by early termination; separable two-array
- Space: O(1) extra space for streaming running-prefix formulations; O(n) or O(n + m) when storing prefix/suffix arrays, split tables, or gap prefixes.

## Pitfalls
- Using binary search on cumulative sums that are not monotone because negative values are allowed.
- Removing sorting without an explicit guarantee that input is already ordered.
- Applying early termination when later states could become feasible again.
- Counting a boundary or endpoint twice when translating prefix indices into item counts.
- Using a locally balanced split without proving that it is globally optimal or that neighboring candidates are covered.
- Replacing a compact O(1)-space DP with O(n) tables without a real clarity, query, or correctness benefit.
- Off-by-one errors in prefix-before-element and suffix-from-index definitions.
- Assuming a valid suffix property when individual predicates are not monotone under the scan direction.

## When not to use
- Input values can be negative and the intended binary-search or early-break monotonicity does not hold.
- The operation is not associative or cannot be summarized by a constant-size prefix/suffix state.
- The objective depends on detailed internal arrangement rather than aggregate segment values.
- Sorting is required because the input order has semantic meaning or is not guaranteed to be ordered.
- A monotone two-pointer invariant cannot be proven.
- The problem requires online updates or arbitrary range queries better served by a Fenwick tree, segment tree, or other dynamic structure.

## Minimal example
Before:
```py
def count_subarrays(nums, target):
    count = 0
    for start in range(len(nums)):
        for end in range(start + 1, len(nums) + 1):
            if sum(nums[start:end]) == target:
                count += 1
    return count
```
After:
```py
from collections import defaultdict

def count_subarrays(nums, target):
    seen, prefix, count = defaultdict(int, {0: 1}), 0, 0
    for value in nums:
        prefix += value; count += seen[prefix - target]; seen[prefix] += 1
    return count
```
