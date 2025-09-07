# You are given an m x n binary matrix grid.
# An island is a group of 1's (representing land) connected 4-directionally (horizontal or vertical.)
# You may assume all four edges of the grid are surrounded by water.
#
# The area of an island is the number of cells with a value 1 in the island.
#
# Return the maximum area of an island in grid. If there is no island, return 0.

# Example 1:
# Input:
# grid = [
#     [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
#     [0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0],
#     [0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
# ]
# Output: 6
# Explanation: The answer is not 11, because the island must be connected 4-directionally.

# Example 2:
# Input: grid = [[0,0,0,0,0,0,0,0]]
# Output: 0

# Constraints:
# m == grid.length
# n == grid[i].length
# 1 <= m, n <= 50
# grid[i][j] is either 0 or 1.

# ===== Analyze =====
# - Let the land cells be the nodes of a graph.
# - The neighbors of a node is the 4 adjacent cells in 4 directions,
#   (condition: is a land cell AND is on grid)
# - The problem is asking for the max number of nodes in a connected component.
# - We can perform a traversal (let choose DFS) to count the number of nodes in each component,
#   then take the largest value.


def max_island_area(grid: list[list[int]]) -> int:
    m = len(grid)  # number of rows
    n = len(grid[0])  # number of columns

    def is_land(row: int, col: int) -> bool:
        """Check if (row, col) is a valid land cell"""
        return 0 <= row < m and 0 <= col < n and grid[row][col] == 1

    seen: set[tuple[int, int]] = set()  # track visited nodes

    # 4 possible directions: right, down, left, up
    directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]

    def dfs_recur(row: int, col: int) -> int:
        """Count number of nodes in a connected component"""
        count = 1
        for dy, dx in directions:
            next_row, next_col = row + dy, col + dx
            if is_land(next_row, next_col) and (next_row, next_col) not in seen:
                seen.add((next_row, next_col))
                count += dfs_recur(next_row, next_col)
        return count

    def dfs_iter(row: int, col: int) -> int:
        """Count number of nodes in a connected component"""
        stack: list[tuple[int, int]] = [(row, col)]
        count = 0

        while stack:
            current_row, current_col = stack.pop()
            count += 1

            for dy, dx in directions:
                next_row, next_col = current_row + dy, current_col + dx
                if is_land(next_row, next_col) and (next_row, next_col) not in seen:
                    seen.add((next_row, next_col))
                    stack.append((next_row, next_col))

        return count

    max_count: int = 0  # max number of nodes in a connected component
    for row in range(m):
        for col in range(n):
            if is_land(row, col) and (row, col) not in seen:
                # start a new connected component
                seen.add((row, col))
                count = dfs_recur(row, col)
                max_count = max(count, max_count)

    return max_count
