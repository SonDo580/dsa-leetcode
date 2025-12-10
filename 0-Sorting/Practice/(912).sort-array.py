"""
https://leetcode.com/problems/sort-an-array/

Given an array of integers 'nums', sort the array in ascending order and return it.

You must solve the problem without using any built-in functions
in O(n*log(n)) time complexity and with the smallest space complexity possible.
"""

"""
Idea:
- Use radix sort.
- Handle negative numbers:
  + negate the values and use radix sort.
  + reverse order and negate back when merging with non-negative numbers.
"""

import math


def sort_array(nums: list[int]) -> list[int]:
    # Split
    negated_negative_nums: list[int] = []
    non_negative_nums: list[int] = []
    for num in nums:
        if num < 0:
            negated_negative_nums.append(-num)  # negate value
        else:
            non_negative_nums.append(num)

    # Sort
    _radix_sort(negated_negative_nums)
    _radix_sort(non_negative_nums)

    # Combine
    i = 0
    for num in reversed(negated_negative_nums):
        nums[i] = -num  # restore sign
        i += 1
    for num in non_negative_nums:
        nums[i] = num
        i += 1

    return nums


def _radix_sort(nums: list[int]) -> None:
    if not nums:
        return nums

    # Find the maximum number of digits in a number
    max_digits = _count_digits(max(nums))

    # Sort by each digit (least significant to most significant)
    for k in range(max_digits):
        _counting_sort_by_digit(nums, k)


def _counting_sort_by_digit(nums: list[int], k: int) -> None:
    # Count frequency of each digit
    count = [0] * 10
    for num in nums:
        d = _get_kth_digit(num, k)
        count[d] += 1

    # Compute cumulative count
    for i in range(1, 10):
        count[i] += count[i - 1]

    # Build sorted nums
    # (iterate in reverse order to keep it stable)
    sorted_nums = [0] * len(nums)
    for num in reversed(nums):
        d = _get_kth_digit(num, k)
        sorted_nums[count[d] - 1] = num
        count[d] -= 1

    # Copy sorted nums back to nums
    nums[:] = sorted_nums


def _count_digits(num: int) -> int:
    if num == 0:
        return 1
    return int(math.log10(num)) + 1


def _get_kth_digit(num: int, k: int) -> int:
    return num // (10**k) % 10


"""
Complexity:
- Let n = len(nums)
      d = maximum number of digits in a number
      b = base of the number system (10 in this case)

1. Time complexity: O(n)
- split negative and non-negative numbers: O(n)
- radix sort: O(d * (n + b)) ~ O(n)
- combine sorted arrays: O(n)

2. Space Complexity: O(n)
- negative and non-negative arrays: O(n)
- radix sort: O(n + b) ~ O(n)
"""
