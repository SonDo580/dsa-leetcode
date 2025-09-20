# The n-queens puzzle is the problem of placing n queens on an n x n chessboard
# such that no two queens attack each other.
# (a queen can attack along the row, column, and diagonals it occupies)
#
# Given an integer n, return the number of distinct solutions to the n-queens puzzle.

# Example 1:
# Input: n = 4
# Output: 2
# Explanation: There are two distinct solutions to the 4-queens puzzle as shown.

# Example 2:
# Input: n = 1
# Output: 1

# Constraints:
# 1 <= n <= 9


# ===== Analysis =====
# - A queen can attack along the row, column and diagonals it occupies
#   => We need to place only 1 queen on each row, column, diagonal and anti-diagonal
# 
# - A brute-force approach would take O(n^n), which is way too big: 
#   . the first queen has n^2 options
#   . for each of the first queen options, 
#     the second queen has n^2 - 1 options
#   . ...
#   . for each of the second last queen options, 
#     the last queen has n^2 - (n - 1) options
#   -> Number of placements: 
#        n^2 * (n^2 - 1) * (n^2 - 2) * ... * (n^2 - (n - 1))
#      = (n^2)! / (n^2 - n)!
#   -> Complexity: 
#        O(n^2 * (n^2 - 1) * (n^2 - 2) * ... * (n^2 - (n - 1)))
#      ~ O((n^2)^n) 
#      ~ O(n^n)

# ===== Identify backtracking problem ====
# - We must construct a solution step by step. At each step, there are multiple choices.
# - Many choices lead to dead ends (conflicts with previously placed queens).
#   When that happens, we need to undo and try another one (backtrack).
#
# => For the current problem:
# - Consider each row as a decision point.
# - Use occupied columns and diagonals as constraints.
# - If a queen cannot be placed in the current row, backtrack to the previous row.
# - A valid solution is found if we can "process" all the rows.
#   (Since there are n queens and n rows, and each queen needs a different row)

# ===== Implementation =====
# - Consider 1 row per backtrack call. Pass row as an argument.
#   When row = n, we found a valid solution.
# - Use columns / diagonals / anti-diagonals as constraints.
#   Use 3 sets to track which column / diagonal / anti-diagonal has been occupied.
#   When we place a queen, add column / diagonal / anti-diagonal to the set.
#   When we backtrack and remove a queen, remove column / diagonal / anti-diagonal from the set.
# - All squares in the same diagonal has the same row - col.
#   Diagonal move down and right, so both row and col get incremented.
#   . next_row - next_col = (row + 1) - (col + 1) = row - col
# - All squares in the same anti-diagonal has the same row + col.
#   Anti-diagonal move down and left, so row gets incremented and col get decremented.
#   . next_row + next_col = (row + 1) + (col - 1) = row + col


def n_queens(n: int) -> int:
    def backtrack(
        row: int,
        used_cols: set[int],
        used_diagonals: set[int],
        used_anti_diagonals: set[int],
    ) -> int:
        # n queens have been placed -> 1 valid solution
        if row == n:
            return 1

        num_solutions: int = 0

        for col in range(n):
            diagonal = row - col
            anti_diagonal = row + col

            # If the queen can not be placed at current position
            if (
                col in used_cols
                or diagonal in used_diagonals
                or anti_diagonal in used_anti_diagonals
            ):
                continue

            # Place a queen at current position
            used_cols.add(col)
            used_diagonals.add(diagonal)
            used_anti_diagonals.add(anti_diagonal)

            # Move on to the next row with updated board state
            num_solutions += backtrack(
                row + 1, used_cols, used_diagonals, used_anti_diagonals
            )

            # Remove the queen from the board
            used_cols.remove(col)
            used_diagonals.remove(diagonal)
            used_anti_diagonals.remove(anti_diagonal)

        return num_solutions

    return backtrack(0, set(), set(), set())
