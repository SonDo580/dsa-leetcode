"""
https://leetcode.com/problems/unique-number-of-occurrences/

Given an array of integers arr,
return true if the number of occurrences of each value
in the array is unique or false otherwise.
"""

"""
Idea:
- Count frequency of each number.
- Add all frequencies to a set. 
  If a frequency has been added before, return False.
"""

from collections import Counter


class Solution:
    def uniqueOccurrences(self, arr: list[int]) -> bool:
        cnt = Counter(arr)
        seen: set[int] = set()  # seen frequencies
        for freq in cnt.values():
            if freq in seen:
                return False
            seen.add(freq)
        return True


"""
Complexity:
- Let n = len(arr)

1. Time complexity: O(n)
- build 'cnt': O(n)
- iterate through 'cnt': O(n)

2. Space complexity: O(n) for 'cnt' and 'seen'
"""
