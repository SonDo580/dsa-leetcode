# Given an m x n 2D binary grid which represents a map of 1 (land) and 0 (water),
# return the number of islands. An island is surrounded by water and is formed
# by connecting adjacent land cells horizontally or vertically.

# ===== Analyze =====
# - Each 'land' square is a node, the left/right/up/down relationship form edges
# - The problem is asking for the number of connected components
# - The graph is undirected

from typing import List


def count_islands(grid: List[List[int]]) -> int:
    m = len(grid)  # number of rows
    n = len(grid[0])  # number of columns

    seen = set()  # track visited nodes
    count = 0  # number of connected components

    # 4 directions to move
    # right  # down  # left  # up
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    def is_valid(row, col):
        """Check if the cell is a land cell"""
        return 0 <= row < m and 0 <= col < n and grid[row][col] == 1

    def dfs(row, col):
        """Visit all nodes in a connected component"""

        # mark the current node as visited
        seen.add((row, col))

        # visit the neighbors
        for dy, dx in directions:
            next_row = row + dy
            next_col = col + dx

            if is_valid(next_row, next_col) and (next_row, next_col) not in seen:
                dfs(next_row, next_col)

    def dfs_iterative(start_row, start_col):
        stack = [(start_row, start_col)]

        while len(stack) > 0:
            row, col = stack.pop()

            for dy, dx in directions:
                next_row = row + dy
                next_col = col + dx

                if is_valid(next_row, next_col) and (next_row, next_col) not in seen:
                    seen.add((next_row, next_col))
                    stack.append((next_row, next_col))

    for row in range(m):
        for col in range(n):
            if grid[row][col] == 1 and (row, col) not in seen:
                count += 1
                dfs(row, col)

    return count

# ===== Complexity =====
# 
# Time complexity:
# - DFS on graph: O(m*n)
#   + each node is visited once: O(m*n)
#   + each edge is visited twice, 4 edges to check per nodes: O(m*n)
#     (although we check the validity of the next cell)
# => Overall O(m*n)
