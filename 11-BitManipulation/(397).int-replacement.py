"""
https://leetcode.com/problems/integer-replacement/

Given a positive integer n, you can apply one of the following operations:
- If n is even, replace n with n / 2.
- If n is odd, replace n with either n + 1 or n - 1.

Return the minimum number of operations needed for n to become 1.
"""

"""
Identify DP problem:
- Optimization: find minimum number of operations
- Local decision affect future decision: 
  . If n is odd, either replace n with n-1 or n+1
- Multiple paths can reach the same state. Examples:
  . 5 -> 6 -> 3 -> 2 -> 1
    5 -> 4 -> 2 -> 1
  . 7 -> 8 -> 4 -> 2 -> 1
    7 -> 6 -> 3 -> 4 -> 2 -> 1
    7 -> 6 -> 3 -> 2 -> 1

Idea:
- Let dp(n) be minimum number of operation to transform n into 1.
- Recurrence:
  . If n is even, dp(n) = 1 + dp(n/2)
  . If n is odd, dp(n) = 1 + min(dp(n-1), dp(n+1))
- Base case: dp(1) = 0
- Guaranteed to reach 1 for x > 1:
  . If x = 2*k + 1  (k > 0)
    -> 1 step: x becomes (2*k + 2) or 2*k
    -> 2 steps: x becomes (k + 1) or k 
  . If x = 2*k  (k > 0)
    -> 1 step: x becomes k
  -> x is reduced after at most 2 steps and 1 <= x' < x
     Since the set of integers is finite, x' will eventually reaches 1.

Bit manipulation:
- Get LSB: x & 1 
  . LSB = 1 -> x is odd
  . LSB = 0 -> x is even
. x / 2 when x is even 
  = x // 2 
  = x >> 1
"""

from functools import cache


class Solution:
    def integerReplacement(self, n: int) -> int:
        @cache
        def dp(x: int) -> int:
            """Return minimum number of operations to transform x into 1."""
            if x == 1:
                return 0

            if x & 1:  # x is odd
                return 1 + min(dp(x - 1), dp(x + 1))

            # x is even
            return 1 + dp(x >> 1)

        return dp(n)


"""
Complexity:

1. Time complexity: O(log(n))
- x is halved after at most 2 steps.
  -> Number of DP states to go from n to 1: O(2*log2(n)) = O(log(n))
     
2. Space complexity: 
- recursion stack: O(log(n))
- cache size: O(log(n))
"""


# === Optimization ===
"""
========== Analysis:
- When x is odd, try to choose optimally between x-1 and x+1.
  . x = 2*k + 1   (k > 0)
  . x + 1 path: 2 steps to reach k + 1   
    (2*k + 1 + 1) / 2
  . x - 1 path: 2 steps to reach k
    (2*k + 1 - 1) / 2

- Case 1: k = 1 (initial x = 3) -> k + 1 = 2:
  . x + 1 path: need 1 more step to reach 1   (2 / 2 = 1)
  . x - 1 path: reached 1

- Case 2: k = 2*k' + 1     (k' > 0):
  + Continue x + 1 path: x' = k + 1
    . 1 step to reach k' + 1: x' / 2 = (2*k' + 1 + 1) / 2
    . 1 more step ((k' + 1) - 1) if want to reach k'
      (2 steps to reach k')
  + Continue x - 1 path: x' = k
    . 2 steps to reach k' + 1: (x' + 1) / 2 = ((2*k' + 1) + 1) / 2
    . 2 steps to reach k': (x' - 1) / 2 = ((2*k' + 1) - 1) / 2
  -> Reduce to k' + 1: x + 1 path uses less steps. 
     Reduce to k': same number of steps in both paths.

- Case 3: k = 2*k'     (k' > 0)
  + Continue x + 1 path: x' = k + 1
    . 2 steps to reach k' + 1: (x' + 1) / 2 = ((2*k' + 1) + 1) / 2
    . 2 steps to reach k': (x' - 1) / 2 = ((2*k + 1) - 1) / 2
  + Continue x - 1 path: x' = k
    . 1 step to reach k': x' / 2 = 2*k' / 2
    . 1 more step (k' + 1) if want to reach k' + 1
      (2 steps to reach k' + 1)
    -> Reduce to k': x - 1 path uses less steps. 
       Reduce to k' + 1: same number of steps in both paths.

========== Conclusion from case 1, 2, 3:
- x is odd and x > 1
  <-> x = 2*k + 1 (k > 0) 
  . If x = 3 (k = 1), pick x - 1 path.
  . If k = 2*k' + 1 (k' > 0), pick x + 1 path.
  . If k = 2*k' (k' > 0), pick x - 1 path.
- Bit patterns:
  . x is odd -> b[0] = 1
  . x = 2*(2*k + 1) + 1 = (((k << 1) + 1) << 1) + 1
    -> b[1] = 1
  . x = 2*(2*k) + 1 = ((k' << 1) << 1) + 1
    -> b[1] = 0
- Get kth bit: x & (1 << k)  (k = 1 -> mask = (1 << 1) = 2)
"""


class Solution:
    def integerReplacement(self, n: int) -> int:
        steps = 0
        while n > 1:
            if (n & 1) == 0:  # n is even
                n >>= 1  # n = n / 2
            elif n == 3:
                n -= 1
            elif n & 2 != 0:  # (n & 2) > 0 -> n = 2*(2*k + 1) + 1
                n += 1
            else:  # (n & 2) == 0 -> n = 2*(2*k) + 1
                n -= 1
            steps += 1
        return steps


"""
Complexity:

1. Time complexity: O(log(n))
- n is halved after at most 2 steps
  -> Number of steps: O(2*log2(n)) = O(log(n))

2. Space complexity: O(1)
"""
