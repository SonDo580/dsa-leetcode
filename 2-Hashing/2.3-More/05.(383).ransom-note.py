"""
https://leetcode.com/problems/ransom-note/

Given two strings 'ransomNote' and 'magazine',
return true if 'ransomNote' can be constructed
by using the letters from 'magazine' and false otherwise.
Each letter in 'magazine' can only be used once in 'ransomNote'.
"""

"""
Idea:
- Count the frequency of characters in both strings.
- If the frequency of any character in ransom_note is greater than in magazine,
  we cannot construct ransom_note.

Small improvement:
- build character frequency dict for magazine first.
- while building character frequency dict for ransom_note,
  break early when a frequency is greater than in magazine.
"""

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


"""
Complexity:
- Let n = ransom_note.length; m = magazine.length

1. Time complexity: O(m + n)
- Build magazine frequency dict: O(m)
- Loop through ransom_note: O(n)

2. Space complexity: O(m + n)
- magazine frequency dict: O(m)
- ransom_note frequency dict: O(n)
"""
