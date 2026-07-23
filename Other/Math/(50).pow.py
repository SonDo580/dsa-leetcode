"""
https://leetcode.com/problems/powx-n/

Implement pow(x, n), which calculates x raised to the power n
"""

# === Approach 1 (exceed time limit) ===
"""
- If n > 0: Init product = 1. Multiply product with x n times.
- If n == 0: x^0 = 0
- If n < 0: x^n = 1 / x^(-n)
"""


class Solution:
    # recursive
    def myPow(self, x: float, n: int) -> float:
        if n == 0:
            return 1
        if n < 0:
            return 1 / self.myPow(x, -n)
        return x * self.myPow(x, n - 1)

    # iterative
    def myPow(self, x: float, n: int) -> float:
        if n == 0:
            return 1
        if n < 0:
            return 1 / self.myPow(x, -n)

        product = 1
        while n > 0:
            product *= x
            n -= 1
        return product


"""
Complexity:

1. Time complexity: O(n)

2. Space complexity: 
- recursive approach: O(n) for recursion stack
- iterative approach: O(1)
"""


# === Approach 2: (reduce to base case / build up result) faster ===
"""
. n = 2*k     -> x^n = x^(n//2) * x^(n//2)
. n = 2*k + 1 -> x^n = x^(n//2) * x^(n//2) * x
"""


class Solution:
    # recursive
    def myPow(self, x: float, n: int) -> float:
        if n == 0:
            return 1
        if n < 0:
            return 1 / self.myPow(x, -n)

        half_pow = self.myPow(x, n // 2)
        if n % 2 == 0:
            return half_pow * half_pow
        return half_pow * half_pow * x

    # iterative
    def myPow(self, x: float, n: int) -> float:
        if n == 0:
            return 1
        if n < 0:
            return 1 / self.myPow(x, -n)

        i = 1
        k = n
        curr = x
        ans = 1

        while i < k:
            if i * 2 <= k:
                # x^(2*i) = x^i * x^i
                i = 2 * i
                curr = curr * curr
            else:
                # accumulate x^i to product
                ans *= curr

                # setup to accumulate remaining x^(n-i)
                k -= i
                i = 1
                curr = x

        ans *= curr
        return ans


"""
Complexity:

1. Time complexity: 
- recursive approach: O(log(n))
- iterative approach: O(log(n)^2)
  . best case: O(log(n))
    . when n = 2^m, i is doubled until it reaches n
      -> number of doublings needed: k = log2(n)
  . worst case: O(log(n)^2)
    . when n = 2^m - 1 (binary representation: all 1's)
    . example: 1, 3, 7, 15, 31, ...
    . see details below.

2. Space complexity: 
- recursive approach: O(log(n)) for recursion stack
- iterative approach: O(1)
"""

# === Approach 2 - iterative: worst case in detailed ===
"""
- Consider the 1st segment (keep doubling i while x^i <= x^n):
  + Initially: 
    . k = n = 2^m - 1
    . i = 1
  + Double i in each iteration as long as i*2 <= k
    . i: 1 -> 2 -> ... -> 2^(m - 1)
      -> takes m - 1 iterations
  + On the next iteration, i*2 = 2^m > k
    -> reset (1 iteration):
        . k_new = k - i = (2^m - 1) - 2^(m-1) = 2^(m-1) - 1
          (same form, shifted right by 1 bit)
        . i = 1
-> Total iterations for this segment: m

- Consider the entire execution:
  . segment 1: k = 2^m - 1; takes m iterations
  . segment 2: k = 2^(m-1) - 1; takes m - 1 iterations
  . ...
  . segment m-1: k = 2^2 - 1 = 3; takes 2 iterations
    next_k = 2^1 - 1 = 1 = i -> exit while loop
-> Sum up iterations spent in each segment
   . T(n) = m + (m - 1) + ... + 2 = O(m^2)

- Express T(n) in terms of n:
  . n = 2^m - 1 -> m = log2(n + 1)
  . T(n) = O(m^2) = O(log2(n + 1)^2) = O((log n)^2)
"""
