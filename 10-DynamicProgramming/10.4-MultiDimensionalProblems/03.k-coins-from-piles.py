# There are n piles of coins on a table.
# Each pile consists of a positive number of coins of assorted denominations.
# In one move, you can choose any coin on top of any pile,
# remove it, and add it to your wallet.
# Given a list 'piles', where piles[i] is a list of integers
# denoting the composition of the ith pile from top to bottom, and a positive integer k,
# return the maximum total value of coins you can have in your wallet
# if you choose exactly k coins optimally.


# ===== Identify DP problem =====
# - Involve optimization: maximize total value of coins.
# - Local decision affect future choices:
#   taking the coin on the top exposes other coins of the pile.
# - Note: Being greedy (always take the biggest coin) does not work
#   (taking a smaller coin may exposes a bigger coin below it)

# ===== Analysis =====
# - Let dp(i, remain) be the maximum value of coins we can take
#   starting from pile i with 'remain' moves remaining.
# - The answer is dp(0, k).
# - At the ith pile, we can skip or take some coins
#   + If we skip: value = dp(i + 1, remain)
#   + If we don't skip, we can take up to jth coins from the pile
#     (number of coins taken is j + 1):
#     . value = sum(piles[i][:j + 1]) + dp(i + 1, remain - j - 1)
#     (make sure not to take more than 'remain' or piles[i].length coins)
# -> Recurrence relation:
#    dp(i, remain) = max(skip, take)
#    . skip = dp(i + 1, remain)
#    . take = max(sum(piles[i][:j + 1]) + dp(i + 1, remain - j - 1)
#                 for j from 0 to min(remain, piles[i].length))
# - Base cases:
#   + no piles left (i == piles.length) -> return 0
#   + remain = 0 -> return 0

# ===== Top-down =====
from functools import cache


def max_value_of_coins(piles: list[list[int]], k: int) -> int:
    @cache
    def dp(i: int, remain: int) -> int:
        if i == len(piles) or remain == 0:
            return 0

        total_val = dp(i + 1, remain)  # skip current pile
        current_val = 0  # value accumulated from current pile
        for j in range(min(remain, len(piles[i]))):
            current_val += piles[i][j]
            total_val = max(total_val, current_val + dp(i + 1, remain - j - 1))

        return total_val

    return dp(0, k)


# ===== Bottom-up =====
def max_value_of_coins(piles: list[list[int]], k: int) -> int:
    n = len(piles)
    dp: list[list[int]] = [[0] * (k + 1) for _ in range(n + 1)]
    # Base cases are already fulfilled:
    # . remain = 0: dp[_][0] = 0
    # . i = n: dp[n][0] = 0

    # Iterate in "reverse" order
    for i in range(n - 1, -1, -1):
        for remain in range(1, k + 1):
            dp[i][remain] = dp[i + 1][remain]  # skip this pile
            current_val = 0  # value accumulated from current pile
            for j in range(min(remain, len(piles[i]))):
                current_val += piles[i][j]
                dp[i][remain] = max(
                    dp[i][remain], current_val + dp[i + 1][remain - j - 1]
                )

    return dp[0][k]


# ===== Complexity (both approaches) =====
# - Let n be the number of piles
#   -> Number of states: n * k
# - Let x be the average number of coins per pile
#
# 1. Time complexity:
# - (bottom-up) Initialize dp: O(n*k)
# - Fill up each entries in dp: O(n*k*x)
#   + At each state, we have a for loop that iterates x times.
# => Overall: O(n*k*x)
#
# 2. Space complexity: O(n*k)
# - (bottom-up) for 'dp' matrix
# - (top-down) for recursion stack


# ===== Bottom-up (space optimized) =====
# - The result of current row only depends on the result of last row
#   -> only need to track results for the last 2 rows
#   -> dp is a 1D array that stores the results of a row
def max_value_of_coins(piles: list[list[int]], k: int) -> int:
    n = len(piles)
    last_dp: list[int] = [0] * (k + 1)

    for i in range(n - 1, -1, -1):
        current_dp = [0] * (k + 1)

        for remain in range(1, k + 1):
            current_dp[remain] = last_dp[remain]  # skip this pile
            current_val = 0  # value accumulated from current pile
            for j in range(min(remain, len(piles[i]))):
                current_val += piles[i][j]
                current_dp[remain] = max(
                    current_dp[remain], current_val + last_dp[remain - j - 1]
                )

        last_dp = current_dp

    return last_dp[k]

# ===== Complexity =====
# 1. Time complexity: O(n*k*x) (same)
# 2. Space complexity: O(2*k) = O(k)