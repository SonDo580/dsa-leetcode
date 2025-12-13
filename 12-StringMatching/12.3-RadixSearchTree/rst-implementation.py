"""
General idea:
- Store numbers by breaking them into digits (or bits) and branching.
  -> Map numbers to tree paths.
"""

"""
RST structure (branching by bit):
- Each edge represents a bit value (0 or 1).
- Traversing from root to leaf goes from MSB to LSB.
- Leaves are at the same depth.
  (numbers are represented with the same number of bits)
- A complete path from root to leaf represents an input number.
- A leaf may optionally store decimal value of the number
  to avoid recomputing it when searching.
"""


class RSTNode:
    def __init__(self, value: int | None):
        self.children: dict[int, RSTNode] = {}  # key: 0 | 1
        self.value: int | None = value  # only for leaves


class RST:
    def __init__(self, bits_length: 32 | 64 = 32):
        self.root = RSTNode()
        self.bits_length = bits_length

    def insert(self, value: int) -> None:
        current = self.root
        for i in reversed(range(self.bits_length)):
            bit = (value >> i) & 1
            if bit not in current.children:
                current.children[bit] = RSTNode()
            current = current.children[bit]
        current.value = value

    def search(self, value: int) -> bool:
        current = self.root
        for i in reversed(range(self.bits_length)):
            bit = (value >> i) & 1
            if bit not in current.children:
                return False
            current = current.children[bit]
        return current.value is not None

    def min(self) -> int | None:
        current = self.root
        for _ in reversed(range(self.bits_length)):
            if 0 in current.children:
                current = current.children[0]
            elif 1 in current.children:
                current = current.children[1]
            else:
                return None
        return current.value

    def max(self) -> int | None:
        current = self.root
        for _ in reversed(range(self.bits_length)):
            if 1 in current.children:
                current = current.children[1]
            elif 0 in current.children:
                current = current.children[0]
            else:
                return None
        return current.value

    # ... Other methods ...


"""
Complexity:
- Let n = number of inserted integers
      b = bits length (fixed)

1. Time complexity:
- insert: O(b) ~ O(1)
- search: O(b) ~ O(1)

2. Space complexity: O(n * b) ~ O(n) for the Radix search tree
. bigger when numbers differ early (near the MSB).
. smaller when numbers share long prefixes.
"""
