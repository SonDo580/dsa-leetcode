"""
https://leetcode.com/problems/missing-number/

Given an array 'nums' containing n distinct numbers in the range [0, n],
return the only number in the range that is missing from the array.

Follow up:
Could you implement a solution using only
O(1) extra space complexity and O(n) runtime complexity?
"""


# === 1) use set ===
# - add all numbers in 'nums' to a set.
# - iterate through [0, n] and check which one is not included in the set.
def missing_number(nums: list[int]) -> int:
    n = len(nums)
    num_set = set(nums)
    for i in range(n + 1):
        if i not in num_set:
            return i
    raise Exception("unreachable")  # solution guaranteed


"""
Complexity:
1. Time complexity: O(n)
2. Space complexity: O(n) for 'num_set'
"""


# === 2) sum difference (improve space complexity) ===
# . sum without missing number: 0 + 1 + ... + n = n * (n + 1) / 2
def missing_number(nums: list[int]) -> int:
    n = len(nums)
    return (n * (n + 1)) // 2 - sum(nums)


"""
Complexity:
1. Time complexity: O(n) for sum(nums)
2. Space complexity: O(1)
"""
