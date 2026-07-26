"""
https://leetcode.com/problems/reverse-words-in-a-string/

Given an input string s, reverse the order of the words.

A word is defined as a sequence of non-space characters.
The words in s will be separated by at least one space.

Return a string of the words in reverse order concatenated by a single space.

Note that s may contain leading or trailing spaces or multiple spaces between two words.
The returned string should only have a single space separating the words.

Follow-up: If the string data type is mutable in your language,
can you solve it in-place with O(1) extra space?
"""


class Solution:
    def reverseWords(self, s: str) -> str:
        return " ".join(reversed(s.strip().split()))


"""
Complexity:
- Let n = len(s)

1. Time complexity: O(n)
- Strip whitespaces: O(n)
- Split into words: O(n)
- Join words in reverse order: O(n)

2. Space complexity: O(n) 
- trimmed string (by strip()): O(n)
- words array (by split()): O(n)
"""


# === Alternative ===
"""
- Convert to character array with 1 space between words 
  and no extra spaces on both ends.
- Iterate through character array in reverse order
  and reverse characters of each word (use 2 pointers)
- Build result string from characters string.
  -> last word becomes 1st word, and so on.
"""


class Solution:
    def reverseWords(self, s: str) -> str:
        chars: list[str] = []
        for c in s:
            # skip whitespaces at the start and redundant whitespaces between words
            if (len(chars) == 0 or chars[-1] == " ") and c == " ":
                continue
            chars.append(c)

        # pop trailing whitespace if needed
        if chars[-1] == " ":
            chars.pop()

        # iterate in reverse
        i = len(chars) - 1
        while i >= 0:
            start = end = i
            while start >= 0 and chars[start] != " ":
                start -= 1

            i = start - 1  # next non-space character

            # reverse chars[start+1..end] (current word)
            start += 1
            while start < end:
                chars[start], chars[end] = chars[end], chars[start]
                start += 1
                end -= 1

        # build result string
        return "".join(reversed(chars))


"""
Complexity:
- Let n = len(s)

1. Time complexity: O(n)
- Collect characters: O(n)
- Reverse characters of all words: O(n)
- Build result string: O(n)

2. Space complexity: O(n) for 'chars' array
"""
