"""
https://leetcode.com/problems/two-sum/

Given an array of integers 'nums' and an integer 'target',
return indices of two numbers such that they add up to 'target'.

You may assume that each input would have exactly one solution,
and you may not use the same element twice.

You can return the answer in any order.
"""

"""
- Brute-force would take O(n^2).
  . for each number, iterate through remaining numbers to find complement.

Idea:
- Use a hash map to store indices of seen numbers.
- For each number, check if its complement has been seen.
"""


def two_sum(nums: list[int], target: int) -> list[int]:
    seen: dict[int, int] = {}  # map seen numbers to their indices

    for i in range(len(nums)):
        num = nums[i]
        complement = target - num

        if complement in seen:
            return [seen[complement], i]
            # return [i, seen[complement]] # also work

        seen[num] = i

    raise Exception("unreachable")  # solution guaranteed


"""
Complexity:
- Let n = len(nums)

1. Time complexity: O(n)
2. Space complexity: O(n) for 'seen' dict
"""
