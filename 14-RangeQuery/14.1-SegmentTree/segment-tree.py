class SegmentTree:
    """Segment tree for range sum query"""

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
        self.tree[i] = self.tree[lci] + self.tree[rci]  # store aggregated result

    def query(self, left: int, right: int, i: int, qleft: int, qright: int) -> int:
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
        left_result = self.query(left, mid, 2 * i + 1, qleft, qright)
        right_result = self.query(mid + 1, right, 2 * i + 2, qleft, qright)
        return left_result + right_result

    def update(self, left: int, right: int, i: int, pos: int, val: int) -> None:
        """Update segment tree when updating nums[pos] = val."""
        if left == right:
            # reach leaf node -> update value
            self.tree[i] = val
            return

        mid = (left + right) // 2
        lci = 2 * i + 1
        rci = 2 * i + 2
        if pos <= mid:
            # find in left subtree
            self.update(left, mid, lci, pos, val)
        else:
            # find in right subtree
            self.update(mid + 1, right, rci, pos, val)

        # update current node based on new values of children
        self.tree[i] = self.tree[lci] + self.tree[rci]


"""
Complexity:
- The tree is balanced -> tree's height is O(log(n)).

1. Time complexity:
- Build: O(n)
  . depends on the number of nodes, which is O(4*n) = O(n).
    (although it doesn't touch every slots)
  . the work at each node is O(1).

- Query: O(log(n))
  . At each level:
    . Any node fully outside [qleft, qright] returns 0 immediately.
    . Any node fully contained in [qleft, qright] returns immediately.
    . Partial overlaps only happen at the boundaries of the query range.
      And there are only 2 boundaries.
  -> At most 2 nodes per level will result in further recursive call.
  -> At most 4 nodes are processed at each level.
  -> Work across levels: O(4*h) = O(log(n))

- Update: O(log(n)) 
  . an update follows exactly 1 path from root to a leaf.
  . the work at each node is O(1).

2. Space complexity: O(n)
- 'tree' array: O(4*n) = O(n)
- recursion stack: O(log(n))  
"""


# ===== Example usage =====
nums = [1, 3, 5, 7, 9, 11]
n = len(nums)
st = SegmentTree(nums)

print(f"Original array: {nums}")
print(f"Sum of range [1, 3]: {st.query(0, n - 1, 0, 1, 3)}")  # 3 + 5 + 7 = 15

print("Updated index 1 to 10.")
nums[1] = 10
st.update(0, n - 1, 0, 1, 10)

print(f"New array: {nums}")  # [1, 10, 5, 7, 9, 11]
print(f"New sum of range [1, 3]: {st.query(0, n - 1, 0, 1, 3)}")  # 10 + 5 + 7 = 22
