"""
https://leetcode.com/problems/check-if-the-sentence-is-pangram/

A pangram is a sentence where every letter of the English alphabet
appears at least once.

Given a string 'sentence' containing only lowercase English letters,
return true if sentence is a pangram, or false otherwise.
"""

"""
Idea:
- iterate through 'sentence', adding characters to a set.
- if final set size == alphabet size, return true.
"""


def is_pangram(sentence: str) -> bool:
    alphabet_size = 26

    if len(sentence) < alphabet_size:
        return False

    char_set: set[str] = set()
    for char in sentence:
        char_set.add(char)
        if len(char_set) == alphabet_size:
            return True

    return False


"""
Complexity:
- Let n = len(sentence), a = alphabet size

1. Time complexity: O(n)
2. Space complexity: O(a) for 'char_set'
"""