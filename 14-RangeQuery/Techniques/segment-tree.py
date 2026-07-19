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


"""
Complexity:
- Let n = len(nums)
- The tree is balanced -> h = O(log(n))

1. Time complexity:
- Build tree: O(4*n) = O(n)

- Query: O(log(n))
  . At each level:
    . Any node fully outside [qleft, qright] returns 0 immediately.
    . Any node fully contained in [qleft, qright] returns immediately.
    . Partial overlaps only happen at 2 boundaries of the query range.
  -> At most 2 nodes per level will result in further recursive call.
  -> At most 4 nodes are processed at each level.
  -> Work across levels: O(4*h) = O(log(n))

- Update: O(h) = O(log(n)) 
  . an update follows exactly 1 path from root to a leaf.

2. Space complexity: O(n + log(n)) = O(n)
- 'tree' array: O(4*n) = O(n)
- recursion stack: O(h) = O(log(n))
"""


# ===== Quick test =====
nums = [1, 3, 5, 7, 9, 11]
n = len(nums)
st = SegmentTree(nums)

# Sum of nums[1..3]
assert st.query(qleft=1, qright=3, left=0, right=n - 1, i=0) == 3 + 5 + 7

# Update nums[1] = 10
nums[1] = 10
st.update(pos=1, val=10, left=0, right=n - 1, i=0)
assert nums == [1, 10, 5, 7, 9, 11]

# Sum of nums[1..3] after update nums[1] = 10
assert st.query(qleft=1, qright=3, left=0, right=n - 1, i=0) == 10 + 5 + 7

print("All tests passed")
