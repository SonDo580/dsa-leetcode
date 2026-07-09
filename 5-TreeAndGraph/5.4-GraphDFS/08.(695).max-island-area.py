"""
https://leetcode.com/problems/max-area-of-island/

You are given an m x n binary matrix 'grid'.
An island is a group of 1's (representing land) connected 4-directionally (horizontal or vertical.)
You may assume all four edges of the grid are surrounded by water.

The area of an island is the number of cells with a value 1 in the island.

Return the maximum area of an island in grid. If there is no island, return 0.
"""

"""
Analysis:
- Let the land cells be the nodes of a graph.
- The neighbors of a node is the 4 adjacent cells in 4 directions
  (condition: is on grid AND is a land cell)
- The problem is asking for the max number of nodes in a connected component.

Idea:
- Perform DFS/BFS to count the number of nodes in each component,
  then take the largest value.
"""


def max_island_area(grid: list[list[int]]) -> int:
    m = len(grid)  # number of rows
    n = len(grid[0])  # number of columns

    def is_land(row: int, col: int) -> bool:
        return 0 <= row < m and 0 <= col < n and grid[row][col] == 1

    seen: set[tuple[int, int]] = set()  # track visited nodes

    # right, down, left, up
    directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]

    def _dfs_recur(row: int, col: int) -> int:
        """Return number of reachable nodes."""
        count = 1
        for dy, dx in directions:
            next_row, next_col = row + dy, col + dx
            if is_land(next_row, next_col) and (next_row, next_col) not in seen:
                seen.add((next_row, next_col))
                count += _dfs_recur(next_row, next_col)
        return count

    def _dfs_iter(row: int, col: int) -> int:
        """Return number of reachable nodes."""
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
                count = _dfs_recur(row, col)
                max_count = max(count, max_count)

    return max_count


"""
Complexity:
- Number of nodes: N = O(m*n)
  Number of edges: E = O(4*N) = O(N)
  Max depth: h
  . worst case: h = O(N)

1. Time complexity: O(N + E) = O(N) = O(m*n)
- visit each node once, each edge twice.

2. Space complexity: O(N) = O(m*n)
- 'seen': O(N)
- stack:
  . recursive approach: O(h)
  . iterative approach: O(N)
"""
