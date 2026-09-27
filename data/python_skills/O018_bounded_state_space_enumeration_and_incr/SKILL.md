---
skill_id: O018
type: operator
language: python
family: graph
name: Bounded State Space Enumeration and Incremental State Tracking
description: Optimize small-constraint exhaustive searches and deterministic simulations by representing only valid states,
  bounding the search by input-derived limits, and maintaining incremental state instead of repeatedly rebuilding or rescanning
  history. Generate monotone or fixed-branching candidates directly with DFS/backtracking or specialized loops, score or count
  each candidate immediately, prune impossible prefixes
tags:
- bounded-bruteforce
- dfs
- backtracking
- combinations-with-repetition
- state-space-pruning
- streaming-enumeration
- incremental-counting
- cycle-detection
- visited-set
- bitmask-state
triggers:
- The input size or maximum digit length is explicitly small.
- Valid candidates satisfy monotonicity, fixed-length, digit-alphabet, or other structural constraints.
- A generic product, queue, frontier, or recursive generator explores invalid or redundant states.
- Partial sequences are copied with slicing or concatenation at every branch.
- Branch-local mutable lists are aliased or mutated without explicit undo.
- The implementation materializes all candidates, scores, or successful outputs although only a count, maximum, or decision
  is needed.
- Candidates are repeatedly converted between tuples, strings, and integers.
- A numeric upper bound can cap candidate depth or prune a prefix immediately.
---

## When to use
- The input size or maximum digit length is explicitly small.
- Valid candidates satisfy monotonicity, fixed-length, digit-alphabet, or other structural constraints.
- A generic product, queue, frontier, or recursive generator explores invalid or redundant states.
- Partial sequences are copied with slicing or concatenation at every branch.
- Branch-local mutable lists are aliased or mutated without explicit undo.
- The implementation materializes all candidates, scores, or successful outputs although only a count, maximum, or decision is needed.
- Candidates are repeatedly converted between tuples, strings, and integers.
- A numeric upper bound can cap candidate depth or prune a prefix immediately.

## Steps
1. Infer the true candidate state space and replace unrestricted generation with only valid structural states.
2. For nondecreasing sequences, generate combinations with repetition using a lower bound equal to the previous choice.
3. For fixed small depth, use direct nested loops or low-overhead DFS; otherwise use one mutable path with append/pop backtracking.
4. Pass an index or depth instead of repeatedly slicing the remaining input.
5. Maintain branch isolation explicitly: mutate one shared path and undo, or create independent state only when necessary.
6. Derive a hard global bound such as maximum digit length and stop expanding prefixes that exceed a numeric limit.
7. Carry numeric prefixes incrementally with arithmetic, or carry a compact state representation such as a bitmask, rather than reconstructing strings or tuples.
8. Fuse validation into construction when partial information can prove invalidity; otherwise defer checks to completed candidates when that reduces repeated work.

## Complexity
- Time: Let S be the number of structurally valid candidates, C the per-candidate scoring cost, D the maximum bounded depth, and T the number of simulated states. Streaming exhaustive search is typically O(S * C), with S often equal to a binomial
- Space: Streaming DFS/backtracking uses O(D) auxiliary space, plus O(Q) for constraints or queries. A materialized candidate list requires O(S * D) or O(S) space and should generally be avoided. Hash-based duplicate detection requires O(T) space

## Pitfalls
- Confusing lower constant factors with an asymptotic improvement; exhaustive enumeration still costs the number of valid states times per-state work.
- Using a queue or materialized Cartesian product when streaming DFS or an iterator would suffice.
- Generating all candidates and filtering them afterward when a prefix constraint permits pruning.
- Using a fixed-depth padded representation without carefully handling leading zeros and numeric equivalence.
- Performing full-string scans, set construction, or integer parsing at every recursive node.
- Appending dummy markers or collecting every score when a scalar counter or best value is sufficient.
- Mutating a shared branch list without append/pop undo, causing sibling branches to contaminate one another.
- Checking sortedness or other invariants only at leaves when they can be enforced during construction.

## When not to use
- The candidate depth or branching factor is large enough that exhaustive enumeration is infeasible.
- The input constraints require an algorithm better than the full valid-state count.
- The objective has exploitable structure for dynamic programming, greedy optimization, meet-in-the-middle, or algebraic counting.
- The search requires random access to all generated candidates or their traversal order.
- The sequence history is needed for more than membership, such as frequencies, ordering, reconstruction, or shortest-path guarantees.
- A pruning rule cannot be proven safe and may discard feasible or optimal branches.

## Minimal example
Before:
```py
from itertools import product
N = 98765
valid = []
for k in range(1, len(str(N)) + 1):
    for ds in product(range(1, 10), repeat=k):
        if list(ds) == sorted(ds) and int(''.join(map(str, ds))) <= N: valid.append(ds)
print(len(valid))
```
After:
```py
N = 98765; count = 0
def dfs(start, value):
    global count
    if value > N: return
    if value: count += 1
    for d in range(start, 10): dfs(d, value * 10 + d)
dfs(1, 0); print(count)
```
