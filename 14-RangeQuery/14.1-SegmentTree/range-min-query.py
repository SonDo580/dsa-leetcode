"""
Given an integer array 'nums', handle multiple queries of the following types:
- Update the value of an element in nums.
- Return the minimum element between indices left and right inclusive where left <= right.

Implement the NumArray class:
- NumArray(int[] nums) Initializes the object with the integer array nums.
- void update(int index, int val) Updates the value of nums[index] to be val.
- int query_min(int left, int right) Returns the minimum element between indices left and right inclusive.
"""

import math


# ===== Approach 1: "Normal" way =====
class NumArray:
    def __init__(self, nums: list[int]):
        self.nums = nums

    def update(self, index: int, val: int) -> None:
        self.nums[index] = val

    def query_min(self, left: int, right: int) -> int:
        ans = math.inf
        for i in range(left, right + 1):
            ans = min(ans, self.nums[i])
        return ans


"""
Complexity:
- Let n = len(nums).

1. Time complexity:
- update: O(1).
- query_min: O(n).

2. Space complexity: O(1)
"""


# ===== Approach 2: Square root decomposition =====
class NumArray:
    def __init__(self, nums: list[int]):
        self.nums = nums
        self.n = len(nums)
        self.block_size = int(math.sqrt(self.n))
        num_blocks = math.ceil(self.n / self.block_size)

        # Record the minimum element for each block
        self.blocks = [math.inf] * num_blocks
        for i in range(self.n):
            block_idx = i // self.block_size
            self.blocks[block_idx] = min(self.blocks[block_idx], nums[i])

    def update(self, index: int, val: int) -> None:
        if val == self.nums[index]:
            return

        old_val = self.nums[index]
        self.nums[index] = val
        block_idx = index // self.block_size

        # If the updated element is not the minimum element in the block,
        # just compare the new value with current minimum.
        if old_val != self.blocks[block_idx]:
            self.blocks[block_idx] = min(self.blocks[block_idx], val)
            return

        # - If the updated element is the minimum element in the block,
        #   iterate through elements of the block to find the new minimum element.
        # - Remember to reset the the block's aggregated result,
        #   since the minimum element has been removed.
        self.blocks[block_idx] = math.inf
        block_start = block_idx * self.block_size
        block_end = min(block_start + self.block_size - 1, self.n - 1)
        for i in range(block_start, block_end + 1):
            self.blocks[block_idx] = min(self.blocks[block_idx], self.nums[i])

    def query_min(self, left: int, right: int) -> int:
        ans = math.inf

        # Process the first part until reaching a block boundary
        while left % self.block_size != 0 and left <= right:
            ans = min(ans, self.nums[left])
            left += 1

        # Process blocks that are completely inside the query range
        while left + self.block_size - 1 <= right:
            block_idx = left // self.block_size
            ans = min(ans, self.blocks[block_idx])
            left += self.block_size

        # Process remaining part after the last complete block
        while left <= right:
            ans = min(ans, self.nums[left])
            left += 1

        return ans


"""
Complexity:

1. Time complexity:
- init: O(n) to build 'blocks'.
- update: O(sqrt(n)).
- query_min: O(sqrt(n)).

2. Space complexity: O(sqrt(n)) for 'blocks'.
"""


# ===== Approach 3: Sparse table =====
# ...


# ===== Approach 4: Segment tree =====
class SegmentTree:
    def __init__(self, nums: list[int]):
        n = len(nums)
        self.tree = [0] * 4 * n
        # self.build_tree

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
        self.tree[i] = min(self.tree[lci], self.tree[rci])  # store aggregated result

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

        # update current node after updating children
        self.tree[i] = min(self.tree[lci], self.tree[rci])

    def query(self, left: int, right: int, i: int, qleft: int, qright: int) -> int:
        """Return the minimum element managed by node i in the range [qleft, qright]."""
        # Query range is outside node's range -> return inf
        if qright < left or qleft > right:
            return math.inf

        # Node's range is completely inside query range -> return precomputed value
        if qleft <= left and right <= qright:
            return self.tree[i]

        # Partial overlap -> query both halves and pick the minimum result
        mid = (left + right) // 2
        left_result = self.query(left, mid, 2 * i + 1, qleft, qright)
        right_result = self.query(mid + 1, right, 2 * i + 2, qleft, qright)
        return min(left_result, right_result)


"""
Complexity: check `segment-tree.py`

1. Time complexity:
- init: O(n)
- update: O(log(n))
- query_min: O(log(n))

2. Space complexity: O(n)
"""


# ===== Tests =====
arr = NumArray([5, 2, 7, 1, 9])
assert arr.query_min(0, 2) == 2, "Min of [5, 2, 7] should be 2"
assert arr.query_min(2, 4) == 1, "Min of [7, 1, 9] should be 1"

arr.update(3, 10)  # [5, 2, 7, 10, 9]
assert arr.query_min(2, 4) == 7, "Min of [7, 10, 9] should be 7"
assert arr.query_min(0, 4) == 2, "Global min should be 2"
assert arr.query_min(4, 4) == 9, "Min of single element range [9] should be 9"

arr.update(3, 3)  # [5, 2, 7, 3, 9]
assert arr.query_min(2, 4) == 3, "Min of [7, 3, 9] should be 3"

print("All tests passed")
