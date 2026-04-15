"""
https://leetcode.com/problems/running-sum-of-1d-array/

Given an array 'nums'.
We define a running sum of an array as
runningSum[i] = sum(nums[0]…nums[i]).
Return the running sum of 'nums'.
"""


def running_sum(nums: list[int]) -> list[int]:
    result = [nums[0]]
    for i in range(1, len(nums)):
        result.append(result[-1] + nums[i])
    return result


"""
Complexity:
1. Time complexity: O(n) 
2. Space complexity: O(1)
"""
