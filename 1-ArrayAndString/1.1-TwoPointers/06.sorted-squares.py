# Given an integer array nums sorted in non-decreasing order,
# return an array of the squares of each number
# sorted in non-decreasing order.

# Example 1:
# Input: nums = [-4,-1,0,3,10]
# Output: [0,1,9,16,100]
# Explanation: After squaring, the array becomes [16,1,0,9,100].
# After sorting, it becomes [0,1,9,16,100].

# Example 2:
# Input: nums = [-7,-3,2,3,11]
# Output: [4,9,9,49,121]

# Constraints:
# 1 <= nums.length <= 10^4
# -10^4 <= nums[i] <= 10^4
# nums is sorted in non-decreasing order.

from typing import List


def sorted_squares(nums: List[int]) -> List[int]:
    n = len(nums)
    squares = [None] * len(nums)

    # pointers to nums
    i = 0
    j = n - 1

    # pointer to squares
    k = n - 1

    while i < j:
        square1 = nums[i]**2
        square2 = nums[j]**2

        if square1 > square2:
            squares[k] = square1
            i += 1
        else:
            squares[k] = square2
            j -= 1
        k -= 1

    if i == j:
        squares[k] = nums[i]**2

    return squares