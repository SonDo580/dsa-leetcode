"""
https://leetcode.com/problems/reverse-bits/

Reverse bits of a given 32 bits signed integer.
"""

"""
Idea:
- Iterate from both ends of bit representation.
  . i = 0, j = 31
- If b[i] == b[j] -> no need to swap
- If b[i] != b[j]
  -> swapping b[i] and b[j] is equivalent to flipping each bit.
"""


class Solution:
    def reverseBits(self, n: int) -> int:
        i = 0  # from LSB
        j = 31  # from MSB

        while i < j:
            bit_i = self._get_bit(n, i)
            bit_j = self._get_bit(n, j)

            if bit_i != bit_j:
                n = self._flip_bit(n, i)
                n = self._flip_bit(n, j)

            i += 1
            j -= 1

        return n

    def _get_bit(self, n: int, i: int) -> int:
        """Get ith bit of n"""
        return (n >> i) & 1

    def _flip_bit(self, n: int, i: int) -> int:
        """Return new n with ith bit flipped"""
        return n ^ (1 << i)


"""
Complexity:
- Let k = number of bits in n

1. Time complexity: O(k)
2. Space complexity: O(1)
"""
