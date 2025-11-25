"""
https://leetcode.com/problems/path-with-minimum-effort

You are a hiker preparing for an upcoming hike.
You are given 'heights', a 2D array of size rows x columns,
where heights[row][col] represents the height of cell (row, col).

You are situated in the top-left cell, (0, 0),
and you hope to travel to the bottom-right cell,
(rows-1, columns-1) (i.e., 0-indexed).

You can move up, down, left, or right,
and you wish to find a route that requires the minimum effort.

A route's effort is the maximum absolute difference in heights
between two consecutive cells of the route.

Return the minimum effort required to travel
from the top-left cell to the bottom-right cell.

Example 1:
Input: heights =
[[1,2,2],
 [3,8,2],
 [5,3,5]]
Output: 2
Explanation: The route of [1,3,5,3,5] has a maximum absolute difference of 2 in consecutive cells.
This is better than the route of [1,2,2,2,5], where the maximum absolute difference is 3.

Example 2:
Input: heights =
[[1,2,3],
 [3,8,4],
 [5,3,5]]
Output: 1
Explanation: The route of [1,2,3,4,5] has a maximum absolute difference of 1 in consecutive cells, which is better than route [1,3,5,3,5].

Example 3:
Input: heights =
[[1,2,1,1,1],
 [1,2,1,2,1],
 [1,2,1,2,1],
 [1,2,1,2,1],
 [1,1,1,2,1]]
Output: 0
Explanation: This route does not require any effort.

Constraints:
rows == heights.length
columns == heights[i].length
1 <= rows, columns <= 100
1 <= heights[i][j] <= 10^6
"""

"""
Analysis:
- Let the minimum effort to complete the journey 'effort'
  Then any value greater than it is possible,
  and any value less than it is impossible.

- Given an effort, we need to check if a valid path exists.
  + Perform DFS starting from 0, with edges are the 4 directions and
    only traversable if difference <= effort.
  + Also check if cell is valid and hasn't been visited.
    (There's already a valid path up to that cell, so don't visit it again)
  + If there is a possible path, try to find smaller effort.
    Otherwise try a bigger effort.

- We can perform binary search for the optimal solution
  + The lower bound is 0 (a path where all numbers are the same)
  + The upper bound is the largest value in the input space,
    since the input doesn't have negative number.
    (The "real" upper bound is the maximum difference between 2 adjacent cells)
"""


def min_effort_path(heights: list[list[int]]) -> int:
    m = len(heights)  # number of rows
    n = len(heights[0])  # number of columns

    # right, down, left, up
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    def _is_valid_cell(row: int, col: int) -> bool:
        return 0 <= row < m and 0 <= col < n

    def _is_destination(row: int, col: int) -> bool:
        return row == m - 1 and col == n - 1

    def _has_valid_path(effort: int) -> bool:
        """Check if there's a valid path with path_effort <= effort"""
        stack = [(0, 0)]
        seen = {(0, 0)}

        while stack:
            row, col = stack.pop()
            if _is_destination(row, col):
                return True

            for dx, dy in directions:
                next_row, next_col = row + dx, col + dy

                if (
                    _is_valid_cell(next_row, next_col)
                    and (next_row, next_col) not in seen
                    and abs(heights[next_row][next_col] - heights[row][col]) <= effort
                ):
                    stack.append((next_row, next_col))
                    seen.add((next_row, next_col))

        return False

    left = 0
    right = max(max(row) for row in heights)

    while left <= right:
        mid = (left + right) // 2
        if _has_valid_path(mid):
            right = mid - 1  # search left portion for smaller effort
        else:
            left = mid + 1  # search right portion for valid effort

    return left


"""
Complexity:
Let m = number of rows, n = number of columns
    k = maximum value in the 2D array

1. Time complexity:
- Find upper bound (max value in 2D array): O(m * n)
- Binary search for minimum effort: O(log(k))
- DFS to find valid path: O(m * n)
  + each cell is visited at most once: O(m * n)
  + each visit check at most 4 directions: O(1)
=> Overall: O(m * n * log(k))

2. Space complexity:
- 'seen' set: O(m * n) 
- stack: O(m * n) 
=> Overall: O(m * n)
"""
