---
skill_id: O038
type: operator
language: python
family: graph
name: Frontier Driven Greedy Priority Queues
description: Replace repeated global simulation, rescanning, sorting, or layered-container maintenance with a data structure
  that exposes only the next actionable state. Use a max-heap when repeatedly selecting the best currently eligible value,
  chronological buckets when eligibility is keyed by a bounded dense index, and frontier or queue propagation when local state
  changes enable new dependencies. Preserve the greedy
tags:
- greedy
- priority-queue
- max-heap
- scheduling
- event-driven-processing
- frontier-processing
- dependency-graph
- topological-order
- bucket-array
- incremental-state
triggers:
- Each step selects the best currently eligible item.
- Items become eligible over time or after local dependency changes.
- A loop repeatedly scans all candidates to find a maximum or discover newly enabled actions.
- The implementation uses sorting, layered lists, pop(0), dictionary keys over a dense integer range, or a heap wrapper.
- A min-heap is used with negated values to emulate a max-heap.
- Only one or a few local states change after each action.
- A valid action requires mutually agreeing front elements or predecessor completion.
- A global day or round loop mostly detects idle periods.
---

## When to use
- Each step selects the best currently eligible item.
- Items become eligible over time or after local dependency changes.
- A loop repeatedly scans all candidates to find a maximum or discover newly enabled actions.
- The implementation uses sorting, layered lists, pop(0), dictionary keys over a dense integer range, or a heap wrapper.
- A min-heap is used with negated values to emulate a max-heap.
- Only one or a few local states change after each action.
- A valid action requires mutually agreeing front elements or predecessor completion.
- A global day or round loop mostly detects idle periods.

## Steps
1. Identify the invariant: select the maximum eligible reward, or process every currently enabled frontier event.
2. For repeated extract-modify-reinsert operations, use one heap containing the current values; store negatives in Python's min-heap or implement a direct max-heap when extreme throughput is required.
3. For time-indexed eligibility with a bounded dense horizon, bucket items in a list of lists using normalized zero-based indices, then sweep time once in order.
4. At each time step, insert newly eligible items before extracting at most one best item.
5. For dependency-driven processes, store each participant's current front with an index or stack and activate a pair/event only when both required fronts agree.
6. After processing an event, advance only the affected pointers and re-check only their newly exposed fronts.
7. Use a queue or topological propagation for dependency activation; count processed events and detect deadlock or cycles explicitly.
8. Replace repeated aggregate calls such as sum(state) with maintained counters or recurrences.

## Complexity
- Time: (pattern dependent)
- Space: Typically O(V + E) for heap and item storage, O(T + E) for dense time buckets, or O(N^2) when explicitly representing all pair dependencies. Specialized online heaps can use O(V) space; buffered output adds O(number of emitted results).

## Pitfalls
- Using a heap wrapper whose method names do not match the calls, causing failure before performance is relevant.
- Negating values inconsistently when emulating a max-heap.
- Using pop(0), repeated maximum scans, or resorting after every update.
- Replacing a dense bounded index with a dictionary and paying unnecessary hashing and object overhead.
- Preallocating a fixed bucket or heap capacity without a proven safe upper bound.
- Processing all days or rounds even when no state changes, instead of propagating from affected frontiers.
- Failing to re-check both endpoints after a dependency event advances their fronts.
- Using lists for membership tests in hot paths instead of sets, counters, or direct state flags.

## When not to use
- Eligibility is not monotone and cannot be represented by a stable heap key, bucket order, or local frontier.
- The objective is not greedy or selecting the current maximum can invalidate future optimality.
- The coordinate universe is sparse or unbounded, making dense bucket preallocation wasteful or unsafe.
- The workload is small enough that simpler sorting or direct simulation is clearer and fast enough.
- You need arbitrary deletions, decrease-key, stable ordering, or rich priority semantics unsupported by the specialized representation.
- A manual heap would only remove negligible overhead while substantially increasing implementation and correctness risk.

## Minimal example
Before:
```py
jobs = [(0, 3, 40), (1, 2, 25), (2, 1, 35), (4, 2, 30)]
time = total = 0
while jobs:
    eligible = [job for job in jobs if job[0] <= time]
    if not eligible: time = min(job[0] for job in jobs); continue
    job = max(eligible, key=lambda job: job[2]); jobs.remove(job)
    time += job[1]; total += job[2]
```
After:
```py
import heapq
pending = sorted([(r, d, v) for r, d, v in [(0, 3, 40), (1, 2, 25), (2, 1, 35), (4, 2, 30)]])
time = total = 0; frontier = []
while pending or frontier:
    while pending and pending[0][0] <= time: _, d, v = pending.pop(0); heapq.heappush(frontier, (-v, d))
    if not frontier: time = pending[0][0]; continue
    value, duration = heapq.heappop(frontier); time += duration; total -= value
```
