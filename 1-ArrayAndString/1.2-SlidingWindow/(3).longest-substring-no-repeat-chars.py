"""
https://leetcode.com/problems/longest-substring-without-repeating-characters/

Given a string s, find the length of the longest substring without duplicate characters.
"""

"""
Monotonicity of window constraint:
- Extending right (may) add a duplicate character
  Shrink left (may) remove an identical character

To check duplicates quickly:
- Use a set to track characters in current window 
"""


# ===== Approach 1: Use set to check duplicates =====
def length_of_longest_substring(s: str) -> int:
    window_chars = set()
    left = 0
    ans = 0
    for right, c in enumerate(s):
        while c in window_chars:
            window_chars.remove(s[left])
            left += 1
        window_chars.add(c)
        ans = max(ans, right - left + 1)
    return ans


"""
Complexity:
- Let n = len(s)
1. Time complexity: O(n)
2. Space complexity: O(1)
"""


# ===== Approach 2: track last_index to check duplicates =====
"""
- We can track the last index of each character.
  When adding the characters c, check if there's another c in current window
  (last_index[c] >= left).
  If yes, the window is invalid -> move left to last_index[c] + 1.
- Constraint: s consists of English letters, digits, symbols and spaces.
  -> Use an array with size 128 (cover all ASCII characters)
"""


def length_of_longest_substring(s: str) -> int:
    last_index = [-1] * 128
    left = 0
    ans = 0
    for right, c in enumerate(s):
        if last_index[ord(c)] >= left:
            left = last_index[ord(c)] + 1
        last_index[ord(c)] = right
        ans = max(ans, right - left + 1)
    return ans


"""
Complexity:
- Let n = len(s)
1. Time complexity: O(n)
2. Space complexity: O(1)
"""
