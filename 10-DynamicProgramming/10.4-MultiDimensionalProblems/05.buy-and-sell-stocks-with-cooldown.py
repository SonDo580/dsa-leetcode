# You are given an array prices where prices[i] is the price of a given stock on the ith day.
# Find the maximum profit you can achieve.
#
# You may complete as many transactions as you like
# (i.e., buy one and sell one share of the stock multiple times) with the following restrictions:
# - After you sell your stock, you cannot buy stock on the next day (i.e., cooldown one day).
#
# Note: You may not engage in multiple transactions simultaneously
# (i.e., you must sell the stock before you buy again).

# Example 1:
# Input: prices = [1,2,3,0,2]
# Output: 3
# Explanation: transactions = [buy, sell, cooldown, buy, sell]

# Example 2:
# Input: prices = [1]
# Output: 0

# Constraints:
# 1 <= prices.length <= 5000
# 0 <= prices[i] <= 1000


# ===== Identify DP problem =====
# - Involve optimization: maximize profit
# - Local decision (buy, hold, sell) affect future choices
# - Optimal sub-structure: profit at day i depends on choices up to day i - 1

# ===== Analysis =====
# - Identify required state variables:
#   + what the current day is: i
#   + whether we are holding stock: holding (0/1 or false/true)
#   + whether we are in the cool-down period: cooling_down (0/1 or false/true)
# -> Let dp(i, holding, cooling_down) returns the maximum profit we can achieve from day i,
#    holding indicated are are holding stock,
#    and cooling_down indicating we are in the cool-down period.
# - The answer will be dp(0, holding=false, cooling_down=false)
# - At each state:
#   + We can always skip:
#     - the profit is dp(i, holding, cooling_down=false)
#       . if currently cooling_down=true, it will becomes false the next day.
#   + If we are not holding stock and not in cool-down period, we can buy.
#     The profit is:
#     . -prices[i] + dp(i + 1, holding=true, cooling_down=false)
#   + If we are holding stock, we can sell. The profit is:
#     . prices[i] + dp(i + 1, holding=false, cooling_down=true)
#     (selling will take us 1 day to cool down)
# -> Recurrence relation:
#    dp(i, holding) = max(skip, buy, sell) where:
#    . skip = dp(i + 1, holding, cooling_down=false)
#    . buy = -prices[i] + dp(i + 1, holding=true, cooling_down)
#      (only considered if holding=false and cooling_down=false)
#    . sell = prices[i] + dp(i + 1, holding=false, cooling_down=true)
#      (only considered if holding=true)
# - Base cases:
#   + when i = prices.length, we can't make more transaction -> return 0


# ===== Top-down =====
from functools import cache


def max_profit_with_cool_down(prices: list[list[int]]) -> int:
    @cache
    def dp(i: int, holding: bool, cooling_down: bool):
        if i == len(prices):
            return 0

        max_profit = dp(i + 1, holding, cooling_down=False)  # skip
        if holding:
            max_profit = max(
                max_profit, prices[i] + dp(i + 1, holding=False, cooling_down=True)
            )  # can sell
        elif not cooling_down:
            max_profit = max(
                max_profit, -prices[i] + dp(i + 1, holding=True, cooling_down=False)
            )  # can buy

        return max_profit

    return dp(0, holding=False, cooling_down=False)


# ===== Bottom-up =====
def max_profit_with_cool_down(prices: list[int]) -> int:
    n = len(prices)

    # day -> holding -> cooling_down
    dp = [[[0] * 2 for _ in range(2)] for __ in range(n + 1)]
    # Base case already fulfilled: dp[n][_][_] = 0

    # Note that this doesn't work: 
    # . dp = [[[0] * 2] * 2] * (n + 1)
    # -> This creates shallow copies. All inner lists reference the same object
    # -> Updating 1 entry mutates the underlying list, affecting other entries.

    for i in range(n - 1, -1, -1):
        for holding in [0, 1]:
            for cooling_down in [0, 1]:
                max_profit = dp[i + 1][holding][0]  # skip
                if holding:
                    max_profit = max(
                        max_profit, prices[i] + dp[i + 1][0][1]
                    )  # can sell
                elif not cooling_down:
                    max_profit = max(
                        max_profit, -prices[i] + dp[i + 1][1][0]
                    )  # can buy

                dp[i][holding][cooling_down] = max_profit

    return dp[0][0][0]  # (day=0, holding=False, cooling_down=False)
