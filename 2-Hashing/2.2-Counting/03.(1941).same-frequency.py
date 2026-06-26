"""
https://leetcode.com/problems/check-if-all-characters-have-equal-number-of-occurrences/

Given a string s, determine if all characters have the same frequency.

For example, given s = "abacbc", return true. All characters appear twice.
Given s = "aaabb", return false. "a" appears 3 times, "b" appears 2 times. 3 != 2.
"""

from collections import defaultdict


def same_frequency(s: str) -> bool:
    cnt: defaultdict[str, int] = defaultdict(int)
    for c in s:
        cnt[c] += 1
    return len(set(cnt.values())) == 1

"""
Complexity:

1. Time complexity: O(n)
- build character frequency dict: O(n)
- convert dict values to a set: O(n)

2. Space complexity: O(k) for 'cnt' dict, where k = alphabet size
"""
