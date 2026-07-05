"""
The n-queens puzzle is the problem of placing n queens on an n x n chessboard
such that no two queens attack each other.
(a queen can attack along the row, column, and diagonals it occupies)

Given an integer n, return the number of distinct solutions to the n-queens puzzle.
"""

"""
Analysis:
- A queen can attack along the row, column and diagonals it occupies
  -> We need to place only 1 queen on each row, column, diagonal and anti-diagonal
- A brute-force approach would take O(n^(2*n)), which is way too big: 
  . the first queen has n^2 options
  . for each of the 1st queen options, the 2nd queen has n^2 - 1 options
  . ...
  . for each of the second last queen options, the last queen has n^2 - (n - 1) options
  -> Number of placements: n^2 * (n^2 - 1) * (n^2 - 2) * ... * (n^2 - (n - 1))
                           = (n^2)! / (n^2 - n)!
  -> Complexity: O(n^2 * (n^2 - 1) * (n^2 - 2) * ... * (n^2 - (n - 1)))
                 = O((n^2)^n) = O(n^(2*n))

Identify backtracking problem:
- Construct a solution step by step. At each step, there are multiple choices.
- Many choices lead to dead ends (conflicts with previously placed queens).
  When that happens, we need to undo and try another one (backtrack).

Implementation:
- Consider each row as a decision point.
- Use occupied columns and diagonals as constraints.
  -> use 3 sets / bitmasks to check which columns/diagonals has been occupied.
- If a queen cannot be placed in the current row, backtrack to the previous row.
- A valid solution is found if we can "process" all the rows.
  (since there are n queens and n rows, and each queen needs a different row)

Identify diagonals / anti-diagonals:
- Diagonal move down and right:
  . next_row - next_col = (row + 1) - (col + 1) = row - col
  -> All squares in the same diagonal has the same row - col
- Anti-diagonal move down and left:
  . next_row + next_col = (row + 1) + (col - 1) = row + col
  -> All squares in the same anti-diagonal has the same row + col.
"""


def n_queens(n: int) -> int:
    def backtrack(
        row: int,
        used_cols: set[int],
        used_diagonals: set[int],
        used_anti_diagonals: set[int],
    ) -> int:
        """Return number of solutions starting from specified states."""
        # n queens have been placed -> 1 valid solution
        if row == n:
            return 1

        num_solutions: int = 0

        for col in range(n):
            diagonal = row - col
            anti_diagonal = row + col

            if (
                col in used_cols
                or diagonal in used_diagonals
                or anti_diagonal in used_anti_diagonals
            ):
                # The queen can not be placed at current position
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


"""
Complexity:

1. Time complexity: O(n^n)
- For each (row, col) in current row, try all columns in next row.
  -> branching factor: O(n)
=> Total work: branching_factor^recursion_depth = O(n^n)

2. Space complexity:
- recursion stack: O(n)
- 3 sets: O(n)
"""
