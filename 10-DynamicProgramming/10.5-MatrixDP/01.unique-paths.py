# There is a robot on an m x n grid.
# The robot is initially located at the top-left corner and wants to move to the bottom-right corner.
# The robot can only move either down or right. Given m and n,
# return the number of possible unique paths that the robot can take to reach the bottom-right corner.

# ===== Identify DP problem =====
# - Similar to 10.5/03 (unique paths with obstacle)

# ===== Implementation =====
# - Let dp(row, col) be the number of unique paths to reach (row, col) from (0, 0)
# - We want to reach the bottom right, so the answer is dp(m - 1, n - 1)
# - Recurrence relation:
#   dp(row, col) = dp(row - 1, col) + dp(row, col - 1)
# - Base case:
#   there's only 1 way to get to (0, 0) - by starting there
#   -> dp(0, 0) = 1

# ===== Top-down =====
from functools import cache


def unique_paths(m: int, n: int) -> int:
    @cache
    def dp(row: int, col: int) -> int:
        if row + col == 0:
            return 1

        num_paths: int = 0
        if row > 0:
            num_paths += dp(row - 1, col)
        if col > 0:
            num_paths += dp(row, col - 1)

        return num_paths

    return dp(m - 1, n - 1)


# ===== Bottom-up =====
def unique_paths(m: int, n: int) -> int:
    dp: list[list[int]] = [[0] * n for _ in range(m)]
    dp[0][0] = 1

    for row in range(m):
        for col in range(n):
            if row > 0:
                dp[row][col] += dp[row - 1][col]
            if col > 0:
                dp[row][col] += dp[row][col - 1]

    return dp[m - 1][n - 1]


# ===== Bottom-up (space-optimized) =====
# - The recurrence relation is static
#   (result of a cell only depends on its left and top cells)
#   -> We only need to track the last 2 rows
#   -> dp is a 1D array to store results for a row
def unique_paths(m: int, n: int) -> int:
    last_dp: list[int] = []  # won't be used for the first row

    for row in range(m):
        current_dp: list[int] = [0] * n

        for col in range(n):
            if row + col == 0:
                current_dp[col] = 1
                continue

            if row > 0:
                current_dp[col] += last_dp[col]
            if col > 0:
                current_dp[col] += current_dp[col - 1]

        last_dp = current_dp

    return last_dp[n - 1]
