"""
https://leetcode.com/problems/search-insert-position

Given a sorted array of distinct integers and a target value,
return the index if the target is found.
If not, return the index where it would be if it were inserted in order.
You must write an algorithm with O(log n) runtime complexity.

Constraints:
. nums contains distinct values sorted in ascending order.
. ...
"""


def search_insert(nums: list[int], target: int) -> int:
    left = 0
    right = len(nums) - 1

    while left <= right:
        mid = (left + right) // 2
        current = nums[mid]

        if current == target:
            return mid
        elif current > target:
            right = mid - 1  # search the left portion
        else:
            left = mid + 1  # search the right portion

    return left  # 1st index i where arr[i] > target


"""
Time complexity: O(log(n)) where n = nums.length
Space complexity: O(1)
"""
