# Given an n x n array of integers matrix,
# return the minimum sum of any falling path through matrix.
#
# A falling path starts at any element in the first row and chooses the element
# in the next row that is either directly below or diagonally left/right.
# Specifically, the next element from position (row, col) will be
# (row + 1, col - 1), (row + 1, col), or (row + 1, col + 1).

# Example 1:
# Input: matrix = [[2,1,3],[6,5,4],[7,8,9]]
# Output: 13
# Explanation: There are two falling paths with a minimum sum as shown.

# Example 2:
# Input: matrix = [[-19,57],[-40,-5]]
# Output: -59
# Explanation: The falling path with a minimum sum is shown.

# Constraints:
# n == matrix.length == matrix[i].length
# 1 <= n <= 100
# -100 <= matrix[i][j] <= 100


# ===== Identify DP problem =====
# - Involve optimization (minimum path sum)
# - Solution can be composed from solutions of sub-problems:
#   + Results of a row depend on results of the row below it.
# - Overlapping sub-problems:
#   + Adjacent cells in a row share common paths starting from the row below it.

# ===== Implementation =====
# - Let dp(row, col) be the minimum sum of falling paths from (row, col).
#   -> Find minimum of dp(row, col) for the first row
# - Recurrence relation:
#   dp(row, col) = matrix[row][col] +
#                  min(dp(row + 1, col - 1), dp(row + 1, col), dp(row + 1, col + 1))
#   (The columns must be in bound)
# - Base case - the last row:
#   dp(row, col) = matrix[row][col]


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


# ===== Bottom-up (space-optimized) =====
# - The recurrence relation is static
#   (results of a row only depends on results of the row below it).
#   -> Only need to track the last 2 rows
#   -> dp is a 1D array that stores results for a row
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
