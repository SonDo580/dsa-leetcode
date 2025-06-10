# Given an integer array nums,
# return the largest integer that only occurs once.
# If no integer occurs once, return -1.

# Example 1:
# Input: nums = [5,7,3,9,4,9,8,3,1]
# Output: 8
# Explanation: The maximum integer in the array is 9 but it is repeated. The number 8 occurs only once, so it is the answer.

# Example 2:
# Input: nums = [9,9,8,8]
# Output: -1
# Explanation: There is no number that occurs only once.

# Constraints:
# 1 <= nums.length <= 2000
# 0 <= nums[i] <= 1000


def largest_unique_num(nums: list[int]) -> int:
    frequency_dict: dict[int, int] = {}
    for num in nums:
        if num not in frequency_dict:
            frequency_dict[num] = 0
        frequency_dict[num] += 1

    max_num = float("-inf")
    for num, frequency in frequency_dict.items():
        if frequency == 1 and num > max_num:
            max_num = num

    return max_num if max_num > float("-inf") else -1


# ===== Complexity =====
# 1. Time complexity:
# - build frequency_dict: O(n)
# - find max_num with frequency 1: O(n)
# => Overall: O(n)
#
# 2. Space complexity:
# - frequency_dict: O(n)
