"""
https://leetcode.com/problems/hamming-distance/

The Hamming distance between two integers is the number of positions
at which the corresponding bits are different.
Given two integers x and y, return the Hamming distance between them.
"""

"""
Idea:
- (x XOR y) has bit=1 at positions where corresponding bits are different,
  and bit=0 where corresponding bits are the same.
-> Problem: Count number of 1's in (x XOR y)
"""

# === Approach 1: Check all bits ===
"""
- Repeatedly check the bits of xor_res from the right:
  . If (xor_res AND 1) == 1
    -> LSB = 1 
    -> count += 1
  . xor_res = xor_res >> 1 
    . x,y >= 0 
      -> xor_res >= 0
      -> logical right shift (high bits become 0's)
  . Repeat until xor_res becomes 0.
"""


def hamming_distance(x: int, y: int) -> int:
    xor = x ^ y
    count = 0

    while xor > 0:
        count += xor & 1
        xor >>= 1

    return count


"""
Complexity:
1. Time complexity: O(1) (check all bits)
2. Space complexity: O(1)
"""


# ===== Brian Kernighan's algorithm =====
"""
- n & (n - 1) set lowest bit=1 to 0.
- Apply to Hamming Distance:
  . Repeatedly drop the lowest set bit from xor_res.
    Increment count each time.
  . Stop when xor_res becomes 0.
"""


def hamming_distance(x: int, y: int) -> int:
    xor = x ^ y
    count = 0

    while xor > 0:
        xor &= xor - 1
        count += 1

    return count

"""
Complexity:
1. Time complexity: still O(1) (allow skipping multiple bits -> generally faster).
2. Space complexity: O(1)
"""
