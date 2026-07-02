"""
https://leetcode.com/problems/unique-paths-ii/

You are given an m x n integer array 'grid'.
There is a robot initially located at the top-left corner (i.e., grid[0][0]).
The robot tries to move to the bottom-right corner (i.e., grid[m - 1][n - 1]).
The robot can only move either down or right at any point in time.

An obstacle and space are marked as 1 or 0 respectively in 'grid'.
A path that the robot takes cannot include any square that is an obstacle.

Return the number of possible unique paths that the robot can take to reach the bottom-right corner.

The testcases are generated so that the answer will be less than or equal to 2 * 10^9.
"""

"""
Identify DP problem:
- Local decision affects future decision: 
  . at each cell, either move right or down, but not both
- Recurrence relation: 
  . path sum to a cell depends on path sum to its left and top cells.
- The paths can intersect -> possible improvement by caching.

Implementation:
- Let dp(row, col) be the number of ways to reach (row, col) from (0, 0).
  -> The answer is dp(m - 1, n - 1)
- Base case:
  + There's only 1 way to get to (0, 0) - by starting there (if it is empty).
    -> dp(0, 0) = 1
  + If a square is an obstacle, we cannot get there:
    -> dp(row, col) = 0 if grid[row][col] == 1
- Recurrence relation: (row, col) can be reached from (row - 1, col) or (row, col - 1).
  -> dp(row, col) = dp(row - 1, col) + dp(row, col - 1)
     Make sure to stay on the grid: 0 <= row < m, 0 <= col < n
"""


# ===== Top-down =====
from functools import cache


def unique_paths_with_obstacles(obstacle_grid: list[list[int]]) -> int:
    @cache
    def dp(row: int, col: int) -> int:
        """Returns number of ways to reach (row, col) from (0, 0)"""
        if obstacle_grid[row][col] == 1:
            return 0

        if row + col == 0:
            return 1

        num_paths: int = 0
        if row > 0:
            num_paths += dp(row - 1, col)
        if col > 0:
            num_paths += dp(row, col - 1)

        return num_paths

    m = len(obstacle_grid)
    n = len(obstacle_grid[0])
    return dp(m - 1, n - 1)


"""
Complexity:

1. Time complexity: O(m * n)

2. Space complexity: O(m * n)
- memoization table: O(m * n)
- recursion stack: O(m + n)
"""


# ===== Bottom-up =====
def unique_paths_with_obstacles(obstacle_grid: list[list[int]]) -> int:
    if obstacle_grid[0][0] == 1:
        return 0

    m = len(obstacle_grid)
    n = len(obstacle_grid[0])

    dp: list[list[int]] = [[0] * n for _ in range(m)]
    dp[0][0] = 1

    for row in range(m):
        for col in range(n):
            if obstacle_grid[row][col] == 1:
                dp[row][col] = 0
                continue

            if row > 0:
                dp[row][col] += dp[row - 1][col]
            if col > 0:
                dp[row][col] += dp[row][col - 1]

    return dp[m - 1][n - 1]


"""
Complexity:
1. Time complexity: O(m * n)
2. Space complexity: O(m * n) for 'dp' matrix
"""


# ===== Bottom-up (space-optimized) =====
"""
- The recurrence relation is static: number of ways to reach a cell
  depends only on number of ways to reach its left and top cells.
  -> We only need to track the last 2 rows.
  -> dp will be a 1D array to store results for each column of the current row.
"""


def unique_paths_with_obstacles(obstacle_grid: list[list[int]]) -> int:
    if obstacle_grid[0][0] == 1:
        return 0

    m = len(obstacle_grid)
    n = len(obstacle_grid[0])

    last_dp: list[int] = []  # won't be used for the first row

    for row in range(m):
        current_dp = [0] * n

        for col in range(n):
            if obstacle_grid[row][col] == 1:
                current_dp[col] = 0
                continue

            if row + col == 0:
                current_dp[col] = 1
                continue

            if row > 0:
                current_dp[col] += last_dp[col]
            if col > 0:
                current_dp[col] += current_dp[col - 1]

        last_dp = current_dp

    return last_dp[n - 1]


"""
Complexity:
1. Time complexity: O(m * n)
2. Space complexity: O(n) for 'last_dp' and 'current_dp'
"""


# === Bottom-up (optimize space further)
"""
- Only use 1 'dp' array
"""


def unique_paths_with_obstacles(obstacle_grid: list[list[int]]) -> int:
    if obstacle_grid[0][0] == 1:
        return 0

    m = len(obstacle_grid)
    n = len(obstacle_grid[0])
    dp: list[int] = [0] * n

    for row in range(m):
        # each dp[col] retains value from last iteration
        # (initial dp[row][col] = dp[row-1][col])
        for col in range(n):
            if obstacle_grid[row][col] == 1:
                dp[col] = 0
                continue

            if row + col == 0:
                dp[col] = 1
                continue

            ans = 0
            if row > 0:
                ans += dp[col]
            if col > 0:
                ans += dp[col - 1]
            dp[col] = ans

    return dp[n - 1]


"""
Complexity:
1. Time complexity: O(m * n)
2. Space complexity: O(n) for 'dp'
"""
