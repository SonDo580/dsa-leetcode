"""
https://leetcode.com/problems/unique-paths/

There is a robot on an m x n grid.
The robot is initially located at the top-left corner and wants to move to the bottom-right corner.
The robot can only move either down or right. Given m and n,
return the number of possible unique paths that the robot can take to reach the bottom-right corner.
"""

"""
Identify DP problem:
Example: We've moved from (0, 0) to square A. The destination is square D
    ... ... ...
    ...  A - C
    ...  |   |
    ...  B - D
- Local decision affects future decisions:
  . If we move to C, we cannot go back to B, since we can only move down and right.
- Recurrence relation:
  . Number of ways to reach D depends on number of ways to reach B and C.
- The paths can intersect -> possible improvement by memoization:
  . (0, 0) -> ... -> A -> B -> D and (0, 0) -> ... -> A -> C -> D are 2 valid paths.
  . In both paths we need to count the number of ways to reach A.

Implementation:
- Let dp(row, col) be the number of unique paths to reach (row, col) from (0, 0)
- We want to reach the bottom right, so the answer is dp(m - 1, n - 1)
- To reach each square, we can go from the top or the left square.
  -> dp(row, col) = dp(row - 1, col) + dp(row, col - 1)
- Base case:
  . there's only 1 way to get to (0, 0) - starting there
  -> dp(0, 0) = 1
"""

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


"""
Complexity:

1. Time complexity: O(m * n)

2. Space complexity: O(m * n + m + n) = O(m * n)
- memoization table: O(m * n)
- recursion stack: O(m + n)
"""


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


"""
Complexity:

1. Time complexity: O(m * n)

2. Space complexity: O(m * n) for 'dp'
"""


# ===== Bottom-up (space-optimized) =====
"""
- The recurrence relation is static
  (result of a cell only depends on its left and top cells)
  -> We only need to track the last 2 rows
  -> dp is a 1D array to store results for a row
"""


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


"""
Complexity:

1. Time complexity: O(m * n)

2. Space complexity: O(n) for 'last_dp' and 'current_dp'
"""

# ===== Bottom-up (optimize space further) =====
"""
- Once dp[row - 1][col] is "used" by dp[row][col],
  we don't need dp[row - 1][col] anymore.
-> Just use 1 array 'dp' and modify it in-place.
"""


def unique_paths(m: int, n: int) -> int:
    dp: list[int] = [0] * n
    dp[0] = 1

    for _ in range(m):
        for col in range(n):
            if col > 0:
                dp[col] += dp[col - 1]

    return dp[n - 1]


"""
Complexity:

1. Time complexity: O(m * n)

2. Space complexity: O(n) for 'dp'
"""
