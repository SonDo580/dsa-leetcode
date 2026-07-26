"""
https://leetcode.com/problems/factorial-trailing-zeroes/

Given an integer n, return the number of trailing zeroes in n!.
. n! = n * (n - 1) * (n - 2) * ... * 3 * 2 * 1.

Follow up: Could you write a solution that works in logarithmic time complexity?
"""

# === Approach 1: Compute n! and count trailing 0's in n! ===
# (exceed time limit)


def _factorial(n: int) -> int:
    ans = 1
    while n > 1:
        ans *= n
        n -= 1
    return ans


def _count_trailing_zeros(n: int) -> int:
    assert n > 0  # factorial cannot be 0
    cnt = 0
    while n > 0 and n % 10 == 0:
        cnt += 1
        n //= 10
    return cnt


class Solution:
    def trailingZeroes(self, n: int) -> int:
        return _count_trailing_zeros(_factorial(n))


"""
Complexity:
- When integer becomes large (> 64-bit limit), 
  Python switches to BigInt arithmetic
  -> multiplication is no longer O(1), O(d)
     where d is number of digits.
- Number of digits in n!: d = O(log10(n!))
  . n! = n*(n-1)*...*2*1 < n^n
    -> d = O(log(n^n) = O(n*log(n))

1. Time complexity: O(n^2 * log(n) + n*log(n)) = O(n^2 * log(n))
- Compute factorial n!: sum(O(i*log(i)) for i in [1..n]) 
  (assume that BigInt arithmetic is used from the beginning)
  . sum(O(i*log(i)) for i in [1..n]) 
    < O(log(n) * sum(i for i in [1..n]))
    = O(n^2 * log(n))
- Count trailing zeros in n!: O(n*log(n))

2. Space complexity: O(1)
"""


# === Improvement ===
"""
Analysis:
- Any integer can be uniquely factored into prime numbers:
  . N = 2^a * 3^b * 5^c * ...
- To form a trailing 0, we need a factor of 10,
  which is composed from a pair (2, 5)
  -> Number of trailing 0's = min(a, c)
     . a = total count of prime factor 2 in n!
     . c = total count of prime factor 5 in n!
- For n! = 1 * 2 * ... * (n-1) * n
  . Multiples of 2 occur every 2 steps: 2, 4, ...
  . Multiples of 5 occur every 5 steps: 5, 10, ...
  -> min(a, c) = c
  -> Number of trailing 0's = Number of factor 5 in n!
- Powers of 5 can contain more than 1 factor 5
  . 5 = 5^1 -> 1 factor of 5
  . 25 = 5^2 -> 2 factors of 5 
  . 125 = 5^3 -> 3 factors of 5
  . ...
  Number of powers of 5 in range [1..n]:
  . 5^k <= n -> k <= log5(n) -> k in [1..floor(log5(n))]
  . Let K = max_k = floor(log5(n))

Counting:
- Each multiple of 5^K contributes K factors of 5
  Number of multiples of 5^K: n // 5^K
  -> Number of factor 5 from multiples of 5^K: K*(n // 5^K)

- Number of multiples of 5^(K-1) not including multiples of 5^K:
  . n // 5^(K-1) - n // 5^K
  Number of factor 5 from multiples of 5^(K-1) not including multiples of 5^K: 
  . (K-1)*(n // 5^(K-1) - n // 5^K)
    = (K-1)*(n // 5^(K-1)) - K*(n // 5^K) + n // 5^K

- ...

- Number of multiples of 5^1 not including multiples of higher powers:
  . n // 5^2 - n // 5^3     (n // 5^3 includes multiples of 5^3 and higher powers)
  Number of factor 5 from multiples of 5^2 not including multiples of higher powers: 
  . 2*(n // 5^2) - 3*(n // 5^3) + n // 5^3

- Number of multiples of 5^1 not including multiples of higher powers:
  . n // 5^1 - n // 5^2     (n // 5^2 includes multiples of 5^2 and higher powers)
  Number of factor 5 from multiples of 5^1 not including multiples of higher powers:
  . n // 5^1 - 2*(n // 5^2) + n // 5^2

=> Count factor 5: sum(n // 5^k for k in [1..K])    (other terms cancel out)
"""

import math


class Solution:
    def trailingZeroes(self, n: int) -> int:
        if n == 0:
            return 0  # 0! = 1 -> no trailing 0's

        factor_5_cnt = 0
        max_k = math.floor(math.log(n, 5))
        for k in range(1, max_k + 1):
            factor_5_cnt += n // 5**k
        return factor_5_cnt


"""
Complexity:
1. Time complexity: O(log5(n)) = O(log(n))
2. Space complexity: O(1)
"""
