# Given a non-empty array of integers nums,
# every element appears twice except for one.
# Find that single one.

# You must implement a solution with a linear runtime complexity
# and use only constant extra space.

# Example 1:
# Input: nums = [2,2,1]
# Output: 1

# Example 2:
# Input: nums = [4,1,2,1,2]
# Output: 4

# Example 3:
# Input: nums = [1]
# Output: 1

# Constraints:
# 1 <= nums.length <= 3 * 10^4
# -3 * 10^4 <= nums[i] <= 3 * 10^4
# Each element in the array appears twice except for one element which appears only once.


# ===== Attempt 1: Use hash map ====
# - Create the frequency dictionary for each number
# - Find the number with frequency 1
def single_number(nums: list[int]) -> int:
    if len(nums) == 1:
        return nums[0]

    frequency_dict: dict[int, int] = {}

    for num in nums:
        if num not in frequency_dict:
            frequency_dict[num] = 0
        frequency_dict[num] += 1

    for num in frequency_dict:
        if frequency_dict[num] == 1:
            return num


# Time complexity: O(n)
# Space complexity: O(n) -> failed


# ===== Attempt 2: Use sorting ====
# - Sort the array
# - Loop through the sorted array, find the number that appears once
#   (check adjacent numbers)
def single_number(nums: list[int]) -> int:
    if len(nums) == 1:
        return nums[0]

    nums.sort()
    for i in range(len(nums) - 1):
        if nums[i] != nums[i + 1] and (i == 0 or nums[i] != nums[i - 1]):
            return nums[i]
    return nums[len(nums) - 1]


# Time complexity: O(n*log(n)) -> failed
# Space complexity: can be O(1) if done in-place


# ==== Solution: Use XOR operation with a mask =====
# (*) XOR properties:
# - x XOR x = 0
# - x XOR 0 = x
# - Commutative: a XOR b = b XOR a
# - Associative: (a XOR b) XOR c = a XOR (b XOR c) 
#  
# -> Implementation: 
# - Create a "zero" mask then XOR it will all numbers
# - The numbers that appear twice will cancel itself: (0 XOR x) XOR x = 0
# - The final result is the only number that appear once: 0 XOR x = x
# - Order doesn't matter (associative property)
def single_number(nums: list[int]) -> int:
    if len(nums) == 1:
        return nums[0]

    mask = 0
    for num in nums:
        mask ^= num
    return mask


# Time complexity: O(n)
# Space complexity: O(1)
