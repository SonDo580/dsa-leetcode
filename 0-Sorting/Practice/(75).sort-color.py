"""
https://leetcode.com/problems/sort-colors

Given an array nums with n objects colored red, white, or blue,
sort them in-place so that objects of the same color are adjacent,
with the colors in the order red, white, and blue.

We will use the integers 0, 1, and 2 to represent the color red, white, and blue, respectively.

You must solve this problem without using the library's sort function.

Follow up: Could you come up with a one-pass algorithm using only constant extra space?
"""

"""
Analysis:
- Since the number of possible values is small,
  we can use counting sort.
"""


def sort_colors(nums: list[int]) -> None:
    # Count frequency of each item
    count: list[int] = [0] * 3
    for num in nums:
        count[num] += 1

    # Compute cumulative count
    for i in range(1, 3):
        count[i] += count[i - 1]

    # Build output array
    n = len(nums)
    ans = [0] * n
    for num in reversed(nums):
        ans[count[num] - 1] = num
        count[num] -= 1

    # Copy answer back to original array
    for i in range(n):
        nums[i] = ans[i]


"""
Complexity:
- Let n = len(nums)
      k = max value (2 in this case)

1. Time complexity:
- Init and build 'count': O(k + n) 
- Compute cumulative count: O(k)
- Init and build 'ans': O(n)
- Copy 'ans' back to 'nums': O(n)
=> Overall: O(n + k) ~ O(n)

2. Space complexity:
- 'count': O(k)
- 'ans': O(n)
=> Overall: O(n + k) ~ O(n)
"""


# ========= OPTIMIZATION ==========
# =================================
"""
- We can output exactly count[num] items for each item 'num'
  to the original array.
- This breaks stability but reduces space complexity.
"""


def sort_colors(nums: list[int]) -> None:
    # Count frequency of each item
    count: list[int] = [0] * 3
    for num in nums:
        count[num] += 1

    # Output count[num] items for each num directly
    k = 0
    for num in range(3):
        for _ in range(count[num]):
            nums[k] = num
            k += 1


"""
Complexity:

1. Time complexity:
- Init and build 'count': O(k + n) 
- Output results to 'nums': O(n)
=> Overall: O(n + k) ~ O(n)

2. Space complexity: O(k) ~ O(1) for 'count'
"""
