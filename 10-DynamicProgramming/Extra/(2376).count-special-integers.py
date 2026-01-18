"""
https://leetcode.com/problems/count-special-integers/

We call a positive integer special if all of its digits are distinct.

Given a positive integer n,
return the number of special integers that belong to the interval [1, n].
"""

# ===== Approach 1: Digit DP =====
"""
Analysis:
- Checking every number from 1 to n individually is O(n),
  which is too slow with the constraint n <= 2*10^9
  -> Let's pick digits incrementally.
- To ensure all digits are distinct, when picking the ith digit, 
  we need to know which digits have been used (order is not important).
  -> use a set or a bitmask.
- There are overlapping sub-problems. For example, with n = 500:
  . pick 1, then pick 2 -> next position using digits except {1, 2}
  . pick 2, then pick 1 -> next position using digits except {1, 2}
  -> use memoization.
- The next available digits can be restricted by current digit picked.
  For example, with n = 345:
  . if with picked 2 for digit0, digit1 can use digits from 0 to 9
  . if with picked 3 for digit0, digit1 can only use digits from 0 to 4
    (since the number must <= n).
- If we are placing leading zeros, that should not count as using the digit 0.
  For example: 0015, 0005, ...
"""

"""
- Let dp(i, tight, used_digits_mask, leading_zero) return the number
  ways to fill remaining positions [i..len(digits)-1] such that the entire
  resulting integer is a special integer.
  . i: the digit position we are filling
  . tight: if True, current digit is restricted by digits[i]
  . used_digits_mask: 10-bit integer where d-th bit is 1 if digit d has been used
  . leading_zero: are we currently placing leading zeros?
- Base case: 
  . i == len(digits) -> return 1 (construct 1 special integer successfully)
  . i == len(digits) and leading_zero -> return 0
    (haven't place any non-zero digits, 0 is not a special integer)
- Recurrence relation:
  . For each ith position, iterate through all digits d in [0, upper_bound]
    . upper_bound = 9 IF not tight ELSE digits[i]
    . skip if d has been used: (used_digits_mask >> d) & 1 == 1
  . Transition to next state:
    . new_tight: tight AND d == upper_bound
    . new_leading_zero: leading_zero AND d == 0
    . new_mask: 0 IF new_leading_zero ELSE used_digits_mask ^ (1 << d)
- Our result state:
  . i=0 (start from first digit)
  . tight=True (first digit cannot exceed first digit of n)
  . used_digits_mask (no digits have been used)
  . leading_zero=True (haven't place a non-zero digit)
"""
from functools import cache


def count_special_numbers(n: int) -> int:
    digits: list[int] = []
    while n > 0:
        digits.append(n % 10)
        n //= 10
    digits.reverse()

    @cache
    def dp(i: int, tight: bool, used_digits_mask: int, leading_zero: bool) -> int:
        if i == len(digits):
            return 1 if not leading_zero else 0

        max_digit = digits[i] if tight else 9
        count = 0
        for d in range(max_digit + 1):
            if (used_digits_mask >> d) & 1:
                continue

            next_tight = tight and d == max_digit
            next_leading_zero = leading_zero and d == 0
            next_mask = used_digits_mask ^ (1 << d) if not next_leading_zero else 0
            count += dp(i + 1, next_tight, next_mask, next_leading_zero)

        return count

    return dp(0, True, 0, True)


"""
Complexity:
- Number of digits in n: L = floor(log10(n)) + 1 -> O(log(n)
- Number of available digits: 10
- Number of used_digits_mask: 2^10 (each of the 10 digits can be included or excluded)

1. Time complexity: O(log(n) * 2^12 * 10)
- Number of states: O(L * 2 * 2^10 * 2)
- Work per state: iterate through 10 available digits

2. Space complexity: O(log(n) * 2^12)
- Memoization table: O(L * 2 * 2^10 * 2)
- Recursion stack: O(L)
"""

# ===== Approach 2: Permutation Counting =====
# TODO
