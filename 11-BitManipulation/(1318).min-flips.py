"""
https://leetcode.com/problems/minimum-flips-to-make-a-or-b-equal-to-c/

Given 3 positives numbers a, b and c.
Return the minimum flips required in some bits of a and b to make (a | b == c).
"""

# === Approach 1: Check all bits ===
"""
- Let L be max bit length of a,b,c 
- For i in range [0..L-1].
  . If get_ith_bit(c) == 1:
    . If get_ith_bit(a) == 1 or get_ith_bit(b) == 1
      -> no flips required.
    . If get_ith_bit(a) == get_ith_bit(b) == 0
      -> flip ith bit in either a or b.
  . If get_ith_bit(c) = 0:
    . If get_ith_bit(a) == get_ith_bit(b) == 0
      -> no flips required.
    . If get_ith_bit(a) == 1 -> flip ith bit of a
      If get_ith_bit(b) == 1 -> flip ith bit of b
"""


def get_bit(x: int, i: int) -> int:
    """Return ith bit of x."""
    return (x >> i) & 1


class Solution:
    def minFlips(self, a: int, b: int, c: int) -> int:
        L = max(a.bit_length(), b.bit_length(), c.bit_length())
        flips = 0

        for i in range(L):
            if get_bit(c, i) == 1:
                # only need ith bit of either a or b to be 1
                if get_bit(a, i) == 0 and get_bit(b, i) == 0:
                    flips += 1
            else:  # get_bit(c, i) == 0
                # need ith bit of both a and b to be 0
                if get_bit(a, i) == 1:
                    flips += 1
                if get_bit(b, i) == 1:
                    flips += 1

        return flips


"""
Complexity:
- Let L = max_bit_length(a,b,c)

1. Time complexity: O(L)
2. Space complexity: O(1)
"""


# === Approach 2: Switch to counting 1's when 2^i exceed c ===
"""
- When 2^i > c, all higher bits of c from i are 0.
  -> Flip all remaining 1's in a and b.
  -> Problem: count number of 1's in remaining part of a and b.
- Only keep remaining part: x = x >> i
- Count number of 1's: 
  . x & (x - 1) clears the lowest set bit of x
    -> Perform until x becomes 0. Count number of steps.
"""


def count_set_bits(x: int) -> int:
    cnt = 0
    while x > 0:
        x &= x - 1
        cnt += 1
    return cnt


class Solution:
    def minFlips(self, a: int, b: int, c: int) -> int:
        flips = 0

        i = 0
        while (1 << i) <= c:
            if get_bit(c, i) == 1:
                if get_bit(a, i) == 0 and get_bit(b, i) == 0:
                    flips += 1
            else:
                if get_bit(a, i) == 1:
                    flips += 1
                if get_bit(b, i) == 1:
                    flips += 1
            i += 1

        # all remaining 1's of a and b must be flipped to 0
        flips += count_set_bits(a >> i)
        flips += count_set_bits(b >> i)

        return flips


"""
Complexity:
- Let L = max_bit_length(a,b,c)

1. Time complexity: still O(L), but faster if c is smaller than a and b
2. Space complexity: O(1)
"""


# === Approach 3: Consider all positions simultaneously ===
"""
- When c[i] = 1
  -> need at least one 1 in a or b.
  -> need 1 flip if a[i] = b[i] = 0 
               (<-> a[i] | b[i] = 0)
  . c & ~(a | b) has set bits at c[i] = 1 and ~(a[i] | b[i]) = 1
                                            (<-> a[i] | b[i] = 0)
    -> flips = count_set_bits(c & ~(a | b))

- When c[i] = 0
  -> both a[i] and b[i] needs to be 0
  -> need 1 flip if x[i] = 1
  . ~c & x has set bits at c[i] = 0 and x = 1
    -> flips = sum(count_set_bits(~c & x) for x in [a, b])

=> Total flips = count_set_bits(c & ~(a | b))
                 + sum(count_set_bits(~c & x) for x in [a, b])
"""


class Solution:
    def minFlips(self, a: int, b: int, c: int) -> int:
        return (
            count_set_bits(c & ~(a | b))
            + count_set_bits(~c & a)
            + count_set_bits(~c & b)
        )


"""
Complexity:
1. Time complexity: O(1)
2. Space complexity: O(1)
"""
