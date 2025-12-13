"""
https://leetcode.com/problems/maximum-xor-of-two-numbers-in-an-array/

Given an integer array 'nums',
return the maximum result of nums[i] XOR nums[j],
where 0 <= i <= j < n.

Constraints:
1 <= nums.length <= 2 * 10^5
0 <= nums[i] <= 2^31 - 1
"""

# ===== Brute-force approach =====
# ================================
"""
- Try XOR all pairs of numbers and find the maximum result.
- Include 0 as result of a number XOR itself.
"""


def find_max_xor(nums: list[int]) -> int:
    n = len(nums)
    max_xor = 0
    for i in range(n - 1):
        for j in range(i + 1, n):
            max_xor = max(max_xor, nums[i] ^ nums[j])
    return max_xor


"""
Complexity:

1. Time complexity: O(n^2)

2. Space complexity: O(1)
"""


# ===== Radix search tree =====
# =============================
"""
- For each number, find a number with "opposite" bits going from MSB to LSB
  (because 0 ^ 1 = 1).
- To do that efficiently, build a radix search tree (branching by bits).
  . 0 <= nums[i] <= 2^31 - 1 -> the tree height is 32 (bits length = 32).
- Still init max XOR as 0 (a number XOR itself).
"""


class RSTNode:
    def __init__(self):
        self.children: list[RSTNode | None] = [None, None]  # key: 0 | 1
        self.value: int | None = None  # decimal value - only for leaves


class RST:
    def __init__(self, bits_length: int = 32):
        self.root = RSTNode()
        self.bits_length = bits_length

    def insert(self, value: int) -> None:
        """Insert a decimal value."""
        current = self.root
        for i in reversed(range(self.bits_length)):
            bit = (value >> i) & 1
            if current.children[bit] is None:
                current.children[bit] = RSTNode()
            current = current.children[bit]
        current.value = value

    def find_value_for_max_xor(self, value: int) -> int:
        """
        At each step, go along the opposite-bit branch if possible.
        """
        current = self.root
        for i in reversed(range(self.bits_length)):
            bit = (value >> i) & 1
            opposite_bit = 1 - bit
            if current.children[opposite_bit] is not None:
                current = current.children[opposite_bit]
            else:
                current = current.children[bit]
        return current.value


def find_max_xor(nums: list[int]) -> int:
    rst = RST()
    for value in nums:
        rst.insert(value)

    max_xor = 0
    for value in nums:
        max_xor = max(max_xor, value ^ rst.find_value_for_max_xor(value))
    return max_xor


"""
Complexity:
- Let n = len(nums)
      b = bits length (32)

1. Time complexity: 
- Build RST (insert n values): O(n * b)
- Find maximum XOR: O(n * b)
=> Overall: O(n * b)

2. Space complexity: O(n * b) for the RST
"""
