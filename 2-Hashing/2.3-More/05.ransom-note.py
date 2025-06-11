# Given two strings ransomNote and magazine,
# return true if ransomNote can be constructed
# by using the letters from magazine and false otherwise.
# Each letter in magazine can only be used once in ransomNote.

# Example 1:
# Input: ransomNote = "a", magazine = "b"
# Output: false

# Example 2:
# Input: ransomNote = "aa", magazine = "ab"
# Output: false

# Example 3:
# Input: ransomNote = "aa", magazine = "aab"
# Output: true

# Constraints:
# 1 <= ransomNote.length, magazine.length <= 10^5
# ransomNote and magazine consist of lowercase English letters.

# ===== Strategy =====
# - Count the frequency of characters in both strings.
# - If the frequency of a character in ransom_note is greater than in magazine,
#   we cannot construct ransom_note
#
# (*) Improvement:
# - build character frequency dict for magazine first
# - build character frequency dict for ransom_note
#   break early when a frequency is greater than in magazine
# => don't need to build the full frequency dict for ransom_note

from collections import defaultdict


def can_construct(ransom_note: str, magazine: str) -> bool:
    magazine_char_freq_dict: defaultdict[str, int] = defaultdict(int)
    for c in magazine:
        magazine_char_freq_dict[c] += 1

    ransom_note_char_freq_dict: defaultdict[str, int] = defaultdict(int)
    for c in ransom_note:
        if c not in magazine:
            return False

        ransom_note_char_freq_dict[c] += 1
        if ransom_note_char_freq_dict[c] > magazine_char_freq_dict[c]:
            return False

    return True


# ===== Complexity =====
# Let n = ransom_note.length; m = magazine.length
#
# 1. Time complexity:
# - Build magazine frequency dict: O(m)
# - Loop through ransom_note: O(n)
# => Overall: O(m + n)
#
# 2. Space complexity:
# - magazine frequency dict: O(m)
# - ransom_note frequency dict: O(n)
# => Overall: O(m + n)
