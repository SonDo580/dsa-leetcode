"""
https://leetcode.com/problems/is-subsequence/

Given two strings s and t, return true if s is a subsequence of t,
or false otherwise.

A subsequence of a string is a sequence of characters
that can be obtained by deleting some (or none)
of the characters from the original string, while maintaining
the relative order of the remaining characters

For example, "ace" is a subsequence of "abcde" while "aec" is not.
"""


def is_subsequence(s: str, t: str) -> bool:
    i = 0
    j = 0

    while i < len(s) and j < len(t):
        if s[i] == t[j]:
            i += 1
        j += 1

    return i == len(s)


"""
Complexity:
- Let m = len(s), n = len(t)

1. Time complexity: O(m + n)
2. Space complexity: O(1)
"""


# === Follow up ===
"""
Suppose there are lots of incoming s, say s1, s2, ..., sk where k >= 10^9, 
and you want to check one by one to see if t has its subsequence.
In this scenario, how would you change your code?
"""


# === Handle follow-up - Approach 1: Next-character table ===
"""
- Let next_pos[j][char] be j' where t[j'] is next occurrence of 'char'
  if we're currently at t[j] (j' > j).
- Check if s is a subsequence of t:
  . Iterate through s. Initial j = -1 (before start of t)
  . If s[i] is not in next_pos[j] -> return False
    Otherwise: increment i and update j = next_pos[j][s[i]]
  . i == len(s) -> return True
- Build next_pos:
  . "inherit": next_pos[j][ch] = next_pos[j+1][ch]
    overwrite: next_pos[j][t[j+1]] = j+1
  . next_pos[n-1] = {}  (no characters after t[n-1])
    next_pos[-1] <-> before start of t
  -> Iterate through t in reverse order to build
"""


class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        m = len(s)
        n = len(t)
        if m == 0:
            return True
        if m > n:
            return False

        next_pos: dict[int, dict[str, int]] = {}
        next_pos[n - 1] = {}
        for j in range(n - 2, -2, -1):  # fill next_pos[n-2..-1]
            next_pos[j] = {}
            for ch, idx in next_pos[j + 1].items():
                next_pos[j][ch] = idx
            next_pos[j][t[j + 1]] = j + 1

        j = -1
        for ch in s:
            if ch not in next_pos[j]:
                return False
            j = next_pos[j][ch]

        return True


"""
Complexity: 
- Let A = alphabet size

1. Time complexity (k strings): O(m*A + k*n)
- Build next_pos (once): O(m*A)
- Check if s is subsequence of t: O(n)
  . In normal case, we can quickly tell s[i] is not a subsequence 
    if next character is not in next_pos[j]
  -> Check k strings: O(k*n)

2. Space complexity: O(m*A) for next_pos
"""


# === Handle follow-up - Approach 2: Binary search ===
"""
- Find indices that each character appear in t.
  . Use a dict to store sorted list of indices for each character.
- For each character in s:
  . If s[i] is not in char_indices dict
    -> s[i] is not in t -> return False  
  . Otherwise, find the 1st index > previously matched index in t
    in char_indices[s[i]]. Since the list is sorted, use binary search.
- Initialize previously matched index in t: prev_idx = -1
  (so next index can start from 0)
"""

from collections import defaultdict


def _bisect_right(asc_arr: list[int], num: int) -> int:
    """
    Return smallest index i > num in asc_arr.
    . i == len(asc_arr) <-> num > all items in asc_arr.
    """
    left = 0
    right = len(asc_arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if asc_arr[mid] > num:
            right = mid - 1  # try to find smaller answer that is still valid
        else:
            left = mid + 1  # search upper half for valid answer
    return left


class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        char_indices: defaultdict[str, list[int]] = defaultdict(list)
        for j in range(len(t)):
            char_indices[t[j]].append(j)

        prev_matched_idx = -1  # previously matched index in t
        for ch in s:
            if ch not in char_indices:
                return False

            idx = _bisect_right(char_indices[ch], prev_matched_idx)
            if idx == len(char_indices[ch]): 
                # no indices match 'ch' after prev_matched_idx
                return False

            prev_matched_idx = char_indices[ch][idx]

        return True

"""
Complexity:

1. Time complexity (k strings): O(n + k*m*log(n))
- Build 'char_indices': O(n)
- Iterate through s: m iterations
  . binary search 1 entry of 'char_indices': O(log(n))
    (worst case: t = same characters repeated n times)
  -> For k strings: O(k*m*log(n))

2. Space complexity: O(n) for 'char_indices'
"""