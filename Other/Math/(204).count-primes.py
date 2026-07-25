"""
https://leetcode.com/problems/count-primes/

Given an integer n,
return the number of prime numbers that are strictly less than n.
"""

# === Approach 1: Check if all numbers in [2..n-1] are primes ===
# (exceed time limit)
"""
Check prime:
. n is prime if n only divides 1 and itself
  -> n is not prime if n divides any number in [2..n-1]

Improvement 1:
- If n is composite, n = x*y
- If x >= 2, y must <= n/2 (and vice versa).
  Otherwise the product will exceed n.
  -> Only check range of 1 component: x in [2..n//2]

Improvement 2 (reduce range of 1 component):
- If x > sqrt(n), y must < sqrt(n) (and vice versa).
  -> Only check x in [2..floor(sqrt(n))]
"""

import math


def _is_prime(n: int) -> bool:
    for i in range(2, math.floor(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


class Solution:
    def countPrimes(self, n: int) -> int:
        cnt = 0
        for i in range(2, n):
            if _is_prime(i):
                cnt += 1
        return cnt


"""
Complexity:

1. Time complexity: O(n*sqrt(n))
. is_prime(i): O(sqrt(i))
  -> T = sum(O(sqrt(i)) for i in [2..n-1])
       = O(sqrt(2) + sqrt(3) + ... + sqrt(n-1))

2. Space complexity: O(1)
"""


# === Approach 2: Sieve of Eratosthenes ===
"""
Idea:
- Identify a prime and mark multiples of it as composite.

Implementation:
- Initialize a boolean array [0..n-1], set all entries to True,
  except for 0 and 1.
- For each number p in [2..floor(sqrt(n))],
  if p is marked as prime (not multiples of any smaller number in [2..p-1]):
  . Mark all multiples (< n) of p as not prime.
  . Start from p*p since smaller multiples have been marked 
    when processing smaller primes.
- After the loop, count number of remaining True entries.

=== Why start marking from p*p ===
- Any composite number k must have at least 1 prime factor <= sqrt(k)
- If k < p*p
  -> sqrt(k) < p
  -> k must have at least 1 prime factor < p
  -> k is marked as composite when processing a prime before p
"""


class Solution:
    def countPrimes(self, n: int) -> int:
        if n <= 2:
            return 0

        is_prime: list[bool] = [True] * n  # [0..n-1]
        is_prime[0] = is_prime[1] = False

        # try each number in [2..floor(sqrt(n))]
        p = 2
        while p * p < n:
            if is_prime[p]:
                # mark all multiples of p as not prime
                # . multiples [p*2, ..., p*(p-1)] have been marked
                #   when processing smaller primes.
                for i in range(p * p, n, p):
                    is_prime[i] = False
            p += 1

        # count prime numbers in [2..n-1]
        cnt = 0
        for i in range(2, n):
            cnt += 1 if is_prime[i] else 0
        return cnt

"""
Complexity:

1. Time complexity: O(n*log(log(n)) + n) = O(n*log(log(n)))
- Marking multiples for each p: O(n/p) iterations
  -> Across range [2..floor(sqrt(n))]
     . T = n * sum(1/p where p <= sqrt(n)) 
         = O(n*log(log(p)))   (Mertens' second theorem)
         = O(n*log(log(n^0.5)))
         = O(n*log(log(n)))
- Find True entries in 'is_prime': O(n)

2. Space complexity: O(n) for 'is_prime' array
"""