"""
https://leetcode.com/problems/string-compression/

Given an array of characters 'chars',
compress it using the following algorithm:

Begin with an empty string s. For each group of consecutive repeating characters in chars:
- If the group's length is 1, append the character to s.
- Otherwise, append the character followed by the group's length.

The compressed string s should not be returned separately, but instead,
be stored in the input character array 'chars'.
Note that group lengths that are 10 or longer will be split into multiple characters in 'chars'.

After you are done modifying the input array,
return the new length of the array.
"""

"""
Idea:
- Use 2 pointers:
  . i to iterate through chars.
  . j to fill result.
- Maintain a counter for current group.
  . If next character is the same as previous character,
    increase the counter.
  . Otherwise put the frequency after the current character.
    Then put the next character.
- If frequency has multiple digits:
  . Find number of digits: d = floor(log10(x)) + 1
  . Start filling digits from j + d - 1.
  . Number of digits in frequency x <= x (guaranteed).
    And we only append frequency if x > 1.
    So overwriting will not happen. 
"""

import math


class Solution:
    def compress(self, chars: list[str]) -> int:
        j = 0
        curr_char = None
        freq = 0  # frequency of current character

        for i in range(len(chars)):
            if i == 0 or chars[i] == chars[i - 1]:
                curr_char = chars[i]
                freq += 1
            else:
                j = self._put(chars, j, curr_char, freq)

                # update info for next group
                curr_char = chars[i]
                freq = 1

        # === handle last group ===
        j = self._put(chars, j, curr_char, freq)

        return j

    def _put(self, chars: list[str], j: int, curr_char: str, freq: int) -> int:
        """
        Put 'curr_char' and its frequency 'freq' into result array 'chars'
        starting from j. Return next slot j to put result.
        """
        chars[j] = curr_char
        j += 1

        if freq > 1:
            # put frequency's digits after current character
            # (fill digits from right to left)
            d = math.floor(math.log10(freq)) + 1
            for k in range(j + d - 1, j - 1, -1):
                chars[k] = str(freq % 10)
                freq //= 10
            j += d

        return j


"""
Complexity:
- Let n = len(chars)

1. Time complexity: O(n)
- Iterate through 'chars': O(n)
- Total iterations of 'for' loop to put digits: O(n)

2. Space complexity: O(1)
"""


# === Proof: if d is number of digits in x then d <= x ===
"""
. 10^(d-1) <= x < 10^d 
  -> x >= 10^(d-1)
. d = 1:
  . 10^(d-1) = 10^(1-1) = 1 = d
  -> x >= d
. d >= 2:
  . binominal theorem: (a + b)^n = sum(nCk*a^(n-k)*b^k for k in [0..n])
  . 10^(d-1)
    = (1 + 9)^(d-1) 
    = (d-1)C0 + (d-1)C1*9 + ...
    > 1 + 9*(d-1) 
    = 9*d - 8 
  . 9*d - 8 - d = 8*(d-1) >= 2*(2 - 1) = 2
    -> 9*d - 8 > d  (for d >= 2)
    -> 10^(d-1) > d
    -> x > d
"""
