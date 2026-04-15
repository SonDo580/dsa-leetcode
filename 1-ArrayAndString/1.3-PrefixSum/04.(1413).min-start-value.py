"""
https://leetcode.com/problems/minimum-value-to-get-positive-step-by-step-sum/

Given an array of integers 'nums',
you start with an initial positive value 'startValue'.
In each iteration, you calculate the step by step sum of 'startValue'
plus elements in nums (from left to right).
Return the minimum positive value of 'startValue' such that
the step by step sum is never less than 1.
"""

"""
Reframe questions:
- Find the min positive 'startValue' such that
  startValue + prefix_sum[i] >= 1

=> Strategy:
- Find the minimum value in the prefix sum array (min_prefix_sum).
  . We don't need to build the full array, just track minimum value.
- Find min_start_value:
  . min_prefix_sum + min_start_value >= 1
  . min_start_value >= 1 (min positive integer)

Note: 
- 'nums' can contain negative numbers
  -> prefix_sum is not monotonically increasing
"""


def min_start_value(nums: list[int]) -> int:
    current_prefix_sum = nums[0]
    min_prefix_sum = current_prefix_sum

    for i in range(1, len(nums)):
        current_prefix_sum += nums[i]
        if current_prefix_sum < min_prefix_sum:
            min_prefix_sum = current_prefix_sum

    return max(1 - min_prefix_sum, 1)


"""
Complexity:
1. Time complexity: O(n) 
2. Space complexity: O(1)
"""
