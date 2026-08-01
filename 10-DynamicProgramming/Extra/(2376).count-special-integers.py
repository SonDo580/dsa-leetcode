"""
https://leetcode.com/problems/count-special-integers/

We call a positive integer special if all of its digits are distinct.

Given a positive integer n,
return the number of special integers that belong to the interval [1, n].
"""

# ===== Approach 1: DP - choose digit for each position =====
"""
Analysis:
- Checking every number from 1 to n individually is O(n),
  which is too slow with the constraint n <= 2*10^9
  -> Let's pick digits incrementally.
- To ensure all digits are distinct, when picking the ith digit, 
  we need to know which digits have been used.
  -> Use a set / boolean array / bitmask.
- There are overlapping sub-problems. For example:
  . pick 1, pick 2 -> next position using digits except {1, 2}
  . pick 2, pick 1 -> next position using digits except {1, 2}
  -> Use memoization.
- The next available digits can be restricted by current digit picked.
  For example, with n = 345:
  . if with picked 2 for digit0, digit1 can use digits from 0 to 9
  . if with picked 3 for digit0, digit1 can only use digits from 0 to 4
    (since result number must <= n).
- If we are placing leading 0's, that should not count as using the digit 0
  (Don't add 0 to used_digits_mask while placing leading 0's)

Idea:
- Let 'digits' represents digits of n.
- Let dp(i, tight, used_digits_mask, leading_zero) 
  return the number ways to fill remaining positions [i..len(digits)-1] 
  such that the entire resulting integer is a special integer.
  . i: the digit position we are filling
  . tight: if True, current digit is restricted by digits[i]
  . used_digits_mask: 10-bit integer where d-th bit is 1 if digit d has been used
  . leading_zero: are we currently placing leading zeros?
- Base case:
  . i == len(digits) -> return 1 (construct 1 special integer successfully)
  . i == len(digits) and leading_zero -> return 0
    (haven't place any non-zero digits, 0 is not a special integer)
- Recurrence relation:
  . For ith position, try all digits d in [0..upper_bound]
    . upper_bound = not_tight ? 9 : digits[i]
    . skip if d has been used: (used_digits_mask >> d) & 1 == 1
  . Transition to next state:
    . next_tight: tight AND d == upper_bound
    . next_leading_zero: leading_zero AND d == 0
    . next_mask: next_leading_zero ? 0 : (used_digits_mask ^ (1 << d))
  . Number of ways = sum of all cases.
- Result state:
  . i=0 (start filling first digit)
  . tight=True (first digit cannot exceed first digit of n)
  . used_digits_mask=0 (no digits have been used)
  . leading_zero=True (haven't place a non-zero digit)
"""

from functools import cache


class Solution:
    def countSpecialNumbers(self, n: int) -> int:
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

        return dp(i=0, tight=True, used_digits_mask=0, leading_zero=True)


"""
Complexity:
- Number of digits in n: L = floor(log10(n)) + 1 = O(log(n))
- Number of available digits: d = 10
- Range of used_digits_mask: [0..2^d-1]  (2^d values)
  . each digit can be included or excluded

1. Time complexity: O(log(n) * 2^d * d)
- Find digits: O(L) = O(log(n))
- Number of DP states: O(L * 2 * 2^d * 2) = O(log(n) * 2^d)
  Work per DP state: O(d) to iterate through available digits

2. Space complexity:  O(log(n) * 2^d)
- digits: O(L) = O(log(n))
- cache: O(log(n) * 2^d)
- recursion stack: O(L) = O(log(n))
"""


# ===== Approach 2: Count arrangements =====
"""
- Let L be number of digits in n, d be number of available digits (10).
  -> Integer with L > 10 cannot have all unique digits.

=== For 1 <= l < L ===
- Count number of integers with l unique digits (position 0 <-> most significant digit):
  . 9 digits as candidates for position 0 (except 0)
  . 9 digits as candidates for position 1 (for each choice at position 0)
  . 8 digits as candidates for position 2 (for each choice at position 1)
  . ...
  . (10 - l + 1) digits as candidates for position l-1 (for each choice at previous position)
  -> count = 9 * 9 * 8 * ... * (10 - l + 1)
           = (10 - 1) * 9 * 8 * ... * (10 - l + 1)
           = 10! / (10 - l)! - (10! / (10 - l)!) / 10
          (= P(10, l) - P(10, l) / 10)
- Calculate 'count': 
  + Approach 1: Find P(n, l) = n! / (n - l)!
    -> Find n!. Cache result of n' < n.
    -> Use DP.
  + Approach 2: Build incrementally
    . l = 1 -> count = 9
    . l = 2 -> count = 9 * 9 = prev_count * 9
    . l = 3 -> count = 9 * 9 * 8 = prev_count * 8
    . ...
    -> Recurrence: count = prev_count * available; available -= 1
       Base case: count = 9; available = 9

=== For l = L ===
TODO
"""


class Solution:
    def countSpecialNumbers(self, n: int) -> int:
        pass
