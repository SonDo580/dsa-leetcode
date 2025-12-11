"""
https://leetcode.com/problems/maximum-score-of-a-good-subarray/

You are given an array of integers 'nums' (0-indexed) and an integer k.
The score of a subarray (i, j) is defined as
. min(nums[i], nums[i+1], ..., nums[j]) * (j - i + 1).
A good subarray is a subarray where i <= k <= j.
Return the maximum possible score of a good subarray.
"""

"""
Problem articulation:
- subarray_score = min_value * size
-> Find the longest window that has nums[i] as the minimum element. 
   Calculate score if 2 bounds satisfy i <= k <= j.
   Repeat for all nums[i] and take the maximum score.
"""

"""
Brute-force approach: 
- Init max score to -infinity
- For each number:
  . Scan left until encountering a smaller number -> record i.
    Scan right until encountering a smaller number -> record j.
  . Check if i <= k <= j. 
    If yes: calculate the subarray score and update max score.
"""

import math


def maximum_score(nums: list[int], k: int) -> int:
    max_score = -math.inf

    for x in range(len(nums)):
        i = j = x

        # Find left bound
        while i >= 0 and nums[i] >= nums[x]:
            i -= 1
        i += 1

        # Find right bound
        while j < len(nums) and nums[j] >= nums[x]:
            j += 1
        j -= 1

        # Check if subarray is good
        if i <= k <= j:
            # Calculate subarray score
            score = nums[x] * (j - i + 1)

            # Update max score
            max_score = max(max_score, score)

    return max_score


"""
Complexity:
- Let n = len(nums)

1. Time complexity:
- scan left (across iterations): 1 + 2 + ... + n - 1 + n
- scan right (across iterations): n + n - 1 + ... + 2 + 1
=> Overall: O(n^2) 

2. Space complexity: O(1)
"""

# ========== IMPROVEMENT ==========
# =================================
"""
- We can record the boundaries of each subarray in advance.

- Find left bound of longest subarray that has min = nums[i]:
  . Keep pushing indices to a stack.
  . Before pushing index i, pop all indices with value >= nums[i].
    If the top of the stack is not empty, left_bound = top_of_stack + 1
    Otherwise, left_bound = 0
  . Note: the stack is monotonically increasing
  
  Let's try the next number nums[i + 1] to verify that 
  we will not "accidentally" pop its left bound off:
  . nums[i + 1] > nums[i] -> left_bound == nums[i] (top of stack)
  . nums[i + 1] == nums[i] -> same left_bound
  . nums[i + 1] < nums[i]
    -> left_bound is in lower part of the non-empty stack (or 0)
  Note that items are popped off the stack when nums[i + 1] <= nums[i]

- Find right bound of longest subarray that has min = nums[i]
  . similar to finding left bound but iterate in reverse.
"""


def maximum_score(nums: list[int], k: int) -> int:
    n = len(nums)
    left_bounds = [0] * n
    right_bounds = [n - 1] * n

    # Find left bound for longest subarray that has min = nums[i]
    stack: list[int] = []  # store indices
    for i in range(n):
        # Pop until encounter value < nums[i]
        while stack and nums[stack[-1]] >= nums[i]:
            stack.pop()

        # Record left bound
        # (default = 0, only update if stack is not empty)
        if stack:
            left_bounds[i] = stack[-1] + 1

        stack.append(i)

    # Find right bound for longest subarray that has min = nums[i]
    stack = []  # reset the stack
    for i in range(n - 1, -1, -1):
        # Pop until encounter value < nums[i]
        while stack and nums[stack[-1]] >= nums[i]:
            stack.pop()

        # Record right bound
        # (default = n - 1, only update if stack is not empty)
        if stack:
            right_bounds[i] = stack[-1] - 1

        stack.append(i)

    # Find max score among good subarrays
    max_score = -math.inf
    for i in range(n):
        left = left_bounds[i]
        right = right_bounds[i]
        if left <= k <= right:
            max_score = max(max_score, nums[i] * (right - left + 1))

    return max_score


"""
Complexity:
- Let n = len(nums)

1. Time complexity:
- Find left/right bounds: O(n)
  . each iteration is amortized O(1) since each item can be popped at most once.
- Find max score: O(n)
=> Overall: O(n) 

2. Space complexity: O(n) for the stack
"""
