---
skill_id: O024
type: operator
language: cpp
family: combinatorics
name: Replace Generic Containers with Dense Counting and Online Aggregation
description: When a solution uses std::map, std::set, repeated scans, or unnecessarily general DP for bounded integer keys,
  small alphabets, fixed-size inputs, or frequency-only workloads, specialize the representation and computation. Prefer flat
  arrays, vectors, compact fixed-size logic, unordered_map when keys are genuinely sparse, and sorted batching when order
  is needed. Accumulate pair contributions and other reusable
tags:
- frequency-counting
- direct-indexing
- dense-array
- unordered-map
- online-aggregation
- duplicate-grouping
- pair-counting
- prefix-sum
- sliding-window
- dp-compression
triggers:
- A std::map or std::set is used only for frequency counting or exact-key lookup.
- Integer keys lie in a known dense range such as [0, U].
- A tiny fixed input or alphabet is handled with a generic ordered container.
- Repeated map operator[] calls occur in a hot loop.
- A second pass exists only to count a value class, compute a maximum, or derive pair contributions.
- The answer can be updated from the previous frequency before incrementing it.
- Many duplicate records share a sortable key, but only grouped totals affect the result.
- A rolling-window frequency map counts equal transformed prefix states.
---

## When to use
- A std::map or std::set is used only for frequency counting or exact-key lookup.
- Integer keys lie in a known dense range such as [0, U].
- A tiny fixed input or alphabet is handled with a generic ordered container.
- Repeated map operator[] calls occur in a hot loop.
- A second pass exists only to count a value class, compute a maximum, or derive pair contributions.
- The answer can be updated from the previous frequency before incrementing it.
- Many duplicate records share a sortable key, but only grouped totals affect the result.
- A rolling-window frequency map counts equal transformed prefix states.

## Steps
1. Identify the actual operations required: exact lookup, ordered traversal, range query, distinct counting, frequency aggregation, or subset reachability.
2. If integer keys are dense and bounded, replace std::map with vector<int>, vector<long long>, std::array, or a static array indexed directly.
3. If keys are sparse and ordering is unnecessary, use unordered_map with reserve; use a custom hash when adversarial inputs are a concern.
4. For constant-size inputs, use direct comparisons, a tiny array, or sort/unique instead of allocating tree nodes.
5. Stream input into the smallest sufficient state. Keep only counts, totals, current prefix state, or touched keys needed later.
6. Accumulate repeated-pair answers online with ans += prior_frequency[key] before incrementing the frequency.
7. Maintain running maxima or sums during input to remove later scans.
8. Replace explicit base initialization with a lazy global-offset formula when final state is base plus local event count.

## Complexity
- Time: (pattern dependent)
- Space: Usually O(U), O(n), or O(number of distinct keys), with lower constants from contiguous storage. Fixed-size specializations use O(1) auxiliary space. Streaming can remove the need to retain the full input, while grouped offline methods

## Pitfalls
- Replacing a map with an array without proving that every key is in range.
- Using unordered_map when deterministic ordering is required and forgetting to sort the final keys.
- Using std::set for a handful of values when direct comparisons are faster and simpler.
- Calling operator[] multiple times for the same key instead of storing the iterator or reference.
- Counting pairs after a second pass when the contribution can be accumulated online.
- Using a Fenwick tree for point updates followed only by final point reads.
- Forgetting that C++ signed remainder may be negative; normalize residues before array indexing.
- Assuming grouping or batching improves asymptotic complexity when it merely changes constants.

## When not to use
- Keys are unbounded, highly sparse, or exceed practical direct-array limits.
- The input is genuinely tiny and the existing constant-time logic is already clearer and faster.
- Hashing has unacceptable worst-case guarantees and deterministic performance is mandatory.
- The DP state is sparse or transitions do not support dense indexing, batching, or bitset shifts.
- The proposed specialization relies on inferred fixed lengths, alphabets, or value bounds not guaranteed by the constraints.
- The extra preprocessing, sorting, or storage costs exceed the work saved by removing the original structure.

## Minimal example
Before:
```cpp
int n; cin >> n;
map<int, long long> freq;
long long pairs = 0;
for (int i = 0, x; i < n; ++i) { cin >> x; pairs += freq[x]++; }
cout << pairs << '\n';
```
After:
```cpp
int n; cin >> n;
vector<int> freq(100001);
long long pairs = 0;
for (int i = 0, x; i < n; ++i) { cin >> x; pairs += freq[x]++; }
cout << pairs << '\n';
```
