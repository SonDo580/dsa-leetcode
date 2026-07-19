class SegmentTreeLazy:
    """
    Segment tree for range sum query with range updates.
    Use lazy propagation.
    """

    def __init__(self, nums: list[int]):
        n = len(nums)
        self.tree = [0] * 4 * n
        self.__build_tree(nums, left=0, right=n - 1, i=0)

        # Store pending updates
        # (value to add to each element in the range of each node)
        self.lazy = [0] * 4 * n

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

    def __push_update(self, left: int, right: int, i: int) -> None:
        """Propagate pending update to direct children of node i."""
        if self.lazy[i] == 0:
            # no pending update
            return

        mid = (left + right) // 2
        lci = self.__lci(i)
        rci = self.__rci(i)

        # Apply update to direct children
        inc = self.lazy[i]
        self.lazy[lci] += inc
        self.lazy[rci] += inc
        self.tree[lci] += inc * (mid - left + 1)
        self.tree[rci] += inc * (right - mid)

        # Reset lazy state for current node
        self.lazy[i] = 0

    def update_range(
        self, qleft: int, qright: int, inc: int, left: int, right: int, i: int
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
        self.__push_update(left, right, i)

        # update children
        mid = (left + right) // 2
        lci = self.__lci(i)
        rci = self.__rci(i)
        self.update_range(qleft, qright, inc, left=left, right=mid, i=lci)
        self.update_range(qleft, qright, inc, left=mid + 1, right=right, i=rci)

        # update current node after updating children
        self.tree[i] = self.tree[lci] + self.tree[rci]

    def query(self, qleft: int, qright: int, left: int, right: int, i: int) -> int:
        """Return aggregated result for the range [qleft, qright]."""
        # query range is outside node's range -> return 0
        if qright < left or qleft > right:
            return 0

        # node's range is completely inside query range
        # -> return value of the node
        if qleft <= left and right <= qright:
            return self.tree[i]

        # partial overlap: push pending update down to ensure children have correct values
        self.__push_update(left, right, i)

        mid = (left + right) // 2
        left_result = self.query(qleft, qright, left=left, right=mid, i=self.__lci(i))
        right_result = self.query(
            qleft, qright, left=mid + 1, right=right, i=self.__rci(i)
        )
        return left_result + right_result


"""
Complexity:
- Let n = len(nums)
- The tree is balanced -> h = O(log(n)).

1. Time complexity:
- Build tree: O(4*n) = O(n)
- Push update: O(1)
- Query: O(log(n))
  . If node's range is completely outside OR fully contained in query range 
    -> Return immediately
  . Partially overlaps can only happen at boundaries.
    -> At most 2 nodes per level can spawn further recursive calls, 2 calls for each node.
    -> At most 4 nodes are processed at each level
  -> Work across levels: O(4*h) = O(log(n))
- Update range: O(log(n)) (similar to Query)

2. Space complexity: O(n)
- 'tree': O(4*n) = O(n)
- 'lazy': O(4*n) = O(n)
- recursion stack: O(log(n))  
"""


# ===== Quick test =====
nums = [1, 1, 1, 1, 1]
n = len(nums)
st = SegmentTreeLazy(nums)

assert st.query(qleft=0, qright=3, left=0, right=n - 1, i=0) == 1 + 1 + 1 + 1

# Add 10 to nums[0..2]
for i in range(3):
    nums[i] += 10
st.update_range(qleft=0, qright=2, inc=10, left=0, right=n - 1, i=0)
assert nums == [11, 11, 11, 1, 1]

assert st.query(qleft=0, qright=3, left=0, right=n - 1, i=0) == 11 + 11 + 11 + 1

print("All tests passed")
