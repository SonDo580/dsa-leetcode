# You are given an array of integers nums which is sorted in ascending order,
# and an integer target.
# If target exists in nums, return its index.
# Otherwise, return -1.

from typing import List


def binary_search(nums: List[int], target: int) -> int:
    left = 0
    right = len(nums) - 1

    while left <= right:
        mid = (left + right) // 2
        current = nums[mid]

        if current == target:
            return mid

        if current > target:
            right = mid - 1
        else:
            left = mid + 1

    return -1


# Time complexity: O(log n)
# Space complexity: O(1)
