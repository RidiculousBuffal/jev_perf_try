---
skill_id: O038
type: operator
language: cpp
family: coprimality
name: Problem Aware Candidate Reduction with Standard Sorting
description: 'Replace bespoke radix sorting, packed integer keys, repeated full scans, and unnecessary data expansion with
  a representation that matches the actual operation: direct typed records, one-time sorting, bounded candidate generation,
  and a linear greedy or grouping scan. For moderate competitive-programming limits, prefer optimized STL sorting when it
  removes multiple memory passes and implementation fragility'
tags:
- sorting
- greedy
- candidate-reduction
- top-n-selection
- interval-scheduling
- offline-processing
- grouping
- rank-compression
- binary-search
- radix-sort
triggers:
- A custom radix/counting sorter is used for ordinary 32-bit or pair-valued data at roughly 1e5 to 3e5 elements.
- The logical solution needs only one ordering followed by a greedy scan, equal-key grouping, rank assignment, or top-N aggregation.
- Only the best N final values matter, while replacement operations may generate many identical candidates.
- Sortable state is naturally a pair or record, but the code packs it into a 64-bit key and later unpacks it.
- Queries operate on static sorted data and currently perform repeated full scans.
- Metadata such as original indices, counts, or prefix information must remain attached to keys during sorting.
- Large temporary arrays, multiple whole-array radix passes, manual signed-order correction, or fragile custom input code
  dominate optimization effort.
- The input scale is moderate enough that tuned std::sort and contiguous vectors are likely competitive with hand-written
  radix code.
---

## When to use
- A custom radix/counting sorter is used for ordinary 32-bit or pair-valued data at roughly 1e5 to 3e5 elements.
- The logical solution needs only one ordering followed by a greedy scan, equal-key grouping, rank assignment, or top-N aggregation.
- Only the best N final values matter, while replacement operations may generate many identical candidates.
- Sortable state is naturally a pair or record, but the code packs it into a 64-bit key and later unpacks it.
- Queries operate on static sorted data and currently perform repeated full scans.
- Metadata such as original indices, counts, or prefix information must remain attached to keys during sorting.
- Large temporary arrays, multiple whole-array radix passes, manual signed-order correction, or fragile custom input code dominate optimization effort.
- The input scale is moderate enough that tuned std::sort and contiguous vectors are likely competitive with hand-written radix code.

## Steps
1. Identify the true required operation: top-N selection, earliest-finish greedy scheduling, equal-key grouping, rank compression, or nearest-value lookup.
2. Represent objects directly with typed records such as pair<int,int>, pair<long long,long long>, or a small struct. Avoid packed keys unless profiling and constraints justify them.
3. Normalize keys before sorting: reduce by gcd, canonicalize signs, separate special zero or axis cases, and ensure signed ordering is explicit.
4. Sort offers or records by the field that drives the greedy choice, usually descending value or ascending right endpoint, using std::sort.
5. For top-N replacement problems, sort operations by replacement value, append no more than N useful generated values in total, merge with originals, and select or sort only the final relevant set.
6. For interval-like problems, store endpoints directly, sort lexicographically by right endpoint, and perform one greedy sweep while tracking the last accepted endpoint.
7. For rank-based problems, sort (value, original_index), write the sorted rank back to the original position, then compute the required parity or mismatch statistic.
8. For normalized-key counting, sort typed pairs, scan contiguous equal runs, and aggregate directly without rebuilding packed-key relationships.

## Complexity
- Time: (pattern dependent)
- Space: Usually O(N + M) for vectors of records and bounded candidates, with O(log N) auxiliary stack for std::sort. Paired metadata or query preprocessing may require additional O(N) space. Avoid large stack scratch buffers; use heap-backed

## Pitfalls
- Choosing radix sort solely because its theoretical complexity is linear while ignoring repeated full-array reads, writes, bucket resets, and cache pressure.
- Expanding every replacement count even though at most N generated values can affect the answer.
- Packing signed values or pair fields into an integer without proving that the resulting bit order matches the required lexicographic order.
- Forgetting sign canonicalization or special-case handling before grouping normalized directions.
- Sorting keys separately from indices, counts, or other payload and then attempting an expensive or error-prone reconstruction.
- Using an unstable sort when equal-key order carries required metadata semantics.
- Allocating large fixed-size temporary arrays on the stack, especially inside frequently called helpers.
- Relying on implementation-defined signed right shifts or unsigned byte order for signed integer sorting.

## When not to use
- Input sizes are so large or time limits so tight that comparison sorting is demonstrably the bottleneck and a carefully validated radix sort materially wins.
- Keys have a fixed unsigned representation, a proven bounded width, and no need for comparator-defined ordering or associated metadata.
- The algorithm requires repeated order-statistics queries where a heap, Fenwick tree, segment tree, or selection structure is more appropriate than full sorting.
- The problem needs online processing and future data cannot be buffered for offline sorting.
- Candidate values cannot be safely truncated to N because every generated item affects feasibility, multiplicity, or an intermediate constraint.
- The post-sort result depends on exact stable ordering among equal keys and the chosen representation does not preserve that requirement.

## Minimal example
Before:
```cpp
vector<uint64_t> keys;
for (auto [a,b,w] : offers) { int g=std::gcd(a,b); keys.push_back((uint64_t)(a/g)<<32 | (uint32_t)(b/g)<<16 | w); }
radix_sort(keys);
long long ans=0;
for (int take=0; take<N; ++take) { uint64_t best=0;
  for (auto x : keys) if ((int)(x&65535)> (int)(best&65535)) best=x;
  ans += best&65535; keys.erase(find(keys.begin(),keys.end(),best)); }
```
After:
```cpp
struct Offer { int a, b, value; };
vector<Offer> v;
for (auto [a,b,w] : offers) { int g=std::gcd(a,b); v.push_back({a/g,b/g,w}); }
sort(v.begin(),v.end(),[](const Offer&x,const Offer&y){ return x.value>y.value; });
long long ans=0; int used=0;
for (int i=0;i<(int)v.size() && used<N;) { int j=i+1; while(j<(int)v.size()&&v[j].a==v[i].a&&v[j].b==v[i].b) ++j; ans+=v[i].value; ++used; i=j; }
```
