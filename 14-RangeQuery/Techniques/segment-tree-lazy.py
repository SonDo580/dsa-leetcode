from abc import ABC, abstractmethod


class BaseSegmentTreeLazy(ABC):
    def __init__(self, nums: list[int]):
        n = len(nums)
        self.tree = [0] * 4 * n
        self.__build_tree(nums, left=0, right=n - 1, i=0)

        # pending updates (value to add to each element in node's range)
        self.lazy = [0] * 4 * n

    def _lci(self, i: int) -> int:
        return 2 * i + 1

    def _rci(self, i: int) -> int:
        return 2 * i + 2

    def __build_tree(self, nums: list[int], left: int, right: int, i: int) -> None:
        if left == right:
            # reached leaf node
            self.tree[i] = nums[left]
            return

        mid = (left + right) // 2
        lci = self._lci(i)
        rci = self._rci(i)
        self.__build_tree(nums, left=left, right=mid, i=lci)  # build left subtree
        self.__build_tree(nums, left=mid + 1, right=right, i=rci)  # build right subtree
        self.tree[i] = self.tree[lci] + self.tree[rci]  # store aggregated result

    @abstractmethod
    def update_range(
        self, qleft: int, qright: int, inc: int, left: int, right: int, i: int
    ) -> None: ...

    @abstractmethod
    def query(self, qleft: int, qright: int, left: int, right: int, i: int) -> int: ...


class SegmentTreeLazyV1(BaseSegmentTreeLazy):
    """
    Segment tree for range sum query with range updates.
    Use lazy propagation (v1).
    """

    def __process_pending(self, left: int, right: int, i: int) -> None:
        """
        Propagate pending update to direct children of node i
        (Node i has been updated)."""
        # process_pending is never called on a leaf node
        # - only called when node's range partially overlaps with query/update range
        # - a leaf's range (single point) is either outside or inside query/update range 
        assert left < right

        # no pending update
        if self.lazy[i] == 0:  
            return

        # apply update to direct children
        inc = self.lazy[i]
        mid = (left + right) // 2
        lci = self._lci(i)
        rci = self._rci(i)
        self.lazy[lci] += inc
        self.lazy[rci] += inc
        self.tree[lci] += inc * (mid - left + 1)
        self.tree[rci] += inc * (right - mid)

        # reset pending state for current node
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
        self.__process_pending(left, right, i)

        # update children
        mid = (left + right) // 2
        lci = self._lci(i)
        rci = self._rci(i)
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
        self.__process_pending(left, right, i)

        # aggregate result from both halves
        mid = (left + right) // 2
        left_result = self.query(qleft, qright, left=left, right=mid, i=self._lci(i))
        right_result = self.query(
            qleft, qright, left=mid + 1, right=right, i=self._rci(i)
        )
        return left_result + right_result


class SegmentTreeLazyV2(BaseSegmentTreeLazy):
    """
    Segment tree for range sum query with range updates.
    Use lazy propagation (v2).
    """

    def __process_pending(self, left: int, right: int, i: int) -> None:
        """
        Apply pending update to node i and
        propagate pending update to its direct children.
        """
        if self.lazy[i] == 0:
            # no pending update
            return

        # apply pending update to node i
        inc = self.lazy[i]
        self.tree[i] += inc * (right - left + 1)

        # reset pending state for node i
        self.lazy[i] = 0

        if left < right:  # node i is not a leaf
            # propagate pending update to direct children
            lci = self._lci(i)
            rci = self._rci(i)
            self.lazy[lci] += inc
            self.lazy[rci] += inc

    def update_range(
        self, qleft: int, qright: int, inc: int, left: int, right: int, i: int
    ) -> None:
        """Add 'inc' to all elements in range [qleft, qright]."""
        # query range is outside node's range -> skip
        if qright < left or qleft > right:
            return

        # node's range is completely inside query range
        if qleft <= left and right <= qright:
            # save pending update
            self.lazy[i] += inc
            return

        # === partial overlap ===

        # apply pending update to current node and
        # propagate pending update to direct children
        self.__process_pending(left, right, i)

        # update children
        mid = (left + right) // 2
        lci = self._lci(i)
        rci = self._rci(i)
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
            # apply pending update before reading node value
            self.__process_pending(left, right, i)
            return self.tree[i]

        # === partial overlap ===

        # apply pending update to current node and
        # propagate pending update to direct children
        self.__process_pending(left, right, i)

        # aggregate result from both halves
        mid = (left + right) // 2
        left_result = self.query(qleft, qright, left=left, right=mid, i=self._lci(i))
        right_result = self.query(
            qleft, qright, left=mid + 1, right=right, i=self._rci(i)
        )
        return left_result + right_result


"""
Complexity:
- Let n = len(nums)
- The tree is balanced -> h = O(log(n)).

1. Time complexity:
- Build tree: O(4*n) = O(n)
- Process pending update: O(1)
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
from typing import Type

StClasses: list[Type[BaseSegmentTreeLazy]] = [SegmentTreeLazyV1, SegmentTreeLazyV2]
for StClass in StClasses:
    nums = [1, 1, 1, 1, 1]
    n = len(nums)
    st = StClass(nums)

    assert st.query(qleft=0, qright=3, left=0, right=n - 1, i=0) == 1 + 1 + 1 + 1

    # Add 10 to nums[0..2]
    for i in range(3):
        nums[i] += 10
    st.update_range(qleft=0, qright=2, inc=10, left=0, right=n - 1, i=0)
    assert nums == [11, 11, 11, 1, 1]

    assert st.query(qleft=0, qright=3, left=0, right=n - 1, i=0) == 11 + 11 + 11 + 1

    print(f"All {StClass.__name__} tests passed")
