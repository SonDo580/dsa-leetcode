"""
https://leetcode.com/problems/range-sum-query-mutable/

Given an integer array 'nums', handle multiple queries of the following types:
- Update the value of an element in nums.
- Calculate the sum of the elements of nums between indices left and right inclusive where left <= right.

Implement the NumArray class:
- NumArray(int[] nums) Initializes the object with the integer array nums.
- void update(int index, int val) Updates the value of nums[index] to be val.
- int sumRange(int left, int right) Returns the sum of the elements of nums between indices left and right inclusive.
"""


# ===== Approach 1: "Normal" way =====
# (exceed time limit)
class NumArray:
    def __init__(self, nums: list[int]):
        self.nums = nums

    def update(self, index: int, val: int) -> None:
        self.nums[index] = val

    def sumRange(self, left: int, right: int) -> int:
        total = 0
        for i in range(left, right + 1):
            total += self.nums[i]
        return total


"""
Complexity:
- Let n = len(nums)

1. Time complexity:
- update: O(1)
- sumRange: O(n)

2. Space complexity: O(1)
"""


# ===== Approach 2: Prefix sum =====
# (exceed time limit, this doesn't work well for mutable array)
class NumArray:
    def __init__(self, nums: list[int]):
        self.nums = nums
        self.n = len(nums)
        self.prefix = self.build_prefix()

    def build_prefix(self) -> list[int]:
        # prefix[i] = sum(nums[0..i-1])
        prefix: list[int] = [0] * (self.n + 1)
        for i in range(1, self.n + 1):
            prefix[i] = prefix[i - 1] + self.nums[i - 1]
        return prefix

    def update(self, index: int, val: int) -> None:
        self.nums[index] = val
        for i in range(index + 1, self.n + 1):
            self.prefix[i] = self.prefix[i - 1] + self.nums[i - 1]

    def sumRange(self, left: int, right: int) -> int:
        return self.prefix[right + 1] - self.prefix[left]


"""
Complexity:

1. Time complexity:
- build_prefix: O(n)
- update: O(n)
- sumRange: O(1)

2. Space complexity: O(n) for 'prefix'
"""


# ===== Approach 3: Square Root Decomposition =====
"""
- Split the original array into approximately sqrt(n) blocks,
  each block contains approximately sqrt(n) elements.
- Each block holds the aggregated result of its elements.
- When update an element, find the affected block and update its result.
- When query a range:
  . for the blocks that are fully contained inside the range,
    accumulate the aggregated results.
  . for the blocks at 2 boundaries, iterate over the elements.
"""
import math


class NumArray:
    def __init__(self, nums: list[int]):
        self.nums = nums
        n = len(nums)
        self.block_size = int(math.sqrt(n))
        num_blocks = math.ceil(n / self.block_size)

        # Store aggregated results for each block
        self.blocks = [0] * num_blocks
        for i in range(n):
            block_idx = i // self.block_size
            self.blocks[block_idx] += nums[i]

    def update(self, index: int, val: int) -> None:
        old_val = self.nums[index]
        self.nums[index] = val

        block_idx = index // self.block_size
        self.blocks[block_idx] += val - old_val

    def sumRange(self, left: int, right: int) -> int:
        total = 0

        # Process the first part until we reach a block boundary
        while left % self.block_size != 0 and left <= right:
            total += self.nums[left]
            left += 1

        # Process blocks that are completely contained in the range
        while left + self.block_size - 1 <= right:
            block_idx = left // self.block_size
            total += self.blocks[block_idx]
            left += self.block_size

        # Process the remaining part after the last complete block
        while left <= right:
            total += self.nums[left]
            left += 1

        return total


"""
Complexity:

1. Time complexity:
- Compute 'blocks': O(n)
- update: O(1)
- sumRange: O(sqrt(n))

2. Space complexity: O(sqrt(n)) for 'blocks'

Note: O(log(n)) < O(sqrt(n)) < O(n)
"""


# ===== Approach 4: Binary Indexed Tree =====
# ...


# ===== Approach 5: Segment Tree =====
class SegmentTree:
    def __init__(self, nums: list[int]):
        n = len(nums)
        self.tree = [0] * 4 * n
        self.build_tree(nums, 0, n - 1, 0)

    def build_tree(self, nums: list[int], left: int, right: int, i: int) -> None:
        if left == right:
            # reached leaf node
            self.tree[i] = nums[left]
            return

        mid = (left + right) // 2
        lci = 2 * i + 1
        rci = 2 * i + 2
        self.build_tree(nums, left, mid, lci)  # build left subtree
        self.build_tree(nums, mid + 1, right, rci)  # build right subtree
        self.tree[i] = self.tree[lci] + self.tree[rci]  # store aggregated results

    def update(self, left: int, right: int, i: int, pos: int, val: int) -> None:
        """Update segment tree when updating nums[pos] = val."""
        if left == right:
            # reached leaf node -> update value
            self.tree[i] = val
            return

        mid = (left + right) // 2
        lci = 2 * i + 1
        rci = 2 * i + 2
        if pos <= mid:
            # go down the left subtree
            self.update(left, mid, lci, pos, val)
        else:
            # go down the right subtree
            self.update(mid + 1, right, rci, pos, val)

        # update current node after based on new values of children
        self.tree[i] = self.tree[lci] + self.tree[rci]

    def query(self, left: int, right: int, i: int, qleft: int, qright: int) -> int:
        """Return the sum of elements managed by node i in the range [qleft, qright]."""
        # Query range is outside node's range -> return 0
        if qright < left or qleft > right:
            return 0

        # Node's range is completely inside query range -> return precomputed value
        if qleft <= left and right <= qright:
            return self.tree[i]

        # Partial overlap -> query both halves and sum the results
        mid = (left + right) // 2
        left_result = self.query(left, mid, 2 * i + 1, qleft, qright)
        right_result = self.query(mid + 1, right, 2 * i + 2, qleft, qright)
        return left_result + right_result


class NumArray:
    def __init__(self, nums: list[int]):
        self.st = SegmentTree(nums)
        self.n = len(nums)

    def update(self, index: int, val: int) -> None:
        # Only modifying segment tree still works
        # nums[index] = val
        self.st.update(0, self.n - 1, 0, index, val)

    def sumRange(self, left: int, right: int) -> int:
        return self.st.query(0, self.n - 1, 0, left, right)


"""
Complexity: check `segment-tree.py`

1. Time complexity:
- init: O(n)
- update: O(log(n))
- sumRange: O(log(n))

2. Space complexity: O(n)
"""
