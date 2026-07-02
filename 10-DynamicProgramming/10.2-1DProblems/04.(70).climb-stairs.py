"""
https://leetcode.com/problems/climbing-stairs/

You are climbing a staircase. It takes n steps to reach the top.
Each time you can either climb 1 or 2 steps.
In how many distinct ways can you climb to the top?
"""

"""
Identify DP problem:
- Asking for number of ways to do something (climb stairs)
- Local decision affects future outcomes (taking 1 or 2 steps changes the remaining number of steps)

Analyze:
- 1 state variable: index i
  . dp(i): number of ways to climb to step i
  . dp(n): result
- Recurrence relation: dp(i) = dp(i - 1) + dp(i - 2)
  . last move take 1 step -> number of ways to reach n is the same as n - 1
  . last move take 2 steps -> number of ways to reach n is the same as n - 2
- Bases cases:
  . dp(0) = 1 (already there)
  . dp(1) = 1 (can only take 1 step)
"""


# ===== Top-down =====
def ways_to_climb_stairs(n: int) -> int:
    def dp(i: int) -> int:
        if i <= 1:
            return 1

        if i in memo:
            return memo[i]

        memo[i] = dp(i - 1) + dp(i - 2)
        return memo[i]

    memo: dict[int, int] = {}
    return dp(n)


"""
Complexity:

1. Time complexity: O(n)
- Each state is computed at most once, since results are memoized.
- Each computation takes O(1)

2. Space complexity: O(n) for memoization and recursion stack
"""


# ===== Bottom-up (space-optimized) =====
def ways_to_climb_stairs(n: int) -> int:
    if n == 1:
        return 1

    prev2 = prev1 = 1  # dp[0] and dp[1]

    for i in range(2, n + 1):
        # dp[i] = dp[i - 1] + dp[i - 2]
        prev2, prev1 = prev1, prev1 + prev2

    return prev1  # dp[n]


"""
Complexity:
1. Time complexity: O(n)
2. Space complexity: O(1)
"""
