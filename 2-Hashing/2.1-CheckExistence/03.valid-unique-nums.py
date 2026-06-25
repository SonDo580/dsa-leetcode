"""
Given an integer array 'nums',
find all the unique numbers x in 'nums' that satisfy the following:
x + 1 is not in 'nums', and x - 1 is not in 'nums'.
"""

"""
- Brute-force would take O(n^2).
  . for each x, iterate through current result to check if it's unique,
    then iterate through remaining characters to check for x + 1 and x - 1.

Idea:
- Add all numbers in 'nums' to a hash set.
- For each unique x in hash set, check if x + 1 and x - 1 is also in it.
"""


def find_numbers(nums: list[int]) -> list[int]:
    result: list[int] = []
    num_set = set(nums)

    for num in num_set:
        if (num + 1 not in num_set) and (num - 1 not in num_set):
            result.append(num)

    return result


"""
Complexity:
- Let n = len(nums)

1. Time complexity: O(n)
- build num_set: O(n)
- iterate through num_set: O(n)

2. Space complexity: O(n) for 'num_set'
"""
