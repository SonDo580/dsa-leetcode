"""
https://leetcode.com/problems/find-all-anagrams-in-a-string/

Given two strings s and p, 
return an array of all the start indices of p's anagrams in s.
You may return the answer in any order.

An anagram is a word or phrase formed by
rearranging the letters of a different word or phrase,
using all the original letters exactly once.
"""

"""
Idea: Use sliding window
- Build the character frequency dictionary for p (cnt).
- Slide window:
  . cnt[c]-- when adding c to window (extend right).
  . cnt[c]++ when removing c from window (shrink left).
- Maintain constraint: all(cnt[c] == 0)
  . initially, all cnt[c] > 0
  . extending right: reduce 1 cnt[c].
  . cnt[c] < 0
    -> the window contains exceeding c
    -> shrink left until cnt[c] == 0
  . c not in cnt
    -> results in cnt[c] < 0
    -> also shrink left until cnt[c] == 0
- After that, if right-left+1 == len(p)
  -> [left..right] forms a valid anagram of p
  -> record left.
"""

from collections import defaultdict


def find_anagrams(s: str, p: str) -> list[int]:
    ans: list[int] = []  # start indices of valid windows

    # character frequencies of p
    cnt: defaultdict[str, int] = defaultdict(int)
    for c in p:
        cnt[c] += 1

    left = 0
    for right, c in enumerate(s):
        cnt[c] -= 1
        while cnt[c] < 0:
            cnt[s[left]] += 1
            left += 1

        if right - left + 1 == len(p):
            ans.append(left)

    return ans


"""
Complexity:
- Let n = len(s), m = len(p)

1. Time complexity: O(n + m)
- Build 'cnt': O(m)
- Sliding window: O(n)

2. Space complexity: O(m) for 'cnt'
"""
