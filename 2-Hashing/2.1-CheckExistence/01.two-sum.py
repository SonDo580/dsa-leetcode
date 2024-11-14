# Given an array of integers nums and an integer target, 
# return indices of two numbers such that they add up to target. 
# You cannot use the same index twice.

from typing import List

def two_sum(nums: List[int], target: int) -> List[int]:
    complement_dict = {}
    
    for i in range(len(nums)):
        num = nums[i]
        complement = target - num

        if complement in complement_dict:
            return [dict[complement], i]
        
        complement_dict[num] = i
    
    return [-1, -1]

# Time complexity: O(n)
# Space complexity: O(n)