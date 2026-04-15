"""
Given an array of positive integers' nums' and an integer k,
find the length of the longest subarray whose sum <= k.
"""

"""
Identify 'sliding window' problem:
- For a given sub-array, extending right increases the sum,
  shrinking left decreases the sum.
- We can recalculate the sum quickly when items are added and removed.
"""


def longest_subarray(nums: list[int], k: int) -> int:
    left = 0
    current_sum = 0
    max_length = 0

    for right in range(len(nums)):
        # add new element to the right
        current_sum += nums[right]

        # remove elements from the left until window is valid
        while current_sum > k:
            current_sum -= nums[left]
            left += 1

        # update max_length if needed
        max_length = max(max_length, right - left + 1)

    return max_length


"""
Complexity:

1. Time complexity: O(n)
- 'right' moves n times.
- 'left' moves at most n times.

2. Space complexity: O(1)
"""
