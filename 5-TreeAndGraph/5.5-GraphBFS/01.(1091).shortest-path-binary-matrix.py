"""
https://leetcode.com/problems/shortest-path-in-binary-matrix/

Given an n x n binary matrix 'grid',
return the length of the shortest clear path in the matrix.
If there is no clear path, return -1.
A clear path is a path from the top-left cell (0, 0)
to the bottom-right cell (n - 1, n - 1) such that all visited cells are 0.
You may move 8-directionally (up, down, left, right, or diagonally).
"""

"""
Idea:
- Treat the matrix as a graph: 
  . Each square is a node.
  . Each node has up to 8 edges (the squares on the edges have less)
- To find the shortest path, use BFS:
  . The first time we visit a node, it is guaranteed that
    we reached it with the fewest steps possible.
"""

from collections import deque


def shortest_path_length(grid: list[list[int]]) -> int:
    if grid[0][0] == 1:
        return -1

    n = len(grid)

    def is_valid(row: int, col: int) -> bool:
        return 0 <= row < n and 0 <= col < n and grid[row][col] == 0

    def is_bottom_right(row: int, col: int) -> bool:
        return row == n - 1 and col == n - 1

    seen: set[tuple[int, int]] = {(0, 0)}  # track visited (node + path_length)
    queue: deque[tuple[int, int, int]] = deque([(0, 0, 1)])  # row, col, path_length

    # up, down, left, right, topleft, topright, bottomleft, bottomright
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

    while queue:
        row, col, path_length = queue.popleft()

        # check if bottom-right cell has been reached
        if is_bottom_right(row, col):
            return path_length

        # expand in 8 directions
        for dy, dx in directions:
            next_row = row + dy
            next_col = col + dx

            if is_valid(next_row, next_col) and (next_row, next_col) not in seen:
                seen.add((next_row, next_col))
                queue.append((next_row, next_col, path_length + 1))

    # there's no clear path
    return -1


"""
Complexity:
- Number of nodes: N = n^2
  Number of edges: E = O(8 * N) = O(n^2)

1. Time complexity: O(N + E) = O(n^2)
- visit each node at most once, each edge at most twice.

2. Space complexity: O(n^2)
- 'seen': O(N) = O(n^2)
- 'queue': O(n)
  . cells in the same layer share the same r + c
    . step 0: r + c = 0 -> size = 1 {(0, 0)}
    . step 1: r + c = 1 -> size = 2 {(0, 1), (1, 0)} 
    . ...
  . layer with max size: 
    . the anti-diagonal from topright corner to bottomleft corner
    . r + c = n - 1 -> size = n
"""
