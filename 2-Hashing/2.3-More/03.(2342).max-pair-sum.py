"""
https://leetcode.com/problems/max-sum-of-a-pair-with-equal-sum-of-digits/

You are given a 0-indexed array 'nums' consisting of positive integers.
You can choose two indices i and j, such that i != j,
and the sum of digits of the number nums[i] is equal to that of nums[j].

Return the maximum value of nums[i] + nums[j] that you can obtain over
all possible indices i and j that satisfy the conditions.
If no such pair of indices exists, return -1.
"""

"""
Strategy:
- Build a dict to group numbers with the same digit sum.
- Iterate over the numbers in groups with at least 2 elements.
  Find the 2 max elements by sorting.
"""

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

    ans = -1  # nums only contains positive integers
    for vals in group_dict.values():
        if len(vals) < 2:
            continue
        vals.sort(reverse=True)
        ans = max(ans, vals[0] + vals[1])

    return ans


"""
Complexity:
- Let n = len(nums)

1. Time complexity:
- build group_dict: O(n)
- loop through each number group and sort the values.
  . can cost O(n*log(n)) if all numbers have the same digit sum.
=> Overall: O(n*log(n))

- get_digit_sum(num) takes O(m) where m is the number of digits in num.
  But the constraint said that num <= 10^9 (at most 10 digits).
  So we can treat it as O(1) in this problem.

2. Space complexity:
- O(n) for group_dict
- O(n) for sorting (timsort)
  (worst case: all numbers have the same digit sum)
=> Overall: O(n)
"""


# === Improvement ===
"""
- Only track the largest number seen for each digit sum
- At each number, we can calculate the max sum of a group (upto that point) right away.
  . if number's digit sum hasn't been seen -> nothing to pair with.
  . otherwise, combine it with the largest number of the group and check.
"""


def max_pair_sum(nums: list[int]) -> int:
    # map digit sum to largest number in group
    group_dict: defaultdict[int, int] = defaultdict(int)

    ans = -1  # nums only contains positive integers
    for num in nums:
        digit_sum = _get_digit_sum(num)
        if digit_sum in group_dict:
            ans = max(ans, num + group_dict[digit_sum])
        group_dict[digit_sum] = max(num, group_dict[digit_sum])

    return ans


"""
Complexity:
1. Time complexity: O(n), but only need 1 pass through 'nums'
2. Space complexity: still O(n), but better on average
"""
