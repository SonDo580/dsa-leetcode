"""
https://leetcode.com/problems/n-queens-ii/

The n-queens puzzle is the problem of placing n queens on an n x n chessboard
such that no two queens attack each other.
(a queen can attack along the row, column, and diagonals it occupies)

Given an integer n, return the number of distinct solutions to the n-queens puzzle.
"""

"""
Analysis:
- Number of rows/columns/diagonals/anti-diagonals = n
- A queen can attack along the row/column/diagonal/anti-diagonal it occupies.
  And we need to place n queens.
  -> Each row/column/diagonal/anti-diagonal only contains 1 queen.

Idea:
- Use backtracking to find all valid placements. 
- Consider each row as a decision point.
  Use occupied columns/diagonals/anti-diagonals as constraints.
- 1 valid solution is found when all rows are processed.

Identify diagonals / anti-diagonals:
- Diagonals move down and right:
  . next_row - next_col = (row + 1) - (col + 1) = row - col
  -> all squares in the same diagonal has the same (row - col)
- Anti-diagonals move down and left:
  . next_row + next_col = (row + 1) + (col - 1) = row + col
  -> all squares in the same anti-diagonal has the same (row + col)

Represent occupied columns (and diagonals/anti-diagonals) with bitmask:
- Use an integer used_cols where the ith bit is 1 if the ith column is used.
- Initially, used_cols = 0 (no columns have been used).
- Check if ith bit is 1 (to check if column is occupied): 
  . method 1: (used_cols >> i) & 1) == 1
  . method 2: (used_cols & (1 << i)) != 0   (> 0 to be exact)
- Flip ith bit (to place/remove a queen): used_cols = used_cols ^ (1 << i).

- Use the same logic for diagonals and anti_diagonals
- For diagonals, (row - col) can be negative
  -> Add a constant C to normalize into non-negative range for shifting operation.
     . min_diff = min_row - max_col = 0 - (n - 1) = -(n - 1)
       -> C >= -min_diff = n - 1
       -> choose C = n
"""


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
            anti_diagonal_mask = 1 << (row + col)
            # add n to normalized into non-negative range
            diagonal_mask = 1 << (row - col + n)

            # If the queen can not be placed at current position
            # (column/diagonal/anti-diagonal has been occupied)
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

    return backtrack(row=0, used_cols=0, used_diagonals=0, used_anti_diagonals=0)


"""
Complexity:
(In the following analysis, '^' denotes power, not XOR)

1. Time complexity: O(n^n)
- For each (row, col) in current row, try all columns in next row.
  -> branching factor: O(n)
=> Total work: branching_factor^recursion_depth = O(n^n)

2. Space complexity: O(n) for recursion stack
"""
