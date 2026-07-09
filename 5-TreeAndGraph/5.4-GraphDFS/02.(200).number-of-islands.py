"""
https://leetcode.com/problems/number-of-islands/

Given an m x n 2D binary 'grid' which represents a map of 1 (land) and 0 (water),
return the number of islands. An island is surrounded by water and is formed
by connecting adjacent land cells horizontally or vertically.
"""

"""
Analysis:
- 'grid' is an undirected graph:
  . Each 'land' square is a node.
  . left/right/up/down relationship form edges.
- The problem is asking for the number of connected components.
"""


def count_islands(grid: list[list[str]]) -> int:
    m = len(grid)  # number of rows
    n = len(grid[0])  # number of columns
    LAND = "1"

    def is_valid(row: int, col: int) -> bool:
        """Return True if node is on grid and is land."""
        return 0 <= row < m and 0 <= col < n and grid[row][col] == LAND

    # right, down, left, up
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    seen: set[tuple[int, int]] = set()  # track visited nodes

    def dfs(row: int, col: int) -> None:
        """Visit all reachable nodes."""
        for dy, dx in directions:
            next_row = row + dy
            next_col = col + dx
            if is_valid(next_row, next_col) and (next_row, next_col) not in seen:
                seen.add((next_row, next_col))
                dfs(next_row, next_col)

    def dfs_iter(start_row: int, start_col: int) -> None:
        stack: list[tuple[int, int]] = [(start_row, start_col)]
        while stack:
            row, col = stack.pop()
            for dy, dx in directions:
                next_row = row + dy
                next_col = col + dx
                if is_valid(next_row, next_col) and (next_row, next_col) not in seen:
                    seen.add((next_row, next_col))
                    stack.append((next_row, next_col))

    count = 0  # number of connected components (islands)

    for row in range(m):
        for col in range(n):
            if grid[row][col] == LAND and (row, col) not in seen:
                count += 1
                seen.add((row, col))
                dfs(row, col)

    return count


"""
Complexity:
- Number of nodes: N = O(m*n)
  Number of edges: E = O(4*N) = O(N)
  Max depth: h
  . worst case: h = O(N)

1. Time complexity: O(N + E) = O(N) = O(m*n)
- visit each node once, each edge twice.

2. Space complexity: O(N) = O(m*n)
- stack:
  . recursive approach: O(h)
  . iterative approach: O(N)
- 'seen': O(N)
"""
