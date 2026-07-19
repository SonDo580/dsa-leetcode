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


# ===== Approach 1: Normal way =====
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
        self.prefix = self.__build_prefix()

    def __build_prefix(self) -> list[int]:
        # prefix[i] = sum(nums[0..i-1])
        # . prefix[0] = sum([])
        # . prefix[n] = sum(nums)
        # . sum[i..j] = prefix[j+1] - prefix[i]
        prefix: list[int] = [0] * (self.n + 1)
        for i in range(1, self.n + 1):
            prefix[i] = prefix[i - 1] + self.nums[i - 1]
        return prefix

    def update(self, index: int, val: int) -> None:
        self.nums[index] = val
        # must rebuild prefix sum array
        # . worst case: index = 0
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

        # Process the first part until we reach a block start
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
- init: O(n)
- update: O(1)
- sumRange: O(sqrt(n))

2. Space complexity: O(sqrt(n)) for 'blocks'

Note: O(log(n)) < O(sqrt(n)) < O(n)
"""


# ===== Approach 3: Segment Tree =====
class SegmentTree:
    """Segment tree for range sum query"""

    def __init__(self, nums: list[int]):
        n = len(nums)
        self.tree = [0] * 4 * n
        self.__build_tree(nums, left=0, right=n - 1, i=0)

    def __lci(self, i: int) -> int:
        return 2 * i + 1

    def __rci(self, i: int) -> int:
        return 2 * i + 2

    def __build_tree(self, nums: list[int], left: int, right: int, i: int) -> None:
        if left == right:
            # reached leaf node
            self.tree[i] = nums[left]
            return

        mid = (left + right) // 2
        lci = self.__lci(i)
        rci = self.__rci(i)
        self.__build_tree(nums, left=left, right=mid, i=lci)  # build left subtree
        self.__build_tree(nums, left=mid + 1, right=right, i=rci)  # build right subtree
        self.tree[i] = self.tree[lci] + self.tree[rci]  # store aggregated result

    def query(self, qleft: int, qright: int, left: int, right: int, i: int) -> int:
        """Return aggregated result for the range [qleft, qright]."""
        # query range is outside node's range -> return 0
        if qright < left or qleft > right:
            return 0

        # node's range is completely inside query range
        # -> return value of the node
        if qleft <= left and right <= qright:
            return self.tree[i]

        # partial overlap -> query both halves
        mid = (left + right) // 2
        left_result = self.query(qleft, qright, left=left, right=mid, i=self.__lci(i))
        right_result = self.query(
            qleft, qright, left=mid + 1, right=right, i=self.__rci(i)
        )
        return left_result + right_result

    def update(self, pos: int, val: int, left: int, right: int, i: int) -> None:
        """Update segment tree when updating nums[pos] = val."""
        if left == right:
            # reach leaf node -> update value
            self.tree[i] = val
            return

        mid = (left + right) // 2
        lci = self.__lci(i)
        rci = self.__rci(i)
        if pos <= mid:
            # target is in left subtree
            self.update(pos, val, left=left, right=mid, i=lci)
        else:
            # target is in right subtree
            self.update(pos, val, left=mid + 1, right=right, i=rci)

        # update current node based on new values of children
        self.tree[i] = self.tree[lci] + self.tree[rci]


class NumArray:
    def __init__(self, nums: list[int]):
        self.nums = nums
        self.st = SegmentTree(nums)
        self.n = len(nums)

    def update(self, index: int, val: int) -> None:
        self.nums[index] = val
        self.st.update(pos=index, val=val, left=0, right=self.n - 1, i=0)

    def sumRange(self, left: int, right: int) -> int:
        return self.st.query(qleft=left, qright=right, left=0, right=self.n - 1, i=0)


"""
Complexity:
- Let n = len(nums)
- The tree is balance -> h = O(log(n))

1. Time complexity:
- init: O(4*n) = O(n)
- update: O(log(n))
  . Each update follows exactly a path from root to a leaf.
- sumRange: O(log(n))
  . Only query children when the ranges are partially overlap. 
    -> At most 2 nodes per level can spawn extra recursive calls (2 calls for each node)
    -> At most 4 nodes are processed at each level.
  -> Work across levels: O(4*h) = O(log(n))

2. Space complexity: O(n)
- 'st': O(4*n) = O(n)
- recursion stack: O(log(n))
"""
