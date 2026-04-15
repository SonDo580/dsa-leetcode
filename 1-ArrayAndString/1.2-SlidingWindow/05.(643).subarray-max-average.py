"""
https://leetcode.com/problems/maximum-average-subarray-i/

You are given an integer array 'nums' consisting of n elements,
and an integer k.

Find a contiguous subarray whose length is equal to k
that has the maximum average value and return this value.
Any answer with a calculation error less than 10^-5 will be accepted.
"""

"""
Monotonicity of window constraint (keep size=k):
- extend right: increase size
- shrink left: decrease size

Implementation:
- We can calculate average for each window. 
- OR use sum since the window size is fixed.
  Only calculate max_average = max_sum / k at the end.
"""


def subarray_max_average(nums: list[int], k: int) -> float:
    current_sum = 0
    for i in range(k):
        current_sum += nums[i]

    max_sum = current_sum
    for i in range(k, len(nums)):
        current_sum += nums[i] - nums[i - k]
        max_sum = max(max_sum, current_sum)

    return max_sum / k


"""
Complexity: 
- Let n = len(nums)
1. Time complexity: O(n)
2. Space complexity: O(1)
"""
