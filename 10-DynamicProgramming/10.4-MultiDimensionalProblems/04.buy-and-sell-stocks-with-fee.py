# You are given an array prices where prices[i] is the price of a given stock on the ith day, and an integer fee representing a transaction fee.
# Find the maximum profit you can achieve. You may complete as many transactions as you like, but you need to pay the transaction fee for each transaction.
#
# Note:
# You may not engage in multiple transactions simultaneously (i.e., you must sell the stock before you buy again).
# The transaction fee is only charged once for each stock purchase and sale.

# Example 1:
# Input: prices = [1,3,2,8,4,9], fee = 2
# Output: 8
# Explanation: The maximum profit can be achieved by:
# - Buying at prices[0] = 1
# - Selling at prices[3] = 8
# - Buying at prices[4] = 4
# - Selling at prices[5] = 9
# The total profit is ((8 - 1) - 2) + ((9 - 4) - 2) = 8.

# Example 2:
# Input: prices = [1,3,7,5,10,3], fee = 3
# Output: 6

# Constraints:
# 1 <= prices.length <= 5 * 10^4
# 1 <= prices[i] < 5 * 10^4
# 0 <= fee < 5 * 10^4


# ===== Identify DP problem =====
# - Involve optimization: maximize profit
# - Local decision (buy, hold, sell) affect future choices
# - Optimal sub-structure: profit at day i depends on choices up to day i - 1

# ===== Analysis =====
# - Identify required state variables:
#   + what the current day is: i
#   + are we holding any stock: holding (0/1 or false/true)
# -> Let dp(i, holding) returns the maximum profit we can achieve
#    from day i, and 'holding' indicating if we currently hold stock.
# - The answer will be dp(0, holding=false)
# - At each state:
#   + If we are not holding stock, we can buy or skip.
#     If we buy, the profit is -prices[i] + dp(i + 1, true)
#     (transaction fee will not be charged yet)
#   + If we are holding stock, we can sell or skip.
#     If we sell, the profit is prices[i] - fee + dp(i + 1, false)
#     (transaction fee will be charged when selling)
#   + In both cases, if we decide to skip, the profit is
#     dp(i + 1, holding)
# -> Recurrence relation:
#    dp(i, holding) = max(skip, buy, sell) where
#    . skip = dp(i + 1, holding)
#    . buy = -prices[i] + dp(i + 1, true) (only considered if holding=false)
#    . sell = prices[i] - fee + dp(i + 1, false) (only considered if holding=true)
# - Base cases:
#   + when i = prices.length, we can't make more transaction -> return 0

# ===== Top-down =====
from functools import cache


def max_profit_with_fee(prices: list[int], fee: int) -> int:
    @cache
    def dp(i: int, holding: bool) -> int:
        if i == len(prices):
            return 0

        max_profit = dp(i + 1, holding)  # skip
        if holding:
            max_profit = max(
                max_profit, prices[i] - fee + dp(i + 1, holding=False)
            )  # can sell
        else:
            max_profit = max(
                max_profit, -prices[i] + dp(i + 1, holding=True)
            )  # can buy

        return max_profit

    return dp(0, holding=False)


# ===== Bottom-up =====
def max_profit_with_fee(prices: list[int], fee: int) -> int:
    n = len(prices)

    # holding -> day
    dp: list[list[int]] = [[0] * (n + 1) for _ in [0, 1]]

    for i in range(n - 1, -1, -1):
        # holding=False (0) -> skip or buy
        dp[0][i] = max(dp[0][i + 1], -prices[i] + dp[1][i + 1])

        # holding=True (1) -> skip or sell
        dp[1][i] = max(dp[1][i + 1], prices[i] - fee + dp[0][i + 1])

    return dp[0][0]  # (holding=False, day=0)

# Notes:
# - Results for day i depend on results of day i + 1, on both values of holding (0, 1).
#   -> fill both holding entries of days i + 1 before moving to day i.