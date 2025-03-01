# You are given an integer array cost
# where cost[i] is the cost of ith step on a staircase.
# Once you pay the cost, you can either climb one or two steps.
#
# You can either start from the step with index 0, or the step with index 1.
#
# Return the minimum cost to reach the top of the floor.
# (outside the array, not the last index of cost)

# Example 1:
# Input: cost = [10,15,20]
# Output: 15
# Explanation: You will start at index 1.
# - Pay 15 and climb two steps to reach the top.
# The total cost is 15.

# Example 2:
# Input: cost = [1,100,1,1,1,100,1,1,100,1]
# Output: 6
# Explanation: You will start at index 0.
# - Pay 1 and climb two steps to reach index 2.
# - Pay 1 and climb two steps to reach index 4.
# - Pay 1 and climb two steps to reach index 6.
# - Pay 1 and climb one step to reach index 7.
# - Pay 1 and climb two steps to reach index 9.
# - Pay 1 and climb one step to reach the top.
# The total cost is 6.

# Constraints:
# 2 <= cost.length <= 1000
# 0 <= cost[i] <= 999


# ===== Framework =====
# 1. A function or data structure that compute/contain the answer
#    to the problem for any given state
# - dp(i): returns the minimum cost to climb the stairs upto ith step
#
# 2. A recurrence function to transition between states
# - dp(i) = min(dp(i-1) + cost[i-1], dp(i-2)+cost[i-2])
# (because we can climb 1 or 2 steps)
#
# 3. Base cases
# - dp(0) = dp(1) = 0
# (because we can start at step 0 or 1)
#
# (*) Complexity:
# - Time complexity: O(N*F) (number of possible states * work done at each state)
# - Space complexity: O(N) or O(1)
# + if going top-down, the hash map will store all N states at the end
# + if going bottom-up, the array use for tabulation will have size N
# + space complexity can be improved when using bottom-up approach


# ===== Bottom-up solution
# 1. Initialize the array dp that is sized according to state variables
# - N states -> N-dimensional array)
#
# 2. Set the base cases
#
# 3. Use nested for loops to iterate over state variables
# - Start from base cases and end at answer state)
# - Each iteration of the inner-most loop represent a given state,
#   and is equivalent to a function call with that state in top-down.
#
# 4. dp array is now populated with the answers for all possible states.
# -> return the answer to the original problem


# Top-down (memoization)
def min_cost_climbing_stairs(cost: list[int]) -> int:
    memo: dict[int, int] = {}

    def dp(i: int):
        if i <= 1:
            return 0

        if i in memo:
            return memo[i]

        memo[i] = min(dp(i - 1) + cost[i - 1], dp(i - 2) + cost[i - 2])
        return memo[i]

    return dp(len(cost))  # we need to climb beyond the last step


# Bottom-up (tabulation)
def min_cost_climbing_stairs(cost: list[int]) -> int:
    n = len(cost)

    dp = [0] * (n + 1)
    # - we need dp[n] (climb beyond the last step)
    # - base cases is implicitly defined as they are 0

    for i in range(2, n + 1):
        dp[i] = min(dp[i - 1] + cost[i - 1], dp[i - 2] + cost[i - 2])

    return dp[n]


# Bottom-up (optimizing space)
def min_cost_climbing_stairs(cost: list[int]) -> int:
    n = len(cost)

    # Base cases (min cost to step 0 and step 1)
    prev2 = 0 # min cost to step i - 2
    prev1 = 0 # min cost to step i - 1

    for i in range(2, n + 1):
        prev2, prev1 = prev1, min(prev1 + cost[i - 1], prev2 + cost[i - 2])

    return prev1
