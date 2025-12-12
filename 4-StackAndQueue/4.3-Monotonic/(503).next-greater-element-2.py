"""
https://leetcode.com/problems/next-greater-element-ii/

Given a circular integer array 'nums'
(i.e., the next element of nums[nums.length - 1] is nums[0]),
return the next greater number for every element in nums.

The next greater number of a number x is the first greater number to its traversing-order next in the array,
which means you could search circularly to find its next greater number.
If it doesn't exist, return -1 for this number.
"""

"""
1. Simplified problem: 
Find the next greater element for each element in an array,
without circulation.
- Keep pushing elements to a stack.
- Before pushing, keep popping elements that are less than 
  current element off the stack.
  Record answers for those elements. 

2. Main problem: Do it with circulation
- We should only search circularly once.
  -> double the array.
  -> reduced to the simplified problem.
- Only update answer for index < len(nums)
"""


def next_greater_elements(nums: list[int]) -> list[int]:
    n = len(nums)

    # Double the list
    doubled_nums = nums[:] + nums[:]  # shallow copy

    # Init answers
    ans: list[int] = [-1] * n

    # Store indices of 'doubled_nums'
    stack: list[int] = []

    for i, num in enumerate(doubled_nums):
        # Keep popping element < current element
        while stack and doubled_nums[stack[-1]] < num:
            j = stack.pop()

            # Record answer for "real" element
            if j < n:
                ans[j] = num

        stack.append(i)

    return ans


"""
Complexity:
- Let n = len(nums)

1. Time complexity:
- Double the array: O(n)
- Init answer: O(n)
- Iterate through 'doubled_nums': O(n)
  . each element is pushed once and popped at most once.
=> Overall: O(n)

2. Space complexity:
- 'doubled_nums': O(n)
- stack: O(n)
=> Overall: O(n)
"""

# ========== Another approach ==========
# ======================================
# (same idea, same complexity)
"""
- Iterate in reversed order and push elements to a stack.
- Before pushing, keep popping elements <= current.
  Now the top of the stack is the first greater element for current
  (if the stack is not empty).
"""


def next_greater_elements(nums: list[int]) -> list[int]:
    n = len(nums)

    # Double the list
    doubled_nums = nums[:] + nums[:]  # shallow copy

    # Init answers
    ans: list[int] = [-1] * n

    # Store elements of 'doubled_nums'
    stack: list[int] = []

    # Iterate in reversed order
    for i in range(len(doubled_nums) - 1, -1, -1):
        # Keep popping element <= current element
        while stack and stack[-1] <= doubled_nums[i]:
            stack.pop()

        # Record answer for "real" element if the stack is not empty
        if i < n and stack:
            ans[i] = stack[-1]

        stack.append(doubled_nums[i])

    return ans
