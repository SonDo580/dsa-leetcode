# Given an integer array nums and an integer k, 
# there is a sliding window of size k that moves from the very left to the very right. 
# For each window, find the maximum element in the window.

# For example, given nums = [1, 3, -1, -3, 5, 3, 6, 7], k = 3, 
# return [3, 3, 5, 5, 6, 7]. 
# The first window is [|1, 3, -1|, -3, 5, 3, 6, 7] 
# and the last window is [1, 3, -1, -3, 5, |3, 6, 7|]

# ===== Brute-force approach =====
# - Loop through all possible starting indices of the window: n - k + 1
# - For each window, find the maximum value by iterating through its element: k
# - Append the maximum value to result
# => Time complexity: O((n - k + 1) * k)
# 
# The problem is when the maximum value leaves the window, we do not know
# what is the second maximum, so we need to search the whole window again.

# ===== Analysis =====
# - + We need a way to store elements so that if the maximum element is removed,
#     we know the second maximum, and so forth.
#   + When we see a number, we no longer care about numbers in the window smaller than it,
#     because they cannot be the maximum
#   -> we need a monotonically non-increasing data structure
#
# - + Maintain the monotonic property requires removing elements from the right.
#   + The problem requires a sliding window, which add elements to the right and 
#     remove elements from the left.
#   -> use a double-ended queue for efficient O(1) operations
#
# - We need to keep track of the window size
#   -> store the indices instead of the values

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

        # Remove index queue[0] if it is outside of the window
        if i - k == queue[0]:
            queue.popleft()

        # Add answer when the window reaches size k
        # queue[0] is the index of the maximum number
        #
        # (after index k - 1, increasing index will move to a new window
        #  the out-of-range element is already removed)
        if i >= k - 1:
            answers.append(nums[queue[0]])

    return answers

# ===== Complexity =====
# 
# Time complexity: O(n)
# - Loop through nums: O(n)
# - Popping elements to keep the monotonic property: O(n)
#
# Space complexity: O(n)
# - 'answers' array: O(n - k)
# - the queue: O(k)