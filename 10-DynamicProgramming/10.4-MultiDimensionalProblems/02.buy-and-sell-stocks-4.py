# You are given an integer array 'prices' where prices[i]
# is the price of a given stock on the ith day, and an integer k.
# You can buy the stock and sell it,
# but you can only hold on to one unit of stock at any given time.
# Find the maximum profit you can achieve with at most k transactions.


# ===== Identify DP problem =====
# - Involve optimization: maximize profit
# - Local decision (buy, hold, sell) affect future choices
# - Optimal sub-structure: profit at day i depends on choices up to day i - 1

# ===== Analysis =====
# - Identify required state variables:
#   + what the current day is: i
#   + are we holding any stock: holding (0/1 or False/True)
#   + how many transactions we have remaining
# -> Let dp(i, holding, remain) returns the maximum profit we can achieve
#    from day i, with 'remain' transactions remaining, and 'holding' indicating
#    if we currently hold stock.
# - The answer will be dp(0, holding=false, remain=k)
# - At each state:
#   + If we are not holding stock, we can buy or skip.
#     If we buy, the profit is -prices[i] + dp(i + 1, true, remain)
#     (note that buying does not count as completing a transaction,
#      so 'remain' stays the same).
#   + If we are holding stock, we can sell or skip.
#     If we sell, the profit is prices[i] + dp(i + 1, false, remain - 1)
#     (we are no longer holding stock, and used up 1 transaction)
#   + In both cases, if we decide to skip, the profit is
#     dp(i + 1, holding, remain)
# -> Recurrence relation:
#    dp(i, holding, remain) = max(skip, buy, sell) where
#    . skip = dp(i + 1, holding, remain)
#    . buy = -prices[i] + dp(i + 1, true, remain) (only considered if holding=false)
#    . sell = prices[i] + dp(i + 1, false, remain - 1) (only considered if holding=true)
# - Base cases:
#   + when i = prices.length, we can't make more transaction -> return 0
#   + when k = 0, we ran out of transactions -> return 0

# ===== Top-down =====
from functools import cache


def max_profit(k: int, prices: list[int]) -> int:
    @cache
    def dp(i: int, holding: bool, remain: int) -> int:
        if i == len(prices) or remain == 0:
            return 0

        profit = dp(i + 1, holding, remain)  # profit if we skip
        if holding:
            profit = max(profit, prices[i] + dp(i + 1, False, remain - 1))  # can sell
        else:
            profit = max(profit, -prices[i] + dp(i + 1, True, remain))  # can buy

        return profit

    return dp(0, False, k)


# ===== Bottom-up =====
def max_profit(k: int, prices: list[int]) -> int:
    n = len(prices)

    # day -> holding (0: False, 1: True) -> remain
    dp: list[list[list[int]]] = [
        [[0] * (k + 1) for _ in range(2)] for __ in range(n + 1)
    ]

    # Base cases are already fulfilled
    # . dp[n][_][_] = 0
    # . dp[_][_][0] = 0

    for i in range(n - 1, -1, -1):
        for holding in range(2):
            for remain in range(1, k + 1):
                profit = dp[i + 1][holding][remain]  # profit if we skip
                if holding:
                    profit = max(
                        profit, prices[i] + dp[i + 1][0][remain - 1]
                    )  # can sell
                else:
                    profit = max(profit, -prices[i] + dp[i + 1][1][remain])  # can buy

                dp[i][holding][remain] = profit

    return dp[0][0][k]

# ===== Complexity (both approaches) =====
# - Number of states: O(n*2*k) = O(n*k)
# 1. Time complexity: O(n*k)
# 2. Space complexity: O(n*k) 