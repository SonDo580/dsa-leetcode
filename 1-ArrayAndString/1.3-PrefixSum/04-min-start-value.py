# Given an array of integers nums, 
# you start with an initial positive value startValue.
# In each iteration, you calculate the step by step sum of startValue 
# plus elements in nums (from left to right).
# Return the minimum positive value of startValue such that 
# the step by step sum is never less than 1.

# # Example 1:
# Input: nums = [-3,2,-3,4,2]
# Output: 5
# Explanation: If you choose startValue = 4, in the third iteration your step by step sum is less than 1.
# step by step sum
# startValue = 4 | startValue = 5 | nums
#   (4 -3 ) = 1  | (5 -3 ) = 2    |  -3
#   (1 +2 ) = 3  | (2 +2 ) = 4    |   2
#   (3 -3 ) = 0  | (4 -3 ) = 1    |  -3
#   (0 +4 ) = 4  | (1 +4 ) = 5    |   4
#   (4 +2 ) = 6  | (5 +2 ) = 7    |   2

# # Example 2:
# Input: nums = [1,2]
# Output: 1
# Explanation: Minimum start value should be positive. 

# Example 3:
# Input: nums = [1,-2,-3]
# Output: 5
 
# Constraints:
# 1 <= nums.length <= 100
# -100 <= nums[i] <= 100

# => Strategy:
# - find the minimum value in the prefix sum array (min_prefix_sum)
# - find min_start_value
#   . min_prefix_sum + min_start_value = 1
#   . min_start_value should be a positive integer
# - no need to build the array, just track the minimum value

from typing import List

def min_start_value(nums: List[int]) -> int:
    current_prefix_sum = nums[0]
    min_prefix_sum = current_prefix_sum

    for i in range(1, len(nums)):
        current_prefix_sum += nums[i]
        if current_prefix_sum < min_prefix_sum:
            min_prefix_sum = current_prefix_sum
    
    return max(1 - min_prefix_sum, 1)

