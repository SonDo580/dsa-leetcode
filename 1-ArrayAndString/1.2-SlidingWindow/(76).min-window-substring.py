"""
https://leetcode.com/problems/minimum-window-substring/

Given two strings s and t of lengths m and n respectively,
return the minimum window substring of s such that
every character in t (including duplicates) is included in the window.
If there is no such substring, return the empty string "".

The testcases will be generated such that the answer is unique.

Follow up: Could you find an algorithm that runs in O(m + n) time?
"""

"""
Idea: 
- A bit similar to `(438).all-anagrams`.
  The difference: 
  . Accept c that is not in t.
  . Accept exceeding c from t.
- We can use sliding window on s
  . Substring constraint: 
    contains every characters in t including duplicates
    <-> each character has at least the same frequency as in t

Implementation:
- Build character frequency dictionary from t (cnt)
- Maintain window constraint (when expanding right):
  . if c in t -> cnt[c]--
  . if c not in t -> allow but don't update 'cnt'
- After expanding right:
  . If all cnt[c] <= 0 (allow exceeding), the current window is valid.
    . Keep shrinking left while the window is still valid
    to get the shortest possible substring
    (don't update 'cnt' if removed c is not in t).
    . Update min window's bounds (only slice string at the end).

=========================
Faster valid window check:
- Let:
  . t_uniq = number of unique characters in t
           = len(cnt) right after build
  . done = number of t's characters whose all instances 
           have been included in current window
         = 0 initially
- Current window is valid when done == t_uniq
- When a cnt[c] transition from positive to 0: 
  -> all instances of c have been included
  -> increase 'done'
- cnt[c] cannot transition from 0 back to positive,
  since we don't shrink left if it makes the window invalid.
"""

from collections import Counter
import math


# ===== Slow valid window check =====
def min_window(s: str, t: str) -> str:
    cnt = Counter(t)
    min_window_size = math.inf
    min_window_left, min_window_right = -1, -1  # boundary

    left = 0
    for right, c in enumerate(s):
        if c not in cnt:
            continue  # allow, doesn't affect validity

        cnt[c] -= 1

        # all frequencies have been reduced to <= 0
        # -> window is valid (contains all characters in t)
        if all(v <= 0 for v in cnt.values()):
            # shrink left while the window is still valid
            while left <= right:
                if s[left] not in cnt:
                    left += 1
                    continue  # doesn't affect validity

                if cnt[s[left]] + 1 > 0:
                    break  # removing s[left] makes window invalid
                cnt[s[left]] += 1
                left += 1

            if right - left + 1 < min_window_size:
                min_window_left, min_window_right = left, right
                min_window_size = right - left + 1

    if min_window_size == math.inf:
        return ""
    return s[min_window_left : min_window_right + 1]


"""
Complexity:
- Let n = len(s), m = len(t) 

1. Time complexity: O(n * m)
- Build 'cnt': O(m)
- Sliding window: O(n * m) (check all entries of 'cnt' in every iteration)
- String slicing (produce result): O(n)

2. Space complexity: O(m) for 'cnt'
"""


# ===== Fast valid window check =====
def min_window(s: str, t: str) -> str:
    cnt = Counter(t)
    min_window_size = math.inf
    min_window_left, min_window_right = -1, -1  # boundary

    t_uniq = len(cnt)
    done = 0

    left = 0
    for right, c in enumerate(s):
        if c not in cnt:
            continue  # allow, doesn't affect validity

        cnt[c] -= 1
        if cnt[c] == 0:
            done += 1

        # all instances of each character in t have been included
        # -> window is valid
        if done == t_uniq:
            # shrink left while the window is still valid
            while left <= right:
                if s[left] not in cnt:
                    left += 1
                    continue  # doesn't affect validity

                if cnt[s[left]] + 1 > 0:
                    break  # removing s[left] makes window invalid
                cnt[s[left]] += 1
                left += 1

            if right - left + 1 < min_window_size:
                min_window_left, min_window_right = left, right
                min_window_size = right - left + 1

    if min_window_size == math.inf:
        return ""
    return s[min_window_left : min_window_right + 1]


"""
Complexity:
- Let n = len(s), m = len(t) 

1. Time complexity: O(n + m)
- Build 'cnt': O(m)
- Sliding window: O(n)
- String slicing (produce result): O(n)

2. Space complexity: O(m) for 'cnt'
"""
