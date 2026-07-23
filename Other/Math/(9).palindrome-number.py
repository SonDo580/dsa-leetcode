"""
https://leetcode.com/problems/palindrome-number/

Given an integer x, return true if x is a palindrome, and false otherwise.

Follow up: Could you solve it without converting the integer to a string?
"""


# === Approach 1: convert to string + 2 pointers ===
class Solution:
    def isPalindrome(self, x: int) -> bool:
        if x < 0:
            return False

        s = str(x)
        l = 0
        r = len(s) - 1
        while l < r:
            if s[l] != s[r]:
                return False
            l += 1
            r -= 1
        return True


"""
Complexity:
- Let n = number of digits in x = O(log(x))

1. Time complexity: O(n)
2. Space complexity: O(n) for 's'
"""


# === Approach 2: repeatedly compare most and least significant digit ===
import math


class Solution:
    def isPalindrome(self, x: int) -> bool:
        if x < 0:
            return False
        if x < 10:  # optional optimization
            return True

        n = math.floor(math.log10(x)) + 1  # number of digits
        ten_pow = 10 ** (n - 1)

        while n > 1:
            ls_digit = x % 10  # least significant digit
            ms_digit = x // ten_pow  # most significant digit
            if ls_digit != ms_digit:
                return False

            x %= ten_pow  # truncate most significant digit
            x //= 10  # truncate least significant digit
            n -= 2
            ten_pow //= 100

        return True


"""
Complexity:
- Let n = number of digits in x = O(log(x))

1. Time complexity: still O(n), but don't need string conversion
2. Space complexity: O(1)
"""
