# Given a string s, find the length of the longest substring without duplicate characters.

# Example 1:
# Input: s = "abcabcbb"
# Output: 3
# Explanation: The answer is "abc", with the length of 3.

# Example 2:
# Input: s = "bbbbb"
# Output: 1
# Explanation: The answer is "b", with the length of 1.

# Example 3:
# Input: s = "pwwkew"
# Output: 3
# Explanation: The answer is "wke", with the length of 3.
# Notice that the answer must be a substring, "pwke" is a subsequence and not a substring.

# Constraints:
# 0 <= s.length <= 5 * 10^4
# s consists of English letters, digits, symbols and spaces.


# ===== Strategy =====
# - Combine "sliding window" and "hashing".
# - Use a set to store characters in current window.
# - Keep expanding the window to the right if there's no duplicates.
# - When there is duplicate, recalculate max length
#   and shrink the window from the left until valid.


def longest_substring_length(s: str) -> int:
    # If a string is empty or has only 1 character, return its length
    if len(s) < 2:
        return len(s)

    left = 0
    max_length = -1
    char_set = set()

    for right in range(len(s)):
        # If the new character is in char_set, move the left pointer to remove duplicates
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1

        # Add the new character to char_set
        char_set.add(s[right])

        # Update substring max length
        max_length = max(max_length, right - left + 1)

    return max_length


# ===== Complexity =====
# 1. Time complexity: O(n)
# - Move the right pointer: O(n)
# - Move the left pointer: O(n) (worst case)
#   (the nested loop can only run upto n iterations in total)
#
# 2. Space complexity: O(n)
# - char_set can grow to O(n) if there's no duplicates
