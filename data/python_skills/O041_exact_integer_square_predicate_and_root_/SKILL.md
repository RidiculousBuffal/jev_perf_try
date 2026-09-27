---
skill_id: O041
type: operator
language: python
family: digit
name: Exact Integer Square Predicate and Root Boundary Simplification
description: Replace floating-point, string-based, or fixed-range enumeration logic for perfect-square decisions and largest-square-below-bound
  queries with exact integer arithmetic. Preserve decimal concatenation semantics by constructing the target once, use math.isqrt
  when available, and reduce extremal square queries to isqrt(n) * isqrt(n). For bounded domains without integer square root
  support, search only roots
tags:
- math
- perfect-square
- integer-square-root
- exact-arithmetic
- search-to-formula
- bounded-search
- string-concatenation
- single-query
- numerical-robustness
- constant-space
triggers:
- Code uses x ** 0.5, math.sqrt, is_integer(), modulo-one checks, or float-to-string inspection to test squarehood.
- A loop compares one fixed target against values generated as i*i.
- A list of squares is built solely for one membership test.
- A downward scan searches for the largest perfect square not exceeding n.
- The target is formed by concatenating numeric tokens as decimal strings rather than adding them.
- The result is a single boolean square-membership decision or one extremal square value.
- Search bounds are hardcoded even though the relevant root range can be derived from the target.
- A small bounded domain tempts manual enumeration of squares or special higher powers.
---

## When to use
- Code uses x ** 0.5, math.sqrt, is_integer(), modulo-one checks, or float-to-string inspection to test squarehood.
- A loop compares one fixed target against values generated as i*i.
- A list of squares is built solely for one membership test.
- A downward scan searches for the largest perfect square not exceeding n.
- The target is formed by concatenating numeric tokens as decimal strings rather than adding them.
- The result is a single boolean square-membership decision or one extremal square value.
- Search bounds are hardcoded even though the relevant root range can be derived from the target.
- A small bounded domain tempts manual enumeration of squares or special higher powers.

## Steps
1. Preserve input meaning: if tokens represent decimal concatenation, read them as strings and compute target = int(a + b) once.
2. For a square-membership query, compute r = math.isqrt(target) and test r * r == target.
3. For the greatest perfect square not exceeding n, compute r = math.isqrt(n) and return r * r directly.
4. If math.isqrt is unavailable, use an integer-only search bounded by r*r <= n, preferably binary search rather than scanning to an arbitrary constant.
5. Remove float formatting, repeated conversions, unsafe eval-based parsing, and unnecessary libraries.
6. Remove precomputed candidate lists when each candidate is used only once.
7. If a bounded fallback enumeration is required, generate squares with integer multiplication, stop at the mathematical bound, and exit early on a match.
8. For broader perfect-power maximization, derive exponent coverage mathematically; use squares for even exponents, enumerate only necessary odd exponents, and avoid brittle hardcoded exceptions unless constraints are explicitly fixed and documented.

## Complexity
- Time: (pattern dependent)
- Space: O(1) auxiliary space, excluding input storage. Avoiding candidate lists removes O(sqrt(n)) temporary memory.

## Pitfalls
- Assuming floating-point square roots are exact for arbitrary-size integers.
- Checking float textual representations, which depends on rounding and formatting details.
- Using a fixed root bound that can produce false negatives when input constraints change.
- Replacing decimal concatenation with numeric addition.
- Building and storing all squares for a one-time membership query.
- Calling a bounded linear scan an optimization when it has the same or worse asymptotic cost.
- Using floor(sqrt(n)) from floating point near exact-square boundaries.
- Hardcoding exceptional perfect powers without proving the constraint range covers all cases.

## When not to use
- The task requires enumerating, reporting, or reusing many candidate squares rather than testing one value.
- The input is a stream of many queries and precomputation is beneficial; use a reusable set or sieve when justified.
- The predicate is not reducible to exact integer squarehood or an extremal square boundary.
- A floating-point approximation is explicitly acceptable and performance dominates exact boundary correctness.
- Manual perfect-power case analysis is being considered without firm, small, documented constraints; use systematic exponent enumeration or a general algorithm instead.

## Minimal example
Before:
```py
a, b = input().split()
target = int(a + b)
squares = [i * i for i in range(1, target + 1)]
print(str(target) in {str(x) for x in squares})
```
After:
```py
from math import isqrt
a, b = input().split()
target = int(a + b)
r = isqrt(target)
print(r * r == target)
```
