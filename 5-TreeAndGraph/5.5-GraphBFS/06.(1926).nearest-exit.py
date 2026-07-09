"""
https://leetcode.com/problems/nearest-exit-from-entrance-in-maze/

You are given an m x n matrix maze (0-indexed)
with empty cells (represented as '.') and walls (represented as '+').
You are also given the entrance of the maze,
where entrance = [entrancerow, entrancecol]
denotes the row and column of the cell you are initially standing at.

In one step, you can move one cell up, down, left, or right.
You cannot step into a cell with a wall, and you cannot step outside the maze.
Your goal is to find the nearest exit from the entrance.
An exit is defined as an empty cell that is at the border of the maze.
The entrance does not count as an exit.

Return the number of steps in the shortest path from the entrance
to the nearest exit, or -1 if no such path exists.
"""

"""
Idea:
- Perform BFS from entrance, increment the number of steps with each level.
- The first time we reach an exit, that's the shortest path -> return number of steps.
- If we cannot reach any exit, return -1.
"""

from collections import deque


class Solution:
    def nearestExit(self, maze: list[list[str]], entrance: list[int]) -> int:
        m = len(maze)  # number of rows
        n = len(maze[0])  # number of columns

        def is_valid(row: int, col: int) -> bool:
            return 0 <= row < m and 0 <= col < n and maze[row][col] == "."

        def is_exit(row: int, col: int) -> bool:
            is_at_border = row == 0 or row == m - 1 or col == 0 or col == n - 1
            return is_valid(row, col) and is_at_border and [row, col] != entrance

        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # (dy, dx)

        seen: set[tuple[int, int]] = {tuple(entrance)}  # track visited (row, col)
        queue: deque[tuple[int, int, int]] = deque(
            [(entrance[0], entrance[1], 0)]
        )  # (row, col, number of steps)

        while queue:
            row, col, steps = queue.popleft()

            # Reached nearest exit
            if is_exit(row, col):
                return steps

            for dy, dx in directions:
                next_row, next_col = row + dy, col + dx
                if is_valid(next_row, next_col) and (next_row, next_col) not in seen:
                    seen.add((next_row, next_col))
                    queue.append((next_row, next_col, steps + 1))

        return -1  # cannot reach exit


"""
Complexity:
- Number of nodes: N = m*n
  Number of edges: E = O(4 * num_nodes) = O(m*n)

1. Time complexity: O(N + E) = O(m*n)

2. Space complexity: O(N) = O(m*n)
- 'seen': O(N)
- queue: O(N) 
"""
