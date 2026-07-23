"""
https://leetcode.com/problems/sqrtx/

Given a non-negative integer x,
return the square root of x rounded down to the nearest integer.
The returned integer should be non-negative as well.

You must not use any built-in exponent function or operator.
"""

"""
Idea:
- Try all integers in range [0..x].
  Return largest i where i*i <= x. 
- Improvement: use binary search
"""


# === Linear search ===
class Solution:
    def mySqrt(self, x: int) -> int:
        ans = -1
        for i in range(x + 1):
            if i * i > x:
                break
            ans = i
        return ans

"""
Complexity:
1. Time complexity: O(x)
2. Space complexity: O(1)
"""


# === Binary search ===
class Solution:
    def mySqrt(self, x: int) -> int:
        ans = -1
        left = 0
        right = x
        while left <= right:
            mid = (left + right) // 2
            if mid*mid <= x:
                ans = mid
                left = mid + 1 # try to find greater 'mid' that is still valid
            else:
                right = mid - 1 # reduce 'mid'
        return ans


"""
Complexity:
1. Time complexity: O(log(x))
2. Space complexity: O(1)
"""