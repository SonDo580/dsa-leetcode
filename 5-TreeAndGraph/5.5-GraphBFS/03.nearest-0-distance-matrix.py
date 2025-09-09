# Given an m x n binary (every element is 0 or 1) matrix 'mat',
# find the distance of the nearest 0 for each cell.
# The distance between adjacent cells (horizontally or vertically) is 1.
#
# For example, given mat = [[0,0,0],[0,1,0],[1,1,1]],
# return [[0,0,0],[0,1,0],[1,2,1]].

# Constraints:
# m == mat.length
# n == mat[i].length
# 1 <= m, n <= 10^4
# 1 <= m * n <= 10^4
# mat[i][j] is either 0 or 1.
# There is at least one 0 in mat.

# ==== Analyze =====
# - For all 0s, the distance is 0. For all 1s, we need to find the nearest 0.
# - Approach 1: Perform BFS from each 1 that stops upon finding the first 0.
#   The time complexity is O((m^2).(n^2)).
#   (Each BFS costs O(m.n), and we need to perform O(m.n) different BFS)
#   (Worst case: the entire matrix is 1s, except for a single 0)
# - Approach 2 (more efficient): Perform BFS starting from the 0s.
#   + Add all 0s to the queue first with distance 0.
#   + Start BFS, increase the distance with each level.
#   + The first time we encounter a 1, record the distance from it to the nearest 0.
#   + Don't update the answer since later encounters can only have equal or greater distance.
#     (Anyway, we don't visit the same node  again, so that's already prevented)

from collections import deque


def nearest_0_distance_matrix(mat: list[list[int]]) -> list[list[int]]:
    m = len(mat)  # number of rows
    n = len(mat[0])  # number of columns

    def is_one(row: int, col: int) -> bool:
        return 0 <= row < m and 0 <= col < n and mat[row][col] == 1

    # 4 directions: right, down, left, up
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    # Store (row, col, level)
    # level = distance to the 0 that starts the path
    queue: deque[tuple[int, int, int]] = deque()

    seen: set[tuple[int, int]] = set()  # track visited node

    # Add all 0s to the queue
    for row in range(m):
        for col in range(n):
            if mat[row][col] == 0:
                seen.add((row, col))
                queue.append((row, col, 0))

    while queue:
        row, col, level = queue.popleft()

        for dy, dx in directions:
            next_row, next_col = row + dy, col + dx
            if (next_row, next_col) not in seen and is_one(next_row, next_col):
                seen.add((next_row, next_col))
                queue.append((next_row, next_col, level + 1))

                # Record distance to the nearest 0 for the current 1
                # (create a copy of mat if don't want to mutate)
                mat[next_row][next_col] = level + 1

    return mat

# ===== Complexity =====
# 1. Time complexity: O(m.n) - BFS visit each node once, and does O(1) work each time.
# 2. Space complexity: O(m.n) - for 'queue' and 'seen'