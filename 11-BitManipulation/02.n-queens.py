# The n-queens puzzle is the problem of placing n queens on an n x n chessboard
# such that no two queens attack each other.
# (a queen can attack along the row, column, and diagonals it occupies)
#
# Given an integer n, return the number of distinct solutions to the n-queens puzzle.


# ===== Analysis =====
# - This is the same problem in 9.2/02 (n-queens)

# ===== Alternative approach =====
# - We'll use the same algorithm, but using bitmask instead of sets,
#   which improves space usage.
# - It also improves time, since sets have hashing overhead
#   (even though the complexity is O(1)).

# ===== Implementation =====
# - Use an integer used_cols where the ith bit is 1 if the ith column is used.
# - Initialize used_cols to 0 (no columns has been used)
# - To check the ith bit, use a mask col_mask = 1 << i
#   and perform col_mask & used_cols.
#   + If the result is not 0, that means the ith bit is 1 (column already used)
#   + If the result is 0, that means the ith bit is 0 (column has not been used)
# - We can place a queen at a column by changing the bit to 1.
#   To do that, set used_cols = col_mask ^ used_cols
# - When we remove a queen, the same operation will undo it:
#   used_cols = col_mask ^ used_cols
#
# - Use the same logic for diagonals and anti_diagonals
# - For diagonals, i = row - col can be negative.
#   But we cannot do negative bit shifts.
#   => Add a constant to make sure it doesn't go negative
#      . min_const = max_col - min_row = n - 1 - 0 = n - 1
#      -> Let's use n

# ===== Bit operation properties used =====
# - a & 1 = a
#   a & 0 = 0
# - a ^ 1 = 1 if a = 0
#   a ^ 1 = 0 if a = 1


def n_queens(n: int) -> int:
    def backtrack(
        row: int,
        used_cols: int,
        used_diagonals: int,
        used_anti_diagonals: int,
    ) -> int:
        # n queens have been placed -> 1 valid solution
        if row == n:
            return 1

        num_solutions: int = 0

        for col in range(n):
            col_mask = 1 << col
            diagonal_mask = 1 << (row - col + n)  # add n to avoid going negative
            anti_diagonal_mask = 1 << (row + col)

            # If the queen can not be placed at current position
            if (
                col_mask & used_cols
                or diagonal_mask & used_diagonals
                or anti_diagonal_mask & used_anti_diagonals
            ):
                continue

            # Place a queen at current position
            used_cols ^= col_mask
            used_diagonals ^= diagonal_mask
            used_anti_diagonals ^= anti_diagonal_mask

            # Move on to the next row with updated board state
            num_solutions += backtrack(
                row + 1, used_cols, used_diagonals, used_anti_diagonals
            )

            # Remove the queen from the board
            used_cols ^= col_mask
            used_diagonals ^= diagonal_mask
            used_anti_diagonals ^= anti_diagonal_mask

        return num_solutions

    return backtrack(0, 0, 0, 0)
