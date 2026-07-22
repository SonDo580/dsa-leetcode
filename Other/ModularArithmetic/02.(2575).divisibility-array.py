"""
https://leetcode.com/problems/find-the-divisibility-array-of-a-string/

You are given a 0-indexed string 'word' of length n consisting of digits,
and a positive integer m.

The divisibility array 'div' of 'word' is an integer array of length n such that:
. div[i] = 1 if the numeric value of word[0,...,i] is divisible by m, or
. div[i] = 0 otherwise.

Return the divisibility array of word.
"""

# === "Normal" way ===
# (exceed int-str conversion limit)
"""
- Iterate over 'word'.
- At each index i:
  . Convert the prefix string into an integer
  . Check if that integer is divisible by m
"""


class Solution:
    def divisibilityArray(self, word: str, m: int) -> list[int]:
        div: list[int] = []
        for i in range(len(word)):
            num = int(word[: i + 1])
            r = num % m
            div.append(1 if r == 0 else 0)
        return div


"""
Complexity:
- Let n = len(word)

1. Time complexity: O(n^2)
- At each index i:
  . Slice word[:i]: O(i)
  . Convert word[i] to integer: O(i)
-> T = sum(O(i) for i in [0..n-1]) = n*(n-1) / 2 = O(n^2)

2. Space complexity: O(n) (max length of word[:i])
"""


# === Improvement 1: Build number incrementally ===
# (exceed time limit)
"""
- Start with current_num = 0
- Append a digit: current_num = previous_num * 10 + digit
- n = 10^5 (constraint) 
  -> Final number is of 10^(10^5) order (exceed 64-bit integer limit).
  -> Much slower operations.
     (Specifically, Python switches from hardware-based arithmetic 
      to software-based BigInt algorithm)
"""


class Solution:
    def divisibilityArray(self, word: str, m: int) -> list[int]:
        div: list[int] = []
        curr_num: int = 0
        for i in range(len(word)):
            curr_num = curr_num * 10 + int(word[i])
            r = curr_num % m
            div.append(1 if r == 0 else 0)
        return div


# === Improvement 2: Only track remainder, not full number ===
"""
. curr_remainder
  = curr_num % m
  = (previous_num * 10 + digit) % m
  = ((previous_num * 10) % m + digit) % m
  = (((previous_num % m) * 10) % m + digit) % m
  = ((previous_remainder * 10) % m + digit) % m
  = (previous_remainder * 10 + digit) % m
"""


class Solution:
    def divisibilityArray(self, word: str, m: int) -> list[int]:
        div: list[int] = []
        remainder = 0
        for digit in word:
            remainder = (remainder * 10 + int(digit)) % m
            div.append(1 if remainder == 0 else 0)
        return div


"""
Complexity:
- Let n = len(word)

1. Time complexity: O(n) to iterate through 'word'
2. Space complexity: O(1)
"""
