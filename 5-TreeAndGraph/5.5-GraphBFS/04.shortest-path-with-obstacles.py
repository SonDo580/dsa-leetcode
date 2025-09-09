# You are given an m x n integer matrix grid
# where each cell is either 0 (empty) or 1 (obstacle).
#
# You can move up, down, left, or right from and to an empty cell in one step.
#
# Return the minimum number of steps to walk
# from the upper left corner to the lower right corner
# given that you can eliminate at most k obstacles.
#
# If it is not possible, return -1.

# ===== Analyze =====
# - This is almost the same as problem '5.5/01'
# - Add a state variable 'remain' to track how many obstacles removals we have remaining
# - If a node is an obstacle, we can walk over it if remain > 0

# ===== Implementation notes =====
# - Use 'seen' to avoid visiting the same state twice.
#   The state is (node, remain) instead of just 'node'.

from collections import deque


def shortest_path_with_obstacles(grid: list[list[int]], k: int) -> int:
    m = len(grid)  # number of rows
    n = len(grid[0])  # number of columns

    def is_valid(row: int, col: int) -> bool:
        return 0 <= row < m and 0 <= col < n

    def is_bottom_right(row: int, col: int) -> bool:
        return row == m - 1 and col == n - 1

    # Track visited states (row, col, remain)
    seen: set[tuple[int, int, int]] = {(0, 0, k)}

    # Store (row, col, remain, path_length)
    queue: deque[tuple[int, int, int, int]] = deque([(0, 0, k, 0)])

    # 4 directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        row, col, remain, path_length = queue.popleft()

        # check if bottom-right cell has been reached
        if is_bottom_right(row, col):
            return path_length

        for dy, dx in directions:
            next_row, next_col = row + dy, col + dx

            if not is_valid(next_row, next_col):
                continue

            # If this is an empty cell, continue normally
            if grid[next_row][next_col] == 0:
                if (next_row, next_col, remain) not in seen:
                    seen.add((next_row, next_col, remain))
                    queue.append((next_row, next_col, remain, path_length + 1))

            # Otherwise this is an obstacle
            # We can only pass if we have remaining removals
            elif remain > 0 and (next_row, next_col, remain - 1) not in seen:
                seen.add((next_row, next_col, remain - 1))
                queue.append((next_row, next_col, remain - 1, path_length + 1))

    return -1

# ===== Complexity =====
# - Let s be the number of possible states
#   state = (node, remain)
#   there m.n nodes and k values for remain
#   => s = m.n.k
# 
# 1. Time complexity: O(s) = O(m.n.k)
# - We visit each state once, and do O(1) work at each state.
# 
# 2. Space complexity: O(s) = O(m.n.k)
# - Space for 'seen' and 'queue' 