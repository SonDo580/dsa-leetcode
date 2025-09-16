# You are given an m x n integer array grid.
# There is a robot initially located at the top-left corner (i.e., grid[0][0]).
# The robot tries to move to the bottom-right corner (i.e., grid[m - 1][n - 1]).
# The robot can only move either down or right at any point in time.
#
# An obstacle and space are marked as 1 or 0 respectively in grid.
# A path that the robot takes cannot include any square that is an obstacle.
#
# Return the number of possible unique paths that the robot can take to reach the bottom-right corner.
#
# The testcases are generated so that the answer will be less than or equal to 2 * 109.

# Example 1:
# Input: obstacleGrid = [[0,0,0],[0,1,0],[0,0,0]]
# Output: 2
# Explanation: There is one obstacle in the middle of the 3x3 grid above.
# There are two ways to reach the bottom-right corner:
# 1. Right -> Right -> Down -> Down
# 2. Down -> Down -> Right -> Right

# Example 2:
# Input: obstacleGrid = [[0,1],[0,0]]
# Output: 1

# Constraints:
# m == obstacleGrid.length
# n == obstacleGrid[i].length
# 1 <= m, n <= 100
# obstacleGrid[i][j] is 0 or 1.


# ===== Identify DP problem =====
# Example: We've moved from (0, 0) to square A. The destination is square D
# ... ... ...
# ...  A - C
# ...  |   |
# ...  B - D
#
# - Local decision affects future decisions:
#   + If we move to C, we cannot go back to B, since we can only move down and right.
#
# - Recurrence relation:
#   + Number of ways to reach D depends on number of ways to reach B and C.
#
# - The paths can intersect -> possible improvement by memoization:
#   + (0, 0) -> ... -> A -> B -> D and (0, 0) -> ... -> A -> B -> D are 2 valid paths.
#   + In both paths we need to count the number of ways to reach A.

# ===== Strategy =====
# - Let dp(row, col) be the number of ways to reach (row, col) from (0, 0).
#   -> The answer is dp(m - 1, n - 1)
# - Base case:
#   + There's only 1 way to get to (0, 0) - by starting there (if it is empty).
#     -> dp(0, 0) = 1
#   + If a square is an obstacle, we cannot get there:
#     -> dp(row, col) = 0 if grid[row][col] == 1
# - Recurrence relation: (row, col) can be reached from (row - 1, col) or (row, col - 1).
#   -> dp(row, col) = dp(row - 1, col) + dp(row, col - 1)
#      Make sure to stay on the grid: 0 <= row < m, 0 <= col < n

from functools import cache


# ===== Top-down =====
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

# ===== Bottom-up (space-optimized) =====
# - The recurrence relation is static: number of ways to reach a cell always
#   depends only on number of ways to reach its left and top cells.
#   -> We only need to track the last 2 rows.
#   -> dp will be a 1D array to store results for each column of the current row.
def unique_paths_with_obstacles(obstacle_grid: list[list[int]]) -> int:
    if obstacle_grid[0][0] == 1:
        return 0
    
    m = len(obstacle_grid)
    n = len(obstacle_grid[0])
    
    last_dp: list[int] = [] # won't be used for the first row
    
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
