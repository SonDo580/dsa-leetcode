# Given an integer array nums, find the number of ways to
# split the array into two parts so that the first section
# has a sum greater than or equal to the sum of the second section.
# The second section should have at least one number.

from typing import List


def ways_to_split_array(nums: List[int]) -> int:
    prefix_sum = [nums[0]]
    for i in range(1, len(nums)):
        prefix_sum.append(nums[i] + prefix_sum[-1])

    count_ways = 0
    for i in range(len(nums) - 1):
        left_sum = prefix_sum[i]
        right_sum = prefix_sum[-1] - prefix_sum[i]
        if left_sum > right_sum:
            count_ways += 1

    return count_ways
