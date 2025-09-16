# Given a m x n grid filled with non-negative numbers,
# find a path from top left to bottom right,
# which minimizes the sum of all numbers along its path.
# Return this sum.
# You can only move down or right.


# ===== Identify DP problem =====
# - Similar to 10.5/03 (unique paths with obstacle)

# ===== Implementation =====
# - Let dp(row, col) be the minimum path sum from (0, 0) to (row, col)
# - We want to reach the bottom right, so the answer is dp(m - 1, n - 1)
# - Recurrence relation:
#   dp(row, col) = grid[row][col] + min(dp(row - 1, col), dp(row, col - 1))
#   (make sure to stay in bounds)
# - Base case: dp(0, 0) = grid[0][0]

# ===== Top-down =====
from functools import cache


def min_path_sum(grid: list[list[int]]) -> int:
    @cache
    def dp(row: int, col: int) -> int:
        if row + col == 0:
            return grid[row][col]

        answer: int = float("inf")
        if row > 0:
            answer = min(answer, dp(row - 1, col))
        if col > 0:
            answer = min(answer, dp(row, col - 1))

        return answer

    m = len(grid)
    n = len(grid[0])
    return dp(m - 1, n - 1)


# ===== Bottom-up =====
def min_path_sum(grid: list[list[int]]) -> int:
    m = len(grid)
    n = len(grid[0])

    dp: list[list[int]] = [[0] * n for _ in range(m)]
    dp[0][0] = grid[0][0]

    for row in range(m):
        for col in range(n):
            if row + col == 0:
                continue

            answer: int = float("inf")
            if row > 0:
                answer = min(answer, dp[row - 1][col])
            if col > 0:
                answer = min(answer, dp[row][col - 1])
            dp[row][col] = grid[row][col] + answer

    return dp[m - 1][n - 1]


# ===== Bottom-up (space-optimized) =====
# - The recurrence relation is static
#   (result of a cell only depends on its left and top cells)
#   -> We only need to track the last 2 rows
#   -> dp is a 1D array to store results for a row
def min_path_sum(grid: list[list[int]]) -> int:
    m = len(grid)
    n = len(grid[0])

    last_dp: list[int] = []  # won't be used for the first row

    for row in range(m):
        current_dp: list[int] = [0] * n

        for col in range(n):
            if row + col == 0:
                current_dp[col] = grid[row][col]
                continue

            answer: int = float("inf")
            if row > 0:
                answer = min(answer, last_dp[col])
            if col > 0:
                answer = min(answer, current_dp[col - 1])
            current_dp[col] = grid[row][col] + answer

        last_dp = current_dp

    return last_dp[n - 1]
