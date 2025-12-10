"""
https://leetcode.com/problems/longest-continuous-subarray-with-absolute-diff-less-than-or-equal-to-limit/

Given an array of integers 'nums' and an integer 'limit',
return the size of the longest subarray such that the absolute difference
between any two elements of this subarray is less than or equal to 'limit'.
"""

"""
Analysis:
- We need to track subarray with a constraint.
  -> use sliding window.
- When the subarray becomes invalid, keep shrinking from the left.
  If the removed item is a maximum / minimum, we need to find the maximum / minimum again.
  -> use 2 monotonic double-ended queues to track the maximum / minimum item in the window.
- We want the longest subarray possible.
  -> the queues are non-increasing and non-decreasing 
     (not strict, allow equal items).
"""


from collections import deque


def longest_subarray(nums: list[int], limit: int) -> int:
    # increasing_queue[0] is the minimum item of the current window
    increasing_queue: deque[int] = deque()

    # decreasing_queue[0] is the maximum item of the current window
    decreasing_queue: deque[int] = deque()

    max_subarray_length = 0

    # left and right define a window
    left = 0

    for right in range(len(nums)):
        # Maintain the monotonic queues
        while len(increasing_queue) > 0 and increasing_queue[-1] > nums[right]:
            increasing_queue.pop()
        while len(decreasing_queue) > 0 and decreasing_queue[-1] < nums[right]:
            decreasing_queue.pop()

        increasing_queue.append(nums[right])
        decreasing_queue.append(nums[right])

        # Maintain the window constraint: max - min <= limit
        while decreasing_queue[0] - increasing_queue[0] > limit:
            # - Shrink the window (advance the left pointer)
            # - If the removed item is a maximum or minimum,
            #   also remove it from the corresponding queue
            if nums[left] == decreasing_queue[0]:
                decreasing_queue.popleft()
            if nums[left] == increasing_queue[0]:
                increasing_queue.popleft()
            left += 1

        # Recalculate maximum subarray length
        max_subarray_length = max(max_subarray_length, right - left + 1)

    return max_subarray_length


"""
Complexity:

1. Time complexity: O(n)
- each 'for' loop iteration is amortized O(1)

2. Space complexity: O(n) for 2 queues
"""