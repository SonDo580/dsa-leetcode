# You are climbing a staircase. It takes n steps to reach the top.
# Each time you can either climb 1 or 2 steps.
# In how many distinct ways can you climb to the top?

# Example 1:
# Input: n = 2
# Output: 2
# Explanation: There are two ways to climb to the top.
# 1. 1 step + 1 step
# 2. 2 steps

# Example 2:
# Input: n = 3
# Output: 3
# Explanation: There are three ways to climb to the top.
# 1. 1 step + 1 step + 1 step
# 2. 1 step + 2 steps
# 3. 2 steps + 1 step

# Constraints:
# 1 <= n <= 45


# ===== Identify DP problem =====
# - Asking for number of ways to do something (climb stairs)
# - Local decision affects future outcomes (taking 1 or 2 steps changes the remaining number of steps)

# ===== Analyze =====
# - 1 state variable: index i
#   dp(i): return number of ways to climb to step i
#
# - dp(i) = dp(i - 1) + dp(i - 2)
# + last move take 1 step -> number of ways to reach n is the same as n - 1
# + last move take 2 steps -> number of ways to reach n is the same as n - 2
# + note that we're counting number of ways (not number of steps)
#
# - bases cases:
# + dp(0) = 1 (already at the top)
# + dp(1) = 1 (can only take 1 step)


# ===== Top-down =====
def ways_to_climb_stairs(n: int) -> int:
    def dp(i: int) -> int:
        if i <= 1:
            return 1

        if i in memo:
            return memo[i]

        memo[i] = dp(i - 1) + dp(i - 2)
        return memo[i]

    memo = {}
    return dp(n)


# ===== Complexity =====
# 1. Time complexity: O(n)
# - Each state is computed at most once, since results are memoized.
# - Each computation takes O(1)
#
# 2. Space complexity: O(n) - for 'memo' dictionary and recursion stack


# ===== Bottom-up =====
def ways_to_climb_stairs(n: int) -> int:
    if n == 1:
        return 1

    prev2 = prev1 = 1

    for i in range(2, n + 1):
        prev2, prev1 = prev1, prev1 + prev2

    return prev1


# ===== Complexity =====
# 1. Time complexity: O(n)
# 2. Space complexity: O(1)
