"""
https://leetcode.com/problems/minimum-size-subarray-sum/

Given an array of positive integers 'nums' and a positive integer 'target',
return the minimal length of a subarray whose sum >= target.
If there is no such subarray, return 0 instead.
"""

"""
Idea:
- Use sliding window with constraint sum < target
- Monotonicity:
  . extending right increases sum, shrinking left decreases sum
    (since 'nums' only contains positive numbers)
- If extending right makes sum >= target,
  keep shrinking left until sum < target.
  The min-size window that ends at 'right' is:
  . right - (left - 1) + 1
"""

import math


def min_subarray_len(target: int, nums: list[int]) -> int:
    ans = math.inf
    left = 0
    curr_sum = 0
    for right in range(len(nums)):
        curr_sum += nums[right]
        has_invalid_window = curr_sum >= target
        while curr_sum >= target:
            curr_sum -= nums[left]
            left += 1
        if has_invalid_window:
            ans = min(ans, right - (left - 1) + 1)
    return 0 if ans == math.inf else ans


"""
Complexity:
- Let n = len(nums)

1. Time complexity: O(n)
- 'right' moves n times
- 'left' moves at most n times 

2. Space complexity: O(1)
"""
