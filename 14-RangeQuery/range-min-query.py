"""
Given an integer array 'nums', handle multiple queries of the following types:
- Update the value of an element in 'nums'.
- Return the minimum element between indices 'left' and 'right' inclusive where left <= right.

Implement the NumArray class:
- NumArray(int[] nums) Initializes the object with the integer array 'nums'.
- void update(int index, int val) Updates the value of nums[index] to be 'val'.
- int query_min(int left, int right) Returns the minimum element between indices 'left' and 'right' inclusive.
"""

# ===== Approach 1: "Normal" way =====
import math


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
- Let n = len(nums)

1. Time complexity:
- update: O(1)
- query_min: O(right - left) = O(n)

2. Space complexity: O(1) (not including 'nums')
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

        # updated element is not block's minimum element
        if old_val != self.blocks[block_idx]:
            self.blocks[block_idx] = min(self.blocks[block_idx], val)
            return

        # === updated element is block's minimum element ===

        # updated_val < old_val -> updated_val is new minimum
        if val < old_val:
            self.blocks[block_idx] = val
            return

        # updated_val > old_val
        # -> another element may become new minimum element
        # -> must iterate through all elements in block to check
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


# ===== Approach 3: Segment tree =====
class SegmentTree:
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
        self.tree[i] = min(self.tree[lci], self.tree[rci])  # store aggregated result

    def update(self, pos: int, val: int, left: int, right: int, i: int) -> None:
        """Update segment tree when updating nums[pos] = val."""
        if left == right:
            # reached leaf node -> update value
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

        # update current node after updating children
        self.tree[i] = min(self.tree[lci], self.tree[rci])

    def query(self, qleft: int, qright: int, left: int, right: int, i: int) -> int:
        """Return the minimum element managed by node i in the range [qleft, qright]."""
        # Query range is outside node's range -> return inf
        if qright < left or qleft > right:
            return math.inf

        # Node's range is completely inside query range -> return precomputed value
        if qleft <= left and right <= qright:
            return self.tree[i]

        # Partial overlap -> query both halves and pick the minimum result
        mid = (left + right) // 2
        left_result = self.query(qleft, qright, left=left, right=mid, i=self.__lci(i))
        right_result = self.query(
            qleft, qright, left=mid + 1, right=right, i=self.__rci(i)
        )
        return min(left_result, right_result)


class NumArray:
    def __init__(self, nums: list[int]):
        self.n = len(nums)
        self.nums = nums
        self.st = SegmentTree(nums)

    def update(self, index: int, val: int) -> None:
        self.nums[index] = val
        self.st.update(pos=index, val=val, left=0, right=self.n - 1, i=0)

    def query_min(self, left: int, right: int) -> int:
        return self.st.query(qleft=left, qright=right, left=0, right=self.n - 1, i=0)


"""
Complexity:
- Let n = len(nums)
- The tree is balanced -> h = O(log(n)) 

1. Time complexity:
- init: O(4*n) = O(n)
- update: O(log(n))
  . Each update follow exactly 1 path from root to a leaf.
- query_min: O(log(n))
  . If node's range is completely outside OR fully contained in query range 
    -> Return immediately
  . Partially overlaps can only happen at boundaries.
    -> At most 2 nodes per level can spawn further recursive calls, 2 calls for each node.
    -> At most 4 nodes are processed at each level
  -> Work across levels: O(4*h) = O(log(n))

2. Space complexity: O(n)
- 'st': O(4*n) = O(n)
- recursion stack: O(log(n))
"""


# ===== Quick test =====
arr = NumArray([5, 2, 7, 1, 9])
assert arr.query_min(left=0, right=2) == 2, "Min of [5, 2, 7] should be 2"
assert arr.query_min(left=2, right=4) == 1, "Min of [7, 1, 9] should be 1"

arr.update(index=3, val=10)  # [5, 2, 7, (10), 9]
assert arr.query_min(left=2, right=4) == 7, "Min of [7, 10, 9] should be 7"
assert arr.query_min(left=0, right=4) == 2, "Global min should be 2"
assert arr.query_min(left=4, right=4) == 9, "Min of [9] should be 9"

arr.update(index=3, val=3)  # [5, 2, 7, (3), 9]
assert arr.query_min(left=2, right=4) == 3, "Min of [7, 3, 9] should be 3"

print("All tests passed")
