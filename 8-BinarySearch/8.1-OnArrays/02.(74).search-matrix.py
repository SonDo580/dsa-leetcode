"""
https://leetcode.com/problems/search-a-2d-matrix

Write an efficient algorithm that searches for a value 'target' in an m x n integer matrix 'matrix'.
Integers in each row are sorted from left to right.
The first integer of each row is greater than the last integer of the previous row.

Analysis:
- each row is sorted and all numbers are less than numbers in the next row
  -> we can treat the matrix as 1 array to perform binary search
- now we need to map the index of the hypothetical array to the correct row and col
  + the row increment every n indices -> row = i // n
  + the column reset to 0 every n indices -> col = i % n
"""


def search_matrix(matrix: list[list[int]], target: int) -> bool:
    m = len(matrix)  # number of rows
    n = len(matrix[0])  # number of columns

    # indices on the hypothetical array
    left = 0
    right = m * n - 1

    while left <= right:
        mid = (left + right) // 2
        row = mid // n
        col = mid % n
        num = matrix[row][col]

        if num == target:
            return True

        if num < target:
            left = mid + 1
        else:
            right = mid - 1

    return False

"""
Time complexity: O(log(m*n))
Space complexity: O(1)
"""
