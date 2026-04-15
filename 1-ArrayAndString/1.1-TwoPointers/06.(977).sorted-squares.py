"""
https://leetcode.com/problems/squares-of-a-sorted-array/

Given an integer array 'nums' sorted in non-decreasing order,
return an array of the squares of each number
sorted in non-decreasing order.
"""

"""
Analysis:
- Since 'nums' may contain negative numbers,
  either end can produce the larger square.
-> We should populate 'squares' in reverse order.
   Use 2 pointers on 'nums' to track the next largest square.
"""


def sorted_squares(nums: list[int]) -> list[int]:
    n = len(nums)
    squares = [None] * len(nums)

    # pointers to nums
    i = 0
    j = n - 1

    # pointer to squares
    k = n - 1

    while i < j:
        square1 = nums[i] ** 2
        square2 = nums[j] ** 2

        if square1 > square2:
            squares[k] = square1
            i += 1
        else:
            squares[k] = square2
            j -= 1
        k -= 1

    if i == j:
        squares[k] = nums[i] ** 2

    return squares


"""
Complexity:
- Let n = len(nums) 
1. Time complexity: O(n) (init squares, populate squares)
2. Space complexity: O(1)
"""
