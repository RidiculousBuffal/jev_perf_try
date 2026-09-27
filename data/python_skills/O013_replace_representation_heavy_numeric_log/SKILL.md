---
skill_id: O013
type: operator
language: python
family: digit
name: Replace Representation Heavy Numeric Logic with Direct Arithmetic
description: Optimize small and digit-oriented numeric tasks by modeling the mathematical property directly instead of reconstructing
  numbers through strings, dynamic evaluation, floating-point arithmetic, or unnecessary containers. Parse trusted numeric
  tokens explicitly, use divisibility invariants and suffix rules, preserve fixed-point decimals as scaled integers, simplify
  formulas algebraically, and batch or stream output
tags:
- numeric-optimization
- decimal-arithmetic
- divisibility
- digit-processing
- fixed-point
- input-parsing
- constant-factors
- integer-arithmetic
- io-batching
- formula-simplification
triggers:
- eval(input()) or dynamic expression evaluation is used for a fixed numeric format.
- Digits are concatenated, sliced, replaced, or repeatedly converted to reconstruct a number.
- A divisibility test can use a known invariant, such as digit sums or a limited decimal suffix.
- The result depends only on the last digit or last few digits.
- A fixed-width numeric input is processed as general-purpose text.
- Floating-point parsing is followed by floor, truncation, or integer conversion.
- Decimal inputs have known fixed precision.
- A hot loop repeatedly calls str(), performs substring searches, or scans digits inefficiently.
---

## When to use
- eval(input()) or dynamic expression evaluation is used for a fixed numeric format.
- Digits are concatenated, sliced, replaced, or repeatedly converted to reconstruct a number.
- A divisibility test can use a known invariant, such as digit sums or a limited decimal suffix.
- The result depends only on the last digit or last few digits.
- A fixed-width numeric input is processed as general-purpose text.
- Floating-point parsing is followed by floor, truncation, or integer conversion.
- Decimal inputs have known fixed precision.
- A hot loop repeatedly calls str(), performs substring searches, or scans digits inefficiently.

## Steps
1. Infer the mathematical data model and output contract before changing representation.
2. Replace eval with plain input reading and explicit int or token parsing; never execute input as code.
3. For fixed-width digits, parse tokens directly and reconstruct with place-value arithmetic only when full reconstruction is needed.
4. For divisibility by 4, inspect or compute only the final two decimal digits; for other moduli, apply the corresponding proven suffix or digit invariant.
5. For divisibility by 9 or similar digit rules, scan the raw decimal string and maintain the digit sum or running remainder instead of constructing a large integer.
6. If a classification depends only on the final decimal digit, read the input as text and classify its last character directly.
7. Algebraically simplify fixed expression patterns into direct integer formulas.
8. For decimal values with fixed precision, parse the decimal text into a scaled integer and compute with integer multiplication and division, such as A * scaled_value // scale.

## Complexity
- Time: Usually O(L) for reading or scanning an input of L digits and O(N * D) for enumerating N values with at most D digits. Fixed-width arithmetic and suffix classification are O(1). Rewrites commonly preserve big-O complexity while reducing
- Space: O(1) auxiliary space for direct arithmetic, suffix checks, streaming digit scans, and online filtering. Buffered output requires O(K) references or O(total_output) characters for K matches; large-integer construction may additionally

## Pitfalls
- Assuming a suffix rule applies without checking the base, modulus, sign, or required digit width.
- Changing decimal semantics by parsing fixed-point input as float.
- Using int(float(text) * scale), which can be off by one because of binary rounding.
- Confusing truncation toward zero with floor for negative products.
- Removing leading zeros when they are semantically significant.
- Using last-character logic when input may contain signs, decimal points, or trailing whitespace that has not been stripped.
- Replacing a full numeric calculation with a digit rule that does not preserve the original operation.
- Buffering all output when the number of matches can be enormous or memory is restricted.

## When not to use
- The task requires the full numeric value for operations not captured by a proven invariant.
- The input format permits arbitrary expressions or syntax and evaluating that syntax is explicitly the specification; even then, use a safe parser rather than eval.
- The decimal precision is variable, uncertain, or requires exact decimal semantics beyond simple scaling; use Decimal or an exact rational representation.
- The chosen suffix or digit rule does not apply to the actual modulus or numeral base.
- Output is interactive, latency-sensitive, or too large to buffer.
- The input is small enough that the proposed rewrite adds complexity without improving correctness or maintainability.

## Minimal example
Before:
```py
# O013 focus: replace
ans = 0
for i in range(1, n+1):
    ans += len(str(i))
```
After:
```py
# optimized for replace
ans = 0
for d in range(1, 19):
    L, R = 10**(d-1), min(n, 10**d - 1)
    if L <= R: ans += (R - L + 1) * d
```
