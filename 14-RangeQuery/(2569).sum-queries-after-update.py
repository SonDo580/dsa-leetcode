"""
https://leetcode.com/problems/handling-sum-queries-after-update/description/

You are given two 0-indexed arrays 'nums1' and 'nums2' and a 2D array 'queries' of queries.

There are 3 types of queries:
- For a query of type 1, queries[i] = [1, l, r].
  Flip the values from 0 to 1 and from 1 to 0 in nums1 from index l to index r.
- For a query of type 2, queries[i] = [2, p, 0].
  For every index 0 <= i < n, set nums2[i] = nums2[i] + nums1[i] * p.
- For a query of type 3, queries[i] = [3, 0, 0].
  Find the sum of the elements in nums2.

Return an array containing all the answers to the third type queries.
"""


# === Approach 1: Iterate every time ===
def handle_query(
    nums1: list[int], nums2: list[int], queries: list[list[int]]
) -> list[int]:
    n = len(nums2)  # = len(nums1)
    ans: list[int] = []

    for qtype, arg1, arg2 in queries:
        if qtype == 1:
            for i in range(arg1, arg2 + 1):
                nums1[i] = 1 - nums1[i]  # 1 -> 0, 0 -> 1
        elif qtype == 2:
            for i in range(n):
                nums2[i] += nums1[i] * arg1
        elif qtype == 3:
            ans.append(sum(nums2))

    return ans


"""
Complexity:
- Let n = len(nums1) = len(nums2)
      q = len(queries)

1. Time complexity: O(n*q)
- Answer each query type:
  . type 1 query: O(arg2-arg1+1) = O(n)
  . type 2 query: O(n)
  . type 3 query: O(n)
-> Answer q queries: O(n*q)

2. Space complexity: O(1)
"""


# === Approach 2: Segment tree ===
"""
- Use a segment tree where each node tracks:
  . Number of 1's (or 0's) in managed range over 'nums1'.
  . Sum of elements in managed range over 'nums2'.
- Use lazy propagation to handle range update.
- Handle type 1 query:
  . If node's range is outside update range: skip
  . If node's range is contained in update range:
    . count_ones = managed_range - count_ones
      (flip all 1's to 0's, and vice versa)
    . Save pending update to propagate to children later
  . Partial overlap:
    . Apply pending update to children
    . Update children
    . Combine count_ones in both ranges (sum)
- Handle type 2 query:
  . root's range == update range (always)
    -> root's sum increases by p * count_ones
- Handle type 3 query:
  . Return precomputed sum at the root (sum of all items in 'nums2').
- Notes:
  . We don't need to store sum for every range, just the root
    (since the update range of type 2 query is the whole range).
    -> use a single variable.
  . Time complexity is reduced but 'nums1' and 'nums2' are not updated.
    We only operate on the segment tree.
"""


class SegmentTreeLazy:
    def __init__(self, nums1: list[int], nums2: list[int], n: int):
        self.nums2_sum = sum(nums2)

        # node's value = number of 1's in managed range over nums1
        self.tree = [0] * 4 * n

        # pending update to propagate to children after updating a node
        # . lazy[i] = True <-> needs to flip managed range of node i's children
        self.lazy = [False] * 4 * n

        self.__build_tree(nums1, left=0, right=n - 1, i=0)

    def __lci(self, i: int) -> int:
        return 2 * i + 1

    def __rci(self, i: int) -> int:
        return 2 * i + 2

    def __build_tree(self, nums1: list[int], left: int, right: int, i: int) -> None:
        if left == right:
            # reached leaf node
            self.tree[i] = nums1[left]
            return

        # build left and right subtrees
        mid = (left + right) // 2
        lci = self.__lci(i)
        rci = self.__rci(i)
        self.__build_tree(nums1, left=left, right=mid, i=lci)
        self.__build_tree(nums1, left=mid + 1, right=right, i=rci)

        # aggregate result
        self.tree[i] = self.tree[lci] + self.tree[rci]

    def __process_pending(self, left: int, right: int, i: int) -> None:
        """
        Propagate pending update from node i to its direct children
        (Value of node i has been updated).
        """
        if not self.lazy[i]:
            # no flips happened at node i
            # (or even number of flips -> cancel out)
            return

        # flip managed ranges of children
        mid = (left + right) // 2
        lci = self.__lci(i)
        rci = self.__rci(i)
        self.tree[lci] = (mid - left + 1) - self.tree[lci]
        self.tree[rci] = (right - mid) - self.tree[rci]

        # save pending update (need flip) to propagate to children later
        # . flip twice should cancel the flip
        self.lazy[lci] = not self.lazy[lci]
        self.lazy[rci] = not self.lazy[rci]

        # reset pending state for node i after propagation
        self.lazy[i] = False

    def flip_range(
        self, qleft: int, qright: int, left: int, right: int, i: int
    ) -> None:
        """Update when flipping 0 to 1 and 1 to 0 in nums1[qleft..qright]."""
        # node is outside update range
        if qright < left or right < qleft:
            return

        # node is contained in update range
        if qleft <= left and right <= qright:
            # count_ones = managed_range - count_ones
            self.tree[i] = (right - left + 1) - self.tree[i]

            # save pending update (need flip) to propagate to children later
            # . flip twice should cancel the flip
            self.lazy[i] = not self.lazy[i]

            return

        # === partial overlap ===

        # propagate pending update to children
        self.__process_pending(left, right, i)

        # update children
        mid = (left + right) // 2
        lci = self.__lci(i)
        rci = self.__rci(i)
        self.flip_range(qleft, qright, left=left, right=mid, i=lci)
        self.flip_range(qleft, qright, left=mid + 1, right=right, i=rci)

        # update current node after updating children
        self.tree[i] = self.tree[lci] + self.tree[rci]

    def increase_sum(self, p: int) -> None:
        """
        Increase each nums2[i] by p*nums1[i]
        -> sum(nums2) increases by p*count_ones_in_nums1.
        """
        self.nums2_sum += p * self.tree[0]


class Solution:
    def handleQuery(
        self, nums1: list[int], nums2: list[int], queries: list[list[int]]
    ) -> list[int]:
        n = len(nums2)  # = len(nums1)
        st = SegmentTreeLazy(nums1, nums2, n)

        ans: list[int] = []
        for qtype, arg1, arg2 in queries:
            if qtype == 1:
                # don't actually update nums1
                st.flip_range(qleft=arg1, qright=arg2, left=0, right=n - 1, i=0)
            elif qtype == 2:
                # don't actually update nums2
                st.increase_sum(p=arg1)
            elif qtype == 3:
                # add precomputed sum(nums2) to answer
                ans.append(st.nums2_sum)

        return ans


"""
Complexity:
- Let n = len(nums1) = len(nums2)
      q = len(queries)
- The tree is full and balanced:
  . number of nodes: O(4*n) (last level contains empty slots)
  . height: h = O(log(n))

1. Time complexity: O(n + q*log(n))
- Init segment tree: O(n)
- Answer each query type: 
  . type 1: O(log(n))
  . type 2: O(1)
  . type 3: O(1)
  -> Answer q queries: O(q * max(log(n), 1, 1)) = O(q*log(n))

2. Space complexity: O(n)
- 'st': O(4*n) = O(n)
- recursion stack: O(h) = O(log(n))
"""
