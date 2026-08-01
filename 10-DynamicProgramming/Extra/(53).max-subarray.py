"""
https://leetcode.com/problems/maximum-subarray/

Given an integer array 'nums', 
find the subarray with the largest sum, and return its sum.
"""

"""
- If all numbers are non-negative, the problem becomes trivial: 
  The subarray with maximum sum is always the entire array.
- But -10^4 <= nums[i] <= 10^4

Idea:
- Let dp[i] be the maximum subarray sum that ends at index i.
- At index i, there are 2 choices:
  . Extend the best subarray ending at nums[i-1].
  . Start a new subarray.
  -> Recurrence relation: dp[i] = max(dp[i-1] + nums[i], nums[i])
- Maximum subarray sum for whole array: `max(dp(i) for i in [0..n-1])`

Optimize space (becomes Kadane's algorithm):
- dp[i] only depends on dp[i-1] -> can optimize space
  . Use 1 variable to track maximum subarray ending at current nums[i].
  . Update maximum subarray sum for whole array at each step.
"""


class Solution:
    def maxSubArray(self, nums: list[int]) -> int:
        curr_max = nums[0]
        global_max = nums[0]

        for i in range(1, len(nums)):
            curr_max = max(curr_max + nums[i], nums[i])
            global_max = max(global_max, curr_max)

        return global_max

"""
Complexity:
1. Time complexity: O(n)
2. Space complexity: O(1)
"""