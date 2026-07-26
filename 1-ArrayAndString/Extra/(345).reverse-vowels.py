"""
https://leetcode.com/problems/reverse-vowels-of-a-string/

Given a string s, reverse only all the vowels in the string and return it.

The vowels are 'a', 'e', 'i', 'o', and 'u',
and they can appear in both lower and upper cases, more than once.
"""

"""
Idea: 2 pointers
- Convert s to character array (for mutation).
- Move inward from both ends.
- Swap items if they are both vowels.
"""


class Solution:
    def reverseVowels(self, s: str) -> str:
        chars = list(s)
        vowels = "aeiou"  # small size -> don't need a set

        left = 0
        right = len(s) - 1
        while left < right:
            while left < right and s[left].lower() not in vowels:
                left += 1
            while left < right and s[right].lower() not in vowels:
                right -= 1

            # swap 2 vowels (swap 1 item with itself if left == right)
            chars[left], chars[right] = chars[right], chars[left]
            left += 1
            right -= 1

        return "".join(chars)

"""
Complexity:
- Let n = len(s)

1. Time complexity: O(n)
2. Space complexity: O(n) for 'chars' array
"""