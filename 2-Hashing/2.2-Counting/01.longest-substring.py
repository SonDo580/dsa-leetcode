"""
You are given a string s and an integer k.
Find the length of the longest substring
that contains at most k distinct characters.

For example, given s = "eceba" and k = 2, return 3.
The longest substring with at most 2 distinct characters is "ece".
"""

"""
Idea: use sliding window
- use a dictionary to track character frequencies in window.
- window is valid if number of nonzero-frequency entries <= k.
- to check number of nonzero-frequency entries quickly:
  . method 1: delete entry from dict when its frequency becomes 0,
  . method 2: use a separate integer counter.
"""

from collections import defaultdict


# method 1: delete entry when frequency becomes 0
def longest_substring(s: str, k: int) -> int:
    cnt: defaultdict[str, int] = defaultdict(int)
    max_length = 0

    left = 0
    for right, right_char in enumerate(s):
        cnt[right_char] += 1

        while len(cnt) > k:
            left_char = s[left]
            cnt[left_char] -= 1
            if cnt[left_char] == 0:
                del cnt[left_char]
            left += 1

        max_length = max(max_length, right - left + 1)

    return max_length


"""
Complexity:
- Let n = len(s)

1. Time complexity: O(n)

2. Space complexity: O(k) for 'cnt' dict
   (delete entry when size goes beyond k)
"""


# method 2: use a separate integer counter
def longest_substring(s: str, k: int) -> int:
    cnt: defaultdict[str, int] = defaultdict(int)
    max_length = 0
    num_unique_chars = 0

    left = 0
    for right, right_char in enumerate(s):
        if right_char not in cnt:
            num_unique_chars += 1
        cnt[right_char] += 1

        while num_unique_chars > k:
            left_char = s[left]
            cnt[left_char] -= 1
            if cnt[left_char] == 0:
                num_unique_chars -= 1
            left += 1

        max_length = max(max_length, right - left + 1)

    return max_length


"""
Complexity:
1. Time complexity: O(n)
2. Space complexity: O(n) for 'cnt' dict
"""
