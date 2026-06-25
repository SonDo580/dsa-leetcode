"""
https://leetcode.com/problems/counting-elements/

Given an integer array 'arr', count how many elements x there are,
such that x + 1 is also in arr.
If there are duplicates in arr, count them separately.
"""

"""
Idea:
- Add all numbers in 'arr' to a hash set.
- For each number in 'arr', check if x + 1 is also in the set.
- Iterate through 'arr' instead of the hash set
  to count duplicate items separately.
"""


def count_elements(arr: list[int]) -> int:
    num_set = set(arr)
    count = 0

    for num in arr:
        if num + 1 in num_set:
            count += 1

    return count


"""
Complexity:
- Let n = len(arr)

1. Time complexity: O(n)
- build 'num_set': O(n)
- iterate through 'arr': O(n)

2. Space complexity: O(n) for 'num_set'
"""
