class SegmentTreeLazy:
    """
    Segment tree for range sum query with range updates.
    Apply lazy propagation.
    """

    def __init__(self, nums: list[int]):
        n = len(nums)
        self.tree = [0] * 4 * n
        self.build_tree(nums, 0, n - 1, 0)

        # Store pending updates
        # (value to add to each element in the range of each node)
        self.lazy = [0] * 4 * n

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
        self.tree[i] = self.tree[lci] + self.tree[rci]  # store aggregated result

    def _push_update(self, left: int, right: int, i: int) -> None:
        """Propagate pending update from node i to its children."""
        if self.lazy[i] == 0:
            # no pending update
            return

        mid = (left + right) // 2
        lci = 2 * i + 1
        rci = 2 * i + 2

        # Apply update to direct children
        inc = self.lazy[i]
        self.lazy[lci] += inc
        self.lazy[rci] += inc
        self.tree[lci] += inc * (mid - left + 1)
        self.tree[rci] += inc * (right - mid)

        # Reset lazy for current node
        self.lazy[i] = 0

    def update_range(
        self, left: int, right: int, i: int, qleft: int, qright: int, inc: int
    ) -> None:
        """Add 'inc' to all elements in range [qleft, qright]."""
        # query range is outside node's range -> skip
        if qright < left or qleft > right:
            return

        # node's range is completely inside query range
        # -> update node value and save pending update (propagate to children later)
        if qleft <= left and right <= qright:
            self.tree[i] += inc * (right - left + 1)
            self.lazy[i] += inc
            return

        # partial overlap: push pending update down to ensure children have correct values
        self._push_update(left, right, i)

        mid = (left + right) // 2
        lci = 2 * i + 1
        rci = 2 * i + 2
        self.update_range(left, mid, lci, qleft, qright, inc)
        self.update_range(mid + 1, right, rci, qleft, qright, inc)
        self.tree[i] = self.tree[lci] + self.tree[rci]

    def query(self, left: int, right: int, i: int, qleft: int, qright: int) -> int:
        """Return aggregated result for the range [qleft, qright]."""
        # query range is outside node's range -> return 0
        if qright < left or qleft > right:
            return 0

        # node's range is completely inside query range
        # -> return value of the node
        if qleft <= left and right <= qright:
            return self.tree[i]

        # Push pending update down to ensure children have correct values
        self._push_update(left, right, i)

        mid = (left + right) // 2
        left_result = self.query(left, mid, 2 * i + 1, qleft, qright)
        right_result = self.query(mid + 1, right, 2 * i + 2, qleft, qright)
        return left_result + right_result


"""
Complexity:
- The tree is balanced -> tree's height is O(log(n)).

1. Time complexity: 
(Similar to analysis in `segment-tree.py`)
- Build: O(n)
- Push update: O(1)
- Query: O(log(n))
- Update range: O(log(n)) (similar to query's time complexity analysis)

2. Space complexity: O(n)
- 'tree': O(4*n) = O(n)
- 'lazy': O(4*n) = O(n)
- recursion stack: O(log(n))  
"""


# ===== Usage =====
nums = [1, 1, 1, 1, 1]
print(f"original array: {nums}")

st = SegmentTreeLazy(nums)

print("Add 10 to indices [0, 2]")
for i in range(3):
    nums[i] += 10
st.update_range(0, 4, 0, 0, 2, 10)

print(f"new array: {nums}")  # [11, 11, 11, 1, 1]
print(f"Sum after range update: {st.query(0, 4, 0, 0, 4)}")  # sum(nums) = 35
