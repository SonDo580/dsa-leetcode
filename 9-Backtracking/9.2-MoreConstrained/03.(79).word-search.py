"""
https://leetcode.com/problems/word-search/

Given an m x n grid of characters 'board' and a string 'word',
return true if 'word' exists in the grid.
The word can be constructed from letters of sequentially adjacent cells,
where adjacent cells are horizontally or vertically neighboring.
The same letter cell may not be used more than once.
"""

"""
Analysis:
- The input is a graph where each square is a node, and there are edges between adjacent squares.
- The problem is backtracking, not just DFS, because we may visit a square multiple times.
  (We aren't allowed to use a square more than once for each path,
   but we can use that same square in different paths).

Strategy:
- Use backtracking to build words. States needed:
  . (row, col): the current node.
  . i: search for character word[i] next. 
  . seen: store visited nodes on the current path
          (to avoid using a square multiple times in the same path)
- Only traverse an edge if the next square contains word[i]
- The answer could start from any square 
  -> start exploring from all squares that contains word[0]
- Return True as soon as we find a valid answer.
"""


def word_exists(board: list[list[str]], word: str) -> bool:
    m = len(board)
    n = len(board[0])

    def is_on_board(row: int, col: int) -> bool:
        return 0 <= row < m and 0 <= col < n

    # right, down, left, up
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    def backtrack(row: int, col: int, i: int, seen: set[tuple[int, int]]) -> bool:
        """Return True if 'word' can be built starting from specified states."""
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


"""
Complexity:
- Number of nodes in graph: m*n
- Max number of neighbors per node: 4

1. Time complexity: O(4^(m*n))
- Each 'backtrack' call explores O(4) neighbors.
  -> branching factor: O(4)
=> Total work: branching_factor^recursion_depth = O(4^(m*n))

2. Space complexity:
- recursion stack: O(m*n)
- 'seen' set: O(m*n)
"""


# === Alternative implementation ===
def word_exists(board: list[list[str]], word: str) -> bool:
    m = len(board)
    n = len(board[0])

    def is_on_board(row: int, col: int) -> bool:
        return 0 <= row < m and 0 <= col < n

    # right, down, left, up
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    ans: bool = False

    def backtrack(row: int, col: int, i: int, seen: set[tuple[int, int]]) -> None:
        nonlocal ans

        if ans:  # already found a valid answer
            return

        if i == len(word):
            ans = True
            return

        for dy, dx in directions:
            next_row, next_col = row + dy, col + dx
            if (
                is_on_board(next_row, next_col)
                and (next_row, next_col) not in seen
                and board[next_row][next_col] == word[i]
            ):
                seen.add((next_row, next_col))
                backtrack(next_row, next_col, i + 1, seen)
                if ans:
                    return
                seen.remove((next_row, next_col))

    for row in range(m):
        for col in range(n):
            if board[row][col] != word[0]:
                continue
            backtrack(row, col, i=1, seen={(row, col)})
            if ans:
                break

    return ans
