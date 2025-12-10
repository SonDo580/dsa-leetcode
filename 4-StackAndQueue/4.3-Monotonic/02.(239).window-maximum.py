"""
https://leetcode.com/problems/sliding-window-maximum/

Given an integer array 'nums' and an integer k,
there is a sliding window of size k that moves from the very left to the very right.
For each window, find the maximum element in the window.

For example, given nums = [1, 3, -1, -3, 5, 3, 6, 7], k = 3,
return [3, 3, 5, 5, 6, 7].
The first window is [|1, 3, -1|, -3, 5, 3, 6, 7]
and the last window is [1, 3, -1, -3, 5, |3, 6, 7|]
"""

"""
Brute-force approach:
- Loop through all possible starting indices of the window: n - k + 1 windows
- For each window, find the maximum value by iterating through its element: k elements
=> Time complexity: O((n - k) * k)

Analysis:
- The problem is when the maximum value leaves the window, we do not know
what is the second maximum, so we need to search the whole window again.
- We need a way to store elements so that if the maximum element is removed,
  we know the second maximum, and so forth.
  When we see a number, we no longer care about numbers in the window 
  that are smaller than it, because they cannot be the maximum.

=> Improvement:
- Use a monotonically non-increasing double-ended queue.
- Before appending:
  . pop all numbers that are smaller than current number.
- Slide the window: 
  . append current number.
  . remove queue[0] if it is outside the window.
- We need to keep track of the window size
  -> store indices instead of values.
- The front of the queue always hold the index of the maximum number
  in the current window.
"""

from collections import deque


def window_maximum(nums: list[int], k: int) -> list[int]:
    # Store the maximum number in each window
    answers: list[int] = []

    # Store the indices to track the window size
    # The associated values must be in non-increasing order
    queue: deque[int] = deque()

    for i in range(len(nums)):
        # Get rid of the indices with values smaller than the current one
        # because they cannot be the maximum
        while len(queue) > 0 and nums[i] > nums[queue[-1]]:
            queue.pop()

        queue.append(i)

        # Remove queue[0] if it is outside of the window
        if i - k == queue[0]:
            queue.popleft()

        # Add answer when the window reaches size k
        # (Skip this step while building the first window)
        if i >= k - 1:
            # queue[0] is the index of the maximum number
            answers.append(nums[queue[0]])

    return answers


"""
Complexity:
- Let n = len(nums)

1. Time complexity: O(n)
. although there's a nested 'while' loop, each item can only be removed at most once.

2. Space complexity: O(k) for the queue
"""
