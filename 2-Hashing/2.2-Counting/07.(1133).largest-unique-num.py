"""
https://leetcode.com/problems/largest-unique-number/

Given an integer array 'nums',
return the largest integer that only occurs once.
If no integer occurs once, return -1.
"""

"""
Idea:
- Use a dict, collect frequency of each number in 'nums'.
- Iterate through dict entries to max number with frequency 1.
"""


def largest_unique_num(nums: list[int]) -> int:
    cnt: dict[int, int] = {}
    for num in nums:
        if num not in cnt:
            cnt[num] = 0
        cnt[num] += 1

    max_num = float("-inf")
    for num, frequency in cnt.items():
        if frequency == 1 and num > max_num:
            max_num = num

    return max_num if max_num > float("-inf") else -1


"""
Complexity:
- Let n = len(nums)

1. Time complexity: O(n)
- build 'cnt': O(n)
- find max number with frequency 1: O(n)

2. Space complexity: O(n) for 'cnt' 
"""
