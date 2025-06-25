# Given an array of integers nums and an integer threshold,
# we will choose a positive integer divisor,
# divide all the array by it, and sum the division's result.
# Find the smallest divisor such that the result mentioned above is less than or equal to threshold.
#
# Each result of the division is rounded to the nearest integer greater than or equal to that element.
# (For example: 7/3 = 3 and 10/2 = 5).
#
# The test cases are generated so that there will be an answer.

# Example 1:
# Input: nums = [1,2,5,9], threshold = 6
# Output: 5
# Explanation: We can get a sum to 17 (1+2+5+9) if the divisor is 1.
# If the divisor is 4 we can get a sum of 7 (1+1+2+3) and if the divisor is 5 the sum will be 5 (1+1+1+2).

# Example 2:
# Input: nums = [44,22,33,11,1], threshold = 5
# Output: 44

# Constraints:
# 1 <= nums.length <= 5 * 10^4
# 1 <= nums[i] <= 10^6
# nums.length <= threshold <= 10^6


# ===== Analyze =====
# - The result of each division is rounded up.
#   A divisor is valid if total_result <= threshold
# - Since the problem is asking for the smallest divisor,
#   every time we find a valid divisor, try a smaller value.
#   Otherwise try a larger one.
# - We can binary search for the answer.
#
# - Search space:
# + lower bound is 1, since divisor is a positive integer (problem constraint)
# + upper bound is the maximum number in nums,
#   since any value from it will produce 1 as the division result,
#   and we are interested in the smallest value.

import math


def smallest_divisor(nums: list[int], threshold: int) -> int:
    def _check(divisor: int) -> bool:
        total = 0
        for num in nums:
            total += math.ceil(num / divisor)
        return total <= threshold

    left = 1
    right = max(nums)

    while left <= right:
        mid = (left + right) // 2
        if _check(mid):
            right = mid - 1
        else:
            left = mid + 1

    return left


# ===== Complexity =====
# Let n = nums.length; k = max(nums)
#
# 1. Time complexity
# - find max of nums: O(n)
# - the check runs in O(n)
# - binary search runs in O(log(k))
# => Overall: O(n*log(k))
#
# 2. Space complexity: O(1)
