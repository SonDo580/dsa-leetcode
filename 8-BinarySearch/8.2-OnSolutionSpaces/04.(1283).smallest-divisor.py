"""
https://leetcode.com/problems/find-the-smallest-divisor-given-a-threshold

Given an array of integers 'nums' and an integer 'threshold',
we will choose a positive integer 'divisor',
divide all the array by it, and sum the division's result.
Find the smallest divisor such that the result mentioned above is less than or equal to 'threshold'.

Each result of the division is rounded to the nearest integer greater than or equal to that element.
(For example: 7/3 = 3 and 10/2 = 5).

The test cases are generated so that there will be an answer.
"""

"""
Analysis:
- The result of each division is rounded up.
  A divisor is valid if total_result <= threshold
- Since the problem is asking for the smallest divisor,
  every time we find a valid divisor, try a smaller value.
  Otherwise try a larger one.
- We can binary search for the answer.

- Search space:
+ lower bound is 1, since divisor is a positive integer (problem constraint)
+ upper bound is the maximum number in nums,
  since any value greater than it will produce 1 as the division result,
  and we are interested in the smallest value.
"""

import math


def smallest_divisor(nums: list[int], threshold: int) -> int:
    def _is_valid(divisor: int) -> bool:
        """Check if sum of division results does not exceed threshold."""
        total = 0
        for num in nums:
            total += math.ceil(num / divisor)
        return total <= threshold

    left = 1
    right = max(nums)

    while left <= right:
        mid = (left + right) // 2
        if _is_valid(mid):
            right = mid - 1  # search left portion for smaller divisor
        else:
            left = mid + 1  # search right portion for valid divisor

    return left


"""
Complexity:
Let n = nums.length; k = max(nums)

1. Time complexity:
- find max of nums: O(n)
- check valid divisor: O(n)
- binary search for smallest divisor: O(log(k))
=> Overall: O(n * log(k))

2. Space complexity: O(1)
"""
