"""
https://leetcode.com/problems/first-letter-to-appear-twice/

Given a string s, return the first character to appear twice.
It is guaranteed that the input will have a duplicate character.
"""

"""
- Brute-force would take O(n^2).
  . for each character, iterate through remaining characters 
    to check for duplicate.

Idea:
- Use a hash set to track seen characters.
- Return if encounter a seen character.
"""


def repeated_character(s: str) -> str:
    seen: set[str] = set()
    for c in s:
        if c in seen:
            return c
        seen.add(c)
    raise Exception("unreachable")  # solution guaranteed


"""
Complexity:
- Let n = len(s); m = alphabet size

1. Time complexity: O(n)
2. Space complexity: O(m) for 'seen' set
"""
