# Given an m x n grid of characters 'board' and a string 'word',
# return true if 'word' exists in the grid.
# The word can be constructed from letters of sequentially adjacent cells,
# where adjacent cells are horizontally or vertically neighboring.
# The same letter cell may not be used more than once.


# ===== Analysis =====
# - The input is a graph where each square is a node, and there are edges between adjacent squares.
# - The problem is backtracking, not just DFS, because we may visit a square multiple times.
#   (We aren't allowed to use a square more than once for each path,
#    but we can use that same square in different paths).

# ===== Strategy =====
# - Use a recursive function backtrack(row, col, i, seen) to build words.
#   . (row, col): the current node
#   . i: we are looking for the ith character of 'word'
#   . seen: store visited nodes on the current path
# - Use 'seen' to avoid using a square multiple times in the same path.
#   (add items when explore, pop items when backtrack)
# - Only traverse an edge if the next square contains word[i]
#   The answer could start from any square -> start exploring from all squares that contains word[0]
# - Return True as soon as we find a valid answer.


def word_exists(board: list[list[str]], word: str) -> bool:
    m = len(board)
    n = len(board[0])

    def is_on_board(row: int, col: int) -> bool:
        return 0 <= row < m and 0 <= col < n

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    def backtrack(row: int, col: int, i: int, seen: set[tuple[int, int]]) -> bool:
        if i == len(word):
            return True

        for dy, dx in directions:
            next_row, next_col = row + dy, col + dx
            if (
                is_on_board(next_row, next_col)
                and (next_row, next_col) not in seen
                and board[next_row][next_col] == word[i]
            ):

                seen.add((next_row, next_col))
                if backtrack(next_row, next_col, i + 1, seen):
                    return True
                seen.remove((next_row, next_col))

        return False

    for row in range(m):
        for col in range(n):
            if board[row][col] == word[0] and backtrack(
                row, col, i=1, seen={(row, col)}
            ):
                return True

    return False
