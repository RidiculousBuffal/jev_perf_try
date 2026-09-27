---
skill_id: O029
type: operator
language: cpp
family: digit
name: Compress Decimal Search into Structural Arithmetic
description: Reusable optimization pattern distilled from weighted traces.
tags:
- optimization
- competitive-programming
- C++
- decimal-digits
- digit-processing
- arithmetic-aggregation
- state-compression
- remainder-automaton
- cycle-detection
- monotone-search
triggers:
- A loop scans every integer even though the predicate depends only on digit length, a fixed digit pattern, or a small decimal
  alphabet.
- A digit-sum or digit-membership helper is called repeatedly for consecutive values.
- The code constructs large decimal numbers with x = x * 10 + digit before taking a modulus.
- A recurrence or divisibility condition depends only on the current remainder.
- A mutable decimal string is repeatedly incremented, carry-normalized, and rescanned.
- An adaptive search repeatedly multiplies a decimal step by 10 or probes nearby candidates.
- The objective is a ratio such as value / digit_sum(value), and floating-point division is used for ordering.
- The valid candidates have a recognizable decimal form such as trailing 9s, palindromes, or digits from a fixed set.
---

## When to use
- A loop scans every integer even though the predicate depends only on digit length, a fixed digit pattern, or a small decimal alphabet.
- A digit-sum or digit-membership helper is called repeatedly for consecutive values.
- The code constructs large decimal numbers with x = x * 10 + digit before taking a modulus.
- A recurrence or divisibility condition depends only on the current remainder.
- A mutable decimal string is repeatedly incremented, carry-normalized, and rescanned.
- An adaptive search repeatedly multiplies a decimal step by 10 or probes nearby candidates.
- The objective is a ratio such as value / digit_sum(value), and floating-point division is used for ordering.
- The valid candidates have a recognizable decimal form such as trailing 9s, palindromes, or digits from a fixed set.

## Steps
1. Identify the semantic invariant and discard information that cannot affect the next transition or predicate result.
2. For digit-length predicates, partition [1, n] into complete base-10 blocks [10^(d-1), 10^d - 1] and count full and partial blocks directly.
3. For consecutive integer scans, maintain digit sums incrementally: increment by one and subtract 9 for each trailing 9 crossed.
4. For fixed decimal membership, build bool banned[10] or a bitmask and reject during a % 10 and / 10 scan with early exit; handle zero explicitly when required.
5. For repeated-digit divisibility, store only rem and update rem = (rem * base + digit) % modulus; mark visited remainders and terminate on repetition.
6. For exact base-k digit counts, repeatedly divide by k until zero instead of using log, ceil, or floating-point powers.
7. For structured decimal optimization, derive the finite candidate family first, such as prefix plus trailing 9s or arithmetic palindromes, then enumerate only those candidates.
8. Compare positive rational objectives by cross multiplication, for example cur * best_sum < best * cur_sum, after checking multiplication bounds or using a wider type.

## Complexity
- Time: (pattern dependent)
- Space: (pattern dependent)

## Pitfalls
- Do not assume a supposed fast reference is algorithmically better; stringstream conversion or interval scanning can be slower than integer arithmetic.
- Do not delay modulo reduction when the process depends only on remainders.
- Use a visited-remainder bound tied to the modulus; avoid fixed arrays whose size may not cover hidden constraints.
- Cross multiplication can overflow even when each operand fits in 64 bits; use __int128 or prove safe bounds.
- Do not use floating-point logs for exact digit counts, especially at powers of the base or when k <= 1.
- A digit loop that skips n == 0 may incorrectly treat zero as having no digits.
- Hard-coded hundreds/tens/ones logic silently fails when input width changes.
- Digit sums alone may lose structural information when the process depends on carry or reduction order.

## When not to use
- The predicate genuinely depends on the full value or on interactions that cannot be represented by a small invariant.
- The numeric bounds are small enough that direct enumeration is simpler, clearly fast, and less error-prone.
- The candidate structure is only guessed and no dominance or completeness argument is available.
- Feasibility is not monotone, so binary search would be invalid.
- The state space is not bounded by a manageable modulus or digit width.
- A string or big-integer representation is required because values exceed fixed-width arithmetic and no compact invariant exists.

## Minimal example
Before:
```cpp
long long countK(long long n, int k) {
    long long ans = 0;
    for (long long x = 1; x <= n; ++x) {
        int digits = 0; for (long long y = x; y; y /= 10) ++digits;
        ans += (digits == k);
    }
    return ans;
}
```
After:
```cpp
long long countK(long long n, int k) {
    long long lo = (k == 1 ? 1 : 1LL * pow10(k - 1));
    long long hi = 1LL * pow10(k) - 1;
    return n < lo ? 0 : min(n, hi) - lo + 1;
}
```
