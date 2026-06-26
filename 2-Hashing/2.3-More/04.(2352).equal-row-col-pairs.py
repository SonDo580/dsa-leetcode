"""
https://leetcode.com/problems/equal-row-and-column-pairs/

Given a 0-indexed n x n integer matrix 'grid',
return the number of pairs (ri, cj) such that row ri and column cj are equal.
A row and column pair is considered equal if they contain the same elements
in the same order (i.e., an equal array).
"""

"""
Idea:
- Use 2 hashmaps to count how many times each row/col occurs
- For Python we can use a tuple as key.
  For other languages, we can join the values with separator in a string.
- Iterate over 1 hashmap. If there is corresponding key in the other hashmap,
  the number of pairs for that key is the product of number of appearances
"""


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


"""
Complexity:
1. Time complexity: O(n^2)
- There are n^2 elements.
  Each element is iterated over twice when building row_dict and col_dict.
- Iterating over 1 hashmap takes O(n)
  (worst case when all rows/cols are unique).

2. Space complexity: O(n^2)
- If all rows and columns are unique, each hash map will both grow to size of n,
  with each key having a length of n
"""
