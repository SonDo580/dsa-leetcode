# The Hamming distance between two integers is the number of positions
# at which the corresponding bits are different.
# Given two integers x and y, return the Hamming distance between them.

# Example 1:
# Input: x = 1, y = 4
# Output: 2
# Explanation:
# 1   (0 0 0 1)
# 4   (0 1 0 0)
#        ↑   ↑

# Example 2:
# Input: x = 3, y = 1
# Output: 1

# Constraints:
# 0 <= x, y <= 2^31 - 1


# ===== Strategy =====
# - Take x XOR y. The result has 1-bit at positions where the original bits are different,
#   and 0-bit everywhere else.
# - Now we need to count the number of 1-bits.
#   Repeatedly check the bits of xor from the right:
#   + Perform xor AND 1. If the result is 1, the last bit is 1.
#   + Do a right shift (xor = xor >> 1) to move to the next bit.
#   + Stop when xor becomes 0 (all bits have been shifted out)


def hamming_distance(x: int, y: int) -> int:
    xor = x ^ y
    count = 0 

    while xor > 0:
        count += xor & 1
        xor >>= 1

    return count


# ===== Complexity =====
# 1. Time complexity: O(1)
# 2. Space complexity: O(1)
