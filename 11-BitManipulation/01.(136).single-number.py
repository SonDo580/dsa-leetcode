"""
https://leetcode.com/problems/single-number/

Given a non-empty array of integers 'nums',
every element appears twice except for one.
Find that single one.

You must implement a solution with a linear runtime complexity
and use only constant extra space.
"""

# ===== Attempt 1: Hashmap ====
"""
- Create the frequency dictionary for each number
- Find the number with frequency 1
"""


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


"""
Complexity:
- Let n = len(nums)

1. Time complexity: O(n)
2. Space complexity: O(n) -> failed
"""


# ===== Attempt 2: Sorting ====
"""
- Sort the array -> equal numbers are adjacent
- Loop through the sorted array, find the number that appears once
"""


def single_number(nums: list[int]) -> int:
    n = len(nums)
    if n == 1:
        return nums[0]

    nums.sort()
    for i in range(n - 1):
        if nums[i] != nums[i + 1] and (i == 0 or nums[i] != nums[i - 1]):
            return nums[i]
    return nums[n - 1]


"""
1. Time complexity: O(n*log(n) + n) = O(n)
- sort 'nums: O(n*log(n))
- iterate through 'nums': O(n)

2. Space complexity: O(n) for sorting (timsort)
"""


# ==== Solution: Use XOR =====
"""
XOR properties:
- x XOR x = 0
- x XOR 0 = x
- a XOR b = b XOR a
- (a XOR b) XOR c = a XOR (b XOR c)

=> Implementation:
- Init a zero mask then XOR it will all numbers.
- The numbers that appear twice will cancel itself: (0 XOR x) XOR x = 0
- The final result is the only number that appear once: 0 XOR x = x
- Order doesn't matter (due to commutative and associative property):
  . Imagine reordering the array so equal numbers are adjacent (using commutative property).
    Apply XOR for each group then apply XOR on group results (using associative property).
"""


def single_number(nums: list[int]) -> int:
    mask = 0
    for num in nums:
        mask ^= num
    return mask


"""
1. Time complexity: O(n)
2. Space complexity: O(1)
"""
