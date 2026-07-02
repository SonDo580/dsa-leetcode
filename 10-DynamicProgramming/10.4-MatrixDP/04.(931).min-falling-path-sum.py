"""
https://leetcode.com/problems/minimum-falling-path-sum/

Given an n x n array of integers 'matrix',
return the minimum sum of any falling path through 'matrix'.

A falling path starts at any element in the first row and chooses the element
in the next row that is either directly below or diagonally left/right.
Specifically, the next element from position (row, col) will be
(row + 1, col - 1), (row + 1, col), or (row + 1, col + 1).
"""

"""
Identify DP problem:
- Involve optimization (minimum path sum)
- Solution can be composed from solutions of sub-problems:
  + Results of a row depend on results of the row below it.
- Overlapping sub-problems:
  + Adjacent cells in a row share common elements in the row below.

Implementation:
- Let dp(row, col) be the minimum sum of falling paths from (row, col).
  -> Find minimum of dp(row, col) for the first row
- Recurrence relation:
  . dp(row, col) = matrix[row][col] +
                   min(dp(row + 1, col - 1), 
                       dp(row + 1, col),
                       dp(row + 1, col + 1))
    (The columns must be in bound)
- Base case: the last row
  . dp(row, col) = matrix[row][col]
"""


# ===== Top-down =====
from functools import cache


def min_falling_path_sum(matrix: list[list[int]]) -> int:
    n = len(matrix)

    @cache
    def dp(row: int, col: int) -> int:
        if row == n - 1:
            return matrix[row][col]

        min_sub_path_sum: int = dp(row + 1, col)
        if col > 0:
            min_sub_path_sum = min(min_sub_path_sum, dp(row + 1, col - 1))
        if col < n - 1:
            min_sub_path_sum = min(min_sub_path_sum, dp(row + 1, col + 1))

        return matrix[row][col] + min_sub_path_sum

    return min(dp(0, col) for col in range(n))


"""
Complexity:
- Number of DP states: O(n^2)

1. Time complexity: O(n^2)

2. Space complexity: O(n^2)
- memoization table: O(n^2)
- recursion stack: O(n)
"""


# ===== Bottom-up =====
from copy import deepcopy


def min_falling_path_sum(matrix: list[list[int]]) -> int:
    n = len(matrix)

    # Initialize solutions with initial cell values
    dp: list[list[int]] = deepcopy(matrix)

    # Start building solutions from the second last row
    # The last row is unchanged (just cell values)
    for row in range(n - 2, -1, -1):
        for col in range(n):
            min_sub_path_sum: int = dp[row + 1][col]
            if col > 0:
                min_sub_path_sum = min(min_sub_path_sum, dp[row + 1][col - 1])
            if col < n - 1:
                min_sub_path_sum = min(min_sub_path_sum, dp[row + 1][col + 1])

            dp[row][col] += min_sub_path_sum

    return min(dp[0][col] for col in range(n))


"""
Complexity:
1. Time complexity: O(n^2)
2. Space complexity: O(n^2) for 'dp'
"""


# ===== Bottom-up (space-optimized) =====
"""
- The recurrence relation is static
  (results of a row only depends on results of the row below it).
  -> Only need to track the last 2 rows
  -> dp is a 1D array that stores results for a row
"""


def min_falling_path_sum(matrix: list[list[int]]) -> int:
    n = len(matrix)

    # The last row is unchanged (just cell values)
    last_dp: list[int] = deepcopy(matrix[n - 1])

    # Start building solutions from the second last row
    for row in range(n - 2, -1, -1):
        current_dp = [0] * n

        for col in range(n):
            min_sub_path_sum: int = last_dp[col]
            if col > 0:
                min_sub_path_sum = min(min_sub_path_sum, last_dp[col - 1])
            if col < n - 1:
                min_sub_path_sum = min(min_sub_path_sum, last_dp[col + 1])

            current_dp[col] = matrix[row][col] + min_sub_path_sum

        last_dp = current_dp

    return min(last_dp[col] for col in range(n))


"""
Complexity:
1. Time complexity: O(n^2)
2. Space complexity: O(n) for 'current_dp' and 'last_dp'
"""


# === Bottom-up (optimize space further) ===
"""
- Only use 1 'dp' array
- Before overwriting dp[col] for current row, 
  save dp[col] of the last row,
  since the next col will need it. 
"""


def min_falling_path_sum(matrix: list[list[int]]) -> int:
    n = len(matrix)

    # The last row is unchanged (just cell values)
    dp: list[int] = deepcopy(matrix[n - 1])

    # Start building solutions from the second last row
    for row in range(n - 2, -1, -1):
        # each dp[col] retains value from last iteration
        # (initial dp[row][col] = dp[row + 1][col])
        for col in range(n):
            min_sub_path_sum: int = dp[col]
            if col > 0:
                min_sub_path_sum = min(min_sub_path_sum, last_dp_prev_col)
            if col < n - 1:
                min_sub_path_sum = min(min_sub_path_sum, dp[col + 1])

            last_dp_prev_col = dp[col]  # save for next col
            dp[col] = matrix[row][col] + min_sub_path_sum

    return min(dp[col] for col in range(n))


"""
Complexity:
1. Time complexity: O(n^2)
2. Space complexity: O(n) for 'dp'
"""
