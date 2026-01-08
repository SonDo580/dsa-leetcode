"""
https://leetcode.com/problems/fibonacci-number/

The Fibonacci numbers, commonly denoted F(n) form a sequence,
called the Fibonacci sequence,
such that each number is the sum of the two preceding ones,
starting from 0 and 1. That is,
. F(0) = 0, F(1) = 1
. F(n) = F(n - 1) + F(n - 2), for n > 1.
Given n, calculate F(n).
"""


# ===== "Naive" recursion =====
def fib(n: int) -> int:
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)


"""
Complexity:

1. Time complexity: O(2^n) 
- every 'fib' call creates 2 more 'fib' calls.
- max recursion depth is n.
(note that the last level is not full since
 subtree fib(n-1) is higher than subtree fib(n-2))

2. Space complexity: O(n) for the recursion stack.
"""


# ===== Recursion + Memoization (Top-down DP) =====
def fibonacci(n: int) -> int:
    memo: dict[int, int] = {}

    def dp(x: int) -> int:
        if x <= 1:
            return x

        if x in memo:
            return memo[x]

        memo[x] = dp(x - 1) + dp(x - 2)
        return memo[x]

    return dp(n)


"""
Complexity:
1. Time complexity: O(n)
. each state only be computed once.

2. Space complexity: O(n) 
- memoization table: O(n).
- recursion stack: O(n).
"""


# ===== Tabulation (Bottom-up DP) =====
def fibonacci(n: int) -> int:
    if n <= 1:
        return n

    dp = [0] * (n + 1)
    dp[1] = 1

    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]

    return dp[n]


"""
Complexity:
1. Time complexity: O(n)

2. Space complexity: O(n) for 'dp'.
"""


# ===== Bottom-up DP (optimize space) =====
"""
- dp[i] only depends on dp[i - 1] and dp[i - 2]
  -> use 2 variables to track instead of a whole array.  
"""


def fibonacci(n: int) -> int:
    if n <= 1:
        return n

    prev2 = 0
    prev1 = 1

    for i in range(2, n + 1):
        prev1, prev2 = prev1 + prev2, prev1

    return prev1

"""
Complexity:
1. Time complexity: O(n)

2. Space complexity: O(1)
"""