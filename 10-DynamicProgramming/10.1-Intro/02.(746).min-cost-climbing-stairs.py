"""
You are given an integer array 'cost'
where cost[i] is the cost of ith step on a staircase.
Once you pay the cost, you can either climb one or two steps.

You can either start from the step with index 0, or the step with index 1.

Return the minimum cost to reach the top of the floor.
(outside the array, not the last index of cost)
"""

"""
- Let dp(i) returns the minimum cost to climb upto ith step.
- We can climb to i either from i - 1 or i - 2
  -> Recurrence relation:
  . dp(i) = min(dp(i-1) + cost[i-1], dp(i-2)+cost[i-2])

3. Base cases
- We can start at step 0 or 1
  -> dp(0) = dp(1) = 0
"""


# ===== Top-down DP =====
from functools import cache


def min_cost_climbing_stairs(cost: list[int]) -> int:
    @cache
    def dp(i: int) -> int:
        """Return the minimum cost to climb to ith step."""
        if i <= 1:
            return 0
        return min(dp(i - 1) + cost[i - 1], dp(i - 2) + cost[i - 2])

    return dp(len(cost))  # we need to climb beyond the last step


"""
Complexity:
1. Time complexity: O(n)

2. Space complexity: O(n) for memoization and recursion stack
"""


# ===== Bottom-up DP =====
def min_cost_climbing_stairs(cost: list[int]) -> int:
    n = len(cost)

    dp = [0] * (n + 1)
    # - we need dp[n] (climb beyond the last step)
    # - base cases is implicitly defined as they are 0

    for i in range(2, n + 1):
        dp[i] = min(dp[i - 1] + cost[i - 1], dp[i - 2] + cost[i - 2])

    return dp[n]


"""
Complexity:
1. Time complexity: O(n)

2. Space complexity: O(n) for 'dp'
"""


# ===== Bottom-up DP (optimize space) =====
def min_cost_climbing_stairs(cost: list[int]) -> int:
    n = len(cost)

    prev2 = 0
    prev1 = 0

    for i in range(2, n + 1):
        prev2, prev1 = prev1, min(prev1 + cost[i - 1], prev2 + cost[i - 2])

    return prev1


"""
Complexity:
1. Time complexity: O(n)

2. Space complexity: O(1)
"""
