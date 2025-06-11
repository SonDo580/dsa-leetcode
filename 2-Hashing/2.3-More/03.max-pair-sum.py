# You are given a 0-indexed array nums consisting of positive integers.
# You can choose two indices i and j, such that i != j,
# and the sum of digits of the number nums[i] is equal to that of nums[j].

# Return the maximum value of nums[i] + nums[j] that you can obtain over
# all possible indices i and j that satisfy the conditions.
# If no such pair of indices exists, return -1.

# Example 1:
# Input: nums = [18,43,36,13,7]
# Output: 54
# Explanation: The pairs (i, j) that satisfy the conditions are:
# - (0, 2), both numbers have a sum of digits equal to 9, and their sum is 18 + 36 = 54.
# - (1, 4), both numbers have a sum of digits equal to 7, and their sum is 43 + 7 = 50.
# So the maximum sum that we can obtain is 54.

# Example 2:
# Input: nums = [10,12,19,14]
# Output: -1
# Explanation: There are no two numbers that satisfy the conditions, so we return -1.

# Constraints:
# 1 <= nums.length <= 10^5
# 1 <= nums[i] <= 10^9


# ===== Strategy =====
# - Build a dict to group numbers with the same digit sum
# - Iterate over the numbers in groups with at least 2 elements.
#   Find the 2 max elements by sorting

from collections import defaultdict


def _get_digit_sum(num: int) -> int:
    digit_sum = 0
    while num:
        digit_sum += num % 10
        num //= 10
    return digit_sum


def max_pair_sum(nums: list[int]) -> int:
    group_dict: defaultdict[int, list[int]] = defaultdict(list)
    for num in nums:
        digit_sum = _get_digit_sum(num)
        group_dict[digit_sum].append(num)

    max_sum = float("-inf")
    for values in group_dict.values():
        if len(values) < 2:
            continue
        values.sort(reverse=True)
        max_sum = max(max_sum, values[0] + values[1])

    return max_sum


# ===== Complexity =====
# 1. Time complexity
# - Loop through nums to build group_dict: O(n)
# - Loop through number groups, sort the values.
#   This can cost O(n*log(n)) if all numbers has the same digit sum.
# => Overall: O(n*log(n))
#
# 2. Space complexity: O(n) - for group_dict


# ===== Improvement =====
# - Only track the largest number seen for each digit sum
# => - Only need 1 pass through nums
#    - Improve average space complexity


def max_pair_sum(nums: list[int]) -> int:
    group_dict: defaultdict[int, int] = {}
    max_sum = float("-inf")

    for num in nums:
        digit_sum = _get_digit_sum(num)
        if digit_sum in group_dict:
            max_sum = max(max_sum, num + group_dict[digit_sum])
        group_dict[digit_sum] = max(num, group_dict[digit_sum])

    return max_sum

# ===== Complexity =====
# 1. Time complexity: O(n)
# 2. Space complexity: still O(n) (but better on average)


# ===== Note =====
# - get_digit_sum(num) takes O(m) where m is the number of digits in num.
#   But the constraint said that num <= 10^9 (at most 10 digits).
#   So we can treat it as O(1) in this problem.