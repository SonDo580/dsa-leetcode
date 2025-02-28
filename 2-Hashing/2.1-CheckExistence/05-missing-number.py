# Given an array nums containing n distinct numbers in the range [0, n],
# return the only number in the range that is missing from the array.

# Example 1:
# Input: nums = [3,0,1]
# Output: 2
# Explanation: n = 3 since there are 3 numbers,
# so all numbers are in the range [0,3].
# 2 is the missing number in the range since it does not appear in nums.

# Example 2:
# Input: nums = [0,1]
# Output: 2
# Explanation: n = 2 since there are 2 numbers,
# so all numbers are in the range [0,2].
# 2 is the missing number in the range since it does not appear in nums.

# Example 3:
# Input: nums = [9,6,4,2,3,5,7,0,1]
# Output: 8
# Explanation: n = 9 since there are 9 numbers,
# so all numbers are in the range [0,9].
# 8 is the missing number in the range since it does not appear in nums.

# Constraints:
# n == nums.length
# 1 <= n <= 10^4
# 0 <= nums[i] <= n
# All the numbers of nums are unique.

# Follow up:
# Could you implement a solution using only
# O(1) extra space complexity and O(n) runtime complexity?

def missing_number(nums: list[int]) -> int:
    n = len(nums)
    num_set = set(nums)

    for i in range(n + 1):
        if i not in num_set:
            return i


# Time complexity: O(n)
# Space complexity: O(n)


# ====================


# Improve space complexity
# => Solution: check sum difference
# - sum without missing number:
#   0 + 1 + 2 + ... + n = n * (n + 1) / 2


def missing_number_v2(nums: list[int]) -> int:
    n = len(nums)
    return (n * (n + 1)) // 2 - sum(nums)


# Space complexity: O(1)
# Time complexity: O(n) (the built-in sum function still loop through nums)
