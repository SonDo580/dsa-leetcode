# Given a 0-indexed n x n integer matrix grid,
# return the number of pairs (ri, cj) such that row ri and column cj are equal.
# A row and column pair is considered equal if they contain the same elements
# in the same order (i.e., an equal array).

# Example 1:
# Input: grid = [[3,2,1],[1,7,6],[2,7,7]]
# Output: 1
# Explanation: There is 1 equal row and column pair:
# - (Row 2, Column 1): [2,7,7]

# Example 2:
# Input: grid = [[3,1,2,2],[1,4,4,5],[2,4,2,2],[2,4,2,2]]
# Output: 3
# Explanation: There are 3 equal row and column pairs:
# - (Row 0, Column 0): [3,1,2,2]
# - (Row 2, Column 2): [2,4,2,2]
# - (Row 3, Column 2): [2,4,2,2]

# Constraints:
# n == grid.length == grid[i].length
# 1 <= n <= 200
# 1 <= grid[i][j] <= 10^5

# ===== Strategy =====
# - Use 2 hashmap to count how many times each row/col occurs
# - For Python we can use a tuple as key.
#   For other languages, we can join the values with separator in a string.
# - Iterate over 1 hashmap. If there is corresponding key in the other hashmap,
#   the number of pairs for that key is the product of number of appearances

from collections import defaultdict


def _get_key(arr: list[int]) -> tuple[int, ...]:
    return tuple(arr)


def equal_row_col_pairs(grid: list[list[int]]) -> int:
    row_dict: defaultdict[tuple[int, ...], int] = defaultdict(int)
    for row_arr in grid:
        row_dict[_get_key(row_arr)] += 1

    col_dict: defaultdict[tuple[int, ...], int] = defaultdict(int)
    for col in range(len(grid[0])):
        col_arr: list[int] = []
        for row in range(len(grid)):
            col_arr.append(grid[row][col])
        col_dict[_get_key(col_arr)] += 1

    count = 0
    for key in row_dict:
        count += row_dict[key] * col_dict[key]

    return count


# ===== Complexity =====
# 1. Time complexity:
# - There are n^2 elements.
#   Each element is iterate over twice when building row_dict and col_dict.
# - Iterating over 1 of the 2 hashmaps takes O(n)
#   (worst case when all rows/cols are unique).
# => Overall: O(n^2)
#
# 2. Space complexity:
# - If all rows and columns are unique, each hash map will both grow to size of n,
#   with each key having a length of n
# => O(n^2)
