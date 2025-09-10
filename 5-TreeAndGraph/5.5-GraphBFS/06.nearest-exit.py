# You are given an m x n matrix maze (0-indexed)
# with empty cells (represented as '.') and walls (represented as '+').
# You are also given the entrance of the maze,
# where entrance = [entrancerow, entrancecol]
# denotes the row and column of the cell you are initially standing at.
#
# In one step, you can move one cell up, down, left, or right.
# You cannot step into a cell with a wall, and you cannot step outside the maze.
# Your goal is to find the nearest exit from the entrance.
# An exit is defined as an empty cell that is at the border of the maze.
# The entrance does not count as an exit.
#
# Return the number of steps in the shortest path from the entrance
# to the nearest exit, or -1 if no such path exists.

# Example 1:
# Input: maze = [["+","+",".","+"],[".",".",".","+"],["+","+","+","."]], entrance = [1,2]
# Output: 1
# Explanation: There are 3 exits in this maze at [1,0], [0,2], and [2,3].
# Initially, you are at the entrance cell [1,2].
# - You can reach [1,0] by moving 2 steps left.
# - You can reach [0,2] by moving 1 step up.
# It is impossible to reach [2,3] from the entrance.
# Thus, the nearest exit is [0,2], which is 1 step away.

# Example 2:
# Input: maze = [["+","+","+"],[".",".","."],["+","+","+"]], entrance = [1,0]
# Output: 2
# Explanation: There is 1 exit in this maze at [1,2].
# [1,0] does not count as an exit since it is the entrance cell.
# Initially, you are at the entrance cell [1,0].
# - You can reach [1,2] by moving 2 steps right.
# Thus, the nearest exit is [1,2], which is 2 steps away.

# Example 3:
# Input: maze = [[".","+"]], entrance = [0,0]
# Output: -1
# Explanation: There are no exits in this maze.

# Constraints:
# maze.length == m
# maze[i].length == n
# 1 <= m, n <= 100
# maze[i][j] is either '.' or '+'.
# entrance.length == 2
# 0 <= entrance_row < m
# 0 <= entrance_col < n
# entrance will always be an empty cell.


# ===== Strategy =====
# - Perform BFS from entrance, increment the number of steps with each level
# - The first time we reach an exit, that's the shortest path -> return number of steps
# - If we cannot reach any exit, return -1

from collections import deque


class Solution:
    def nearestExit(self, maze: list[list[str]], entrance: list[int]) -> int:
        m = len(maze)  # number of rows
        n = len(maze[0])  # number of columns

        def is_valid(row: int, col: int) -> bool:
            return 0 <= row < m and 0 <= col < n and maze[row][col] == "."

        def is_at_border(row: int, col: int) -> bool:
            return row == 0 or row == m - 1 or col == 0 or col == n - 1

        def is_exit(row: int, col: int) -> bool:
            return (
                is_valid(row, col) and is_at_border(row, col) and [row, col] != entrance
            )

        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # (dy, dx)

        seen: set[tuple[int, int]] = {tuple(entrance)}  # track visited nodes (row, col)
        queue: deque[tuple[int, int, int]] = deque(
            [(entrance[0], entrance[1], 0)]
        )  # (row, col, number of steps)

        while queue:
            row, col, steps = queue.popleft()

            # Reached nearest exit -> return number of steps
            if is_exit(row, col):
                return steps

            for dy, dx in directions:
                next_row, next_col = row + dy, col + dx
                if is_valid(next_row, next_col) and (next_row, next_col) not in seen:
                    seen.add((next_row, next_col))
                    queue.append((next_row, next_col, steps + 1))

        return -1  # cannot reach exit
