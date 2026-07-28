"""
https://leetcode.com/problems/power-of-two/

Given an integer n, return true if it is a power of two.
Otherwise, return false.

An integer n is a power of two
if there exists an integer x such that n == 2^x.
"""

"""
Idea:
. x <= 0 -> x is not power of 2
. x = 2^i <-> ith bit is 1, all other bits are 0
. x & (x - 1) clear the lowest set bit
  -> If x & (x - 1) = 0, x only has 1 set bit
  -> x is a power of 2
"""


class Solution:
    def isPowerOfTwo(self, n: int) -> bool:
        return n > 0 and n & (n - 1) == 0


"""
1. Time complexity: O(1)
2. Space complexity: O(1)
"""
