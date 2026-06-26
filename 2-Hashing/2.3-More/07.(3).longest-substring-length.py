"""
https://leetcode.com/problems/longest-substring-without-repeating-characters/

Given a string s, find the length of the longest substring without duplicate characters.
"""

"""
Idea: use sliding window
- Window constraint: no duplicate characters.
- Use a set to store characters in current window.
- Recalculate max length after each maintenance.
"""


def longest_substring_length(s: str) -> int:
    # string is empty or has only 1 character
    if len(s) < 2:
        return len(s)

    max_length = -1
    char_set: set[str] = set()  # set of characters in window

    left = 0
    for right in range(len(s)):
        # new character is duplicate
        # -> shrink until an instance of it is removed
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1

        # add new character
        char_set.add(s[right])

        # recalculate max window length
        max_length = max(max_length, right - left + 1)

    return max_length


"""
Complexity:
- Let n = len(s)

1. Time complexity: O(n)
- 'right' moves O(n) times
- 'left' can move at most O(n) across iterations

2. Space complexity: O(k) for char_set where k = alphabet_size
"""
