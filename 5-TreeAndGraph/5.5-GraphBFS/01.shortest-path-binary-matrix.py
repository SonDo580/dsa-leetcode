# Given an n x n binary matrix grid,
# return the length of the shortest clear path in the matrix.
# If there is no clear path, return -1.
# A clear path is a path from the top-left cell (0, 0)
# to the bottom-right cell (n - 1, n - 1) such that all visited cells are 0.
# You may move 8-directionally (up, down, left, right, or diagonally).

# ===== Analyze =====
# - Treat the matrix as a graph, each square as a node
# - Each square has up to 8 edges (the squares on the edge have less)

# ===== Strategy =====
# - To find the shortest path, we should use BFS
#   (with BFS, the first time we visit a node, it is guaranteed that
#    we reached it with the fewest steps possible)

from typing import List
from collections import deque


def shortest_path_length(grid: List[List[int]]) -> int:
    if grid[0][0] == 1:
        return -1

    n = len(grid)

    def is_valid(row, col):
        return 0 <= row < n and 0 <= col < n and grid[row][col] == 0

    def is_bottom_right(row, col):
        return row == n - 1 and col == n - 1

    seen = {(0, 0)}  # track visited nodes
    queue = deque[(0, 0, 1)]  # row, col, path_length

    # up, down, left, right, top-left, top-right, bottom-left, bottom-right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

    while len(queue) > 0:
        row, col, path_length = queue.popleft()

        # check if bottom-right cell has been reached
        if is_bottom_right(row, col):
            return path_length

        # expand in 8 directions
        for dy, dx in directions:
            next_row = row + dy
            next_col = col + dx

            if is_valid(next_row, next_col) and (next_row, next_col) not in seen:
                # mark the node as visited
                seen.add((next_row, next_col))

                # add the valid neighbors to the queue
                # increment the path length
                queue.append((next_row, next_col, path_length + 1))

    # there's no clear path
    return -1

# ===== Complexity =====
#
# Time complexity: O(n^2)
# - the work on each node is O(1) - the queue is efficient
# - number of nodes is n^2
#
# Space complexity: O(n^2)
# - 'seen' can grow to that size