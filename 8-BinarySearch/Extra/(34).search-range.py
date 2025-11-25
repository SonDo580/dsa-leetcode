"""
https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array

Given an array of integers 'nums' sorted in non-decreasing order,
find the starting and ending position of a given 'target' value.

If 'target' is not found in the array, return [-1, -1].

You must write an algorithm with O(log n) runtime complexity.

Example 1:
Input: nums = [5,7,7,8,8,10], target = 8
Output: [3,4]

Example 2:
Input: nums = [5,7,7,8,8,10], target = 6
Output: [-1,-1]

Example 3:
Input: nums = [], target = 0
Output: [-1,-1]

Constraints:
0 <= nums.length <= 10^5
-10^9 <= nums[i] <= 10^9
nums is a non-decreasing array.
-10^9 <= target <= 10^9
"""

"""
Algorithm:
- Find the leftmost position to insert 'target' into 'nums' 
  (maintain the sorted order)
  -> use bisect_left 
- Check if 'target' exists in 'nums'.
- Find the rightmost position to insert 'target' into 'nums'
  (maintain the sorted order)
  -> use bisect_right and subtract 1
- Optimization: 
  . when searching for end_index, specify lower bound as start_index.
  . note that this doesn't change time complexity.
"""

import bisect


def search_range(nums: list[int], target: int) -> tuple[int, int]:
    start_index = bisect.bisect_left(nums, target)
    if start_index == len(nums) or nums[start_index] != target:
        return [-1, -1]

    end_index = bisect.bisect_right(nums, target, lo=start_index) - 1
    return [start_index, end_index]


"""
Time complexity: O(log(n)) where n = nums.length

Space complexity: O(1)
"""
