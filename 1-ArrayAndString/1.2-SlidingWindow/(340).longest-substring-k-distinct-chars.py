"""
https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/

Given a string s and an integer k,
return the length of the longest substring of s
that contains at most k distinct characters.
"""

"""
Idea: use sliding window
- Window constraint: num_unique_chars <= k
- Track character frequencies in current window by a dictionary cnt
- Slide window:
  . extend right: cnt[c]++
  . shrink left: cnt[c]--
- Number of unique characters is number of nonzero keys.
  To track that quickly (without looping through all keys):  
  . method 1: evict entry when frequency becomes 0 -> check len(cnt).
  . method 2: use separate integer counter, update when slide.
"""

from collections import defaultdict


# Method 1: evict entry when frequency becomes 0
def length_of_longest_substr_k_distinct(s: str, k: int) -> int:
    cnt = defaultdict(int)
    ans = -1

    left = 0
    for right, c in enumerate(s):
        cnt[c] += 1
        while len(cnt) > k:
            cnt[s[left]] -= 1
            if cnt[s[left]] == 0:
                del cnt[s[left]]
            left += 1
        ans = max(right - left + 1, ans)

    return ans


# Method 2: separate counter for number of unique characters in window
def length_of_longest_substr_k_distinct(s: str, k: int) -> int:
    cnt = defaultdict(int)
    ans = -1
    num_unique_chars = 0

    left = 0
    for right, c in enumerate(s):
        if (c not in cnt) or (cnt[c] == 0):
            num_unique_chars += 1
        cnt[c] += 1

        while num_unique_chars > k:
            cnt[s[left]] -= 1
            if cnt[s[left]] == 0:
                num_unique_chars -= 1
            left += 1

        ans = max(right - left + 1, ans)

    return ans


"""Complexity:
- Let n = len(s)
1. Time complexity: O(n)
2. Space complexity: O(n) for 'cnt'
"""
