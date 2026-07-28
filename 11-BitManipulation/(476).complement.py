"""
https://leetcode.com/problems/number-complement/

The complement of an integer is the integer you get
when you flip all the 0's to 1's and all the 1's to 0's in its binary representation.

For example, The integer 5 is "101" in binary and its complement is "010" which is the integer 2.
Given an integer 'num', return its complement.
"""

"""
Idea:
- Try flipping each kth bit, starting from k = 0 (LSB).
  Stop when 2^k (1 << k) exceeds num.
- To flip kth bit of x: x ^ (1 << k).
"""


class Solution:
    def findComplement(self, num: int) -> int:
        k = 0
        complement = num
        while (1 << k) <= num:
            complement ^= 1 << k
            k += 1
        return complement


"""
Complexity:
- Let L = number of bits in num, exclude leading 0's 

1. Time complexity: O(L)
2. Space complexity: O(1)
"""


# === Improvement ===
"""
- To flip all bits (except leading 0's) in x, we want a mask of all 1's
  with length = L = number of bits in num (exclude leading 0's)
- Use Python built-in: L = num.bit_length() (O(1))
  -> mask = 2^L - 1
"""


class Solution:
    def findComplement(self, num: int) -> int:
        L = num.bit_length()
        mask = (1 << L) - 1
        return num ^ mask


"""
Complexity:
1. Time complexity: O(1)
2. Space complexity: O(1)
"""
