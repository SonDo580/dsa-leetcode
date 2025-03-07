# You are planning to rob houses along a street.
# The ith house has nums[i] money.
# If you rob two houses beside each other,
# the alarm system will trigger and alert the police.
# What is the most money you can rob without alerting the police?

# Constraints:
# 1 <= nums.length <= 100
# 0 <= nums[i] <= 400

# ===== Analyze =====
# - When we're at house i, we have 2 choices:
# + rob house i: add money of house i to the maximum money up to house i - 2
#   (house i - 1 is skipped)
# + skip house i: take the maximum money upto house i - 1
#
# - Let's call dp[i] the maximum money we can robbed up to house i
#
# - State transition:
# dp[i] = max(dp[i - 1], nums[i] + dp[i - 2])
#
# - Base cases:
# + dp[0] = nums[0] -> rob the only house
# + dp[1] = max(nums[0], nums[1]) -> rob the house with more money

# ===== Implementation =====
# - Create a dp array of size n, where n is the number of house
# - Initialize dp[0] and dp[1]
# - Iterate from 2 to n-1 (inclusive), filling in dp[i]
# - Return dp[n-1], which contains the maximum money that can be robbed
#
# * Optimizing space:
# - Only track the last 2 values instead of using a full dp array


def rob_house(nums: list[int]) -> int:
    # If there's only 1 house, rob it
    if len(nums) == 1:
        return nums[0]

    # Initialize the base cases
    prev2 = nums[0]  # max money upto house i - 2
    prev1 = max(nums[0], nums[1])  # max money upto house i - 1

    for i in range(2, len(nums)):
        prev2, prev1 = prev1, max(prev1, nums[i] + prev2)

    return prev1


# Time complexity: O(n)
# Space complexity: O(1)


# ===== Bottom-up (use dp array) =====
def rob_house(nums: list[int]) -> int:
    n = len(nums)
    if n == 1:
        return nums[0]

    dp = [0] * n
    dp[0] = nums[0]
    dp[1] = max(nums[0], nums[1])

    for i in range(2, n):
        dp[i] = max(dp[i - 1], nums[i] + dp[i - 2])

    return dp[n - 1]


# ===== Top-down =====
def rob_house(nums: list[int]) -> int:
    def dp(i):
        if i == 0:
            return nums[0]
        if i == 1:
            return max(nums[0], nums[1])

        if i in memo:
            return memo[i]

        memo[i] = max(dp(i - 2) + nums[i], dp(i - 1))
        return memo[i]

    memo = {}
    return dp(len(nums) - 1)


# ===== Top-down  =====
# (with functools module to automatically memoize function)
from functools import cache


def rob_house(nums: list[int]) -> int:
    @cache
    def dp(i):
        if i == 0:
            return nums[0]
        if i == 1:
            return max(nums[0], nums[1])

        return max(dp(i - 2) + nums[i], dp(i - 1))

    return dp(len(nums) - 1)
