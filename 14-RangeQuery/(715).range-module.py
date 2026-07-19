"""
https://leetcode.com/problems/range-module/

A Range Module is a module that tracks ranges of numbers.
Design a data structure to track the ranges represented as half-open intervals and query about them.

A half-open interval [left, right) denotes all the real numbers x where left <= x < right.

Implement the RangeModule class:
- RangeModule()
  . Initializes the object of the data structure.
- void addRange(int left, int right)
  . Adds the half-open interval [left, right), tracking every real number in that interval.
    Adding an interval that partially overlaps with currently tracked numbers
    should add any numbers in the interval [left, right) that are not already tracked.
- boolean queryRange(int left, int right)
  . Returns true if every real number in the interval [left, right)
    is currently being tracked, and false otherwise.
- void removeRange(int left, int right)
  . Stops tracking every real number
    currently being tracked in the half-open interval [left, right).
"""

"""
Idea:
- Use segment tree with lazy propagation.
  . Since the size is not fixed (ranges can be added and removed),
    use hashmap for internal data structures ('tree' and 'lazy')
  . Constraint: 1 <= left < right <= 10^9
    -> The root manages [1, 10^9) range
  . Node value = True (tree[node] = True) indicates that
    node tracks all elements in its managed range.
- Update range [qleft, qright]: 
  . add <-> covered=True
    remove <-> covered=False
  . If node's range is completely outside [qleft, qright]
    -> No changes to node subtree
  . If node's range is completely inside [qleft, qright]
    . Set node value to 'covered'
    . Accumulate pending update to propagate to children later.
  . If node's range partially overlaps with [qleft, qright]:
    . Propagate pending updates to children to ensure correct values,
      then update the children.
    . Update node value after updating children: 
      tree[node] = tree[left] AND tree[right]
      (Node tracks all elements in its managed range
       if both children tracks all elements in their managed range)
- Query range [qleft, qright]:
  . Return True if node tracks all items in intersection(managed_range, query_range).
    For the root, intersection(managed_range, query_range) = query_range.
  . If node's range is completely outside [qleft, qright],
    don't contribute to parent's result
    -> Return True (True AND x = x)
  . If node's range is completely inside [qleft, qright],
    return True if node track all elements in its managed range
    -> Return node value.
  . If node's range partially overlaps with [qleft, qright]:
    . Propagate pending updates to children to ensure correct values,
      then query both halves.
    . Combine returned values of children: res = res_left AND res_right
      (Node tracks all elements in managed range overlapping with query range
       if both children tracks all elements in their managed ranges overlapping with query range)

Handle half-open range:
- querying/updating node i and its children:
  . query/update(qleft, qright, left, right, i, ...)
  . query/update(qleft, qright, left=left, right=mid, lci, ...)
  . query/update(qleft, qright, left=mid+1, right=right, rci, ...)
- Normally, nodes manage discrete integers:
  . left child manages [left, ...,  mid]
  . right child manages [mid + 1, ..., right]
- But in this problem, the ranges are continuous.
  To ensure the combined range is continuous:
  . left child manages [left, mid + 1)
  . right child manages [mid + 1, right + 1)
=> 
. If node manages [left, right), pass right-1 as argument to query/update.
. For correct comparson with 'right', if query range is [qleft, qright),
  pass qright-1 as argument to query/update
"""


class SegmentTreeLazy:
    def __init__(self):
        # Value is True if node tracks all numbers in its managed range
        self.tree: dict[int, bool] = {}

        # Store pending updates (updated node but haven't propagated to children)
        self.lazy: dict[int, bool] = {}

    def __lci(self, i: int) -> int:
        return 2 * i + 1

    def __rci(self, i: int) -> int:
        return 2 * i + 2

    def __process_pending(self, i: int):
        """
        Propagate pending updates from node i to its direct children
        (Node i has been updated).
        """
        # no pending updates
        if i not in self.lazy:
            return

        # propagate updates to direct children
        lci = self.__lci(i)
        rci = self.__rci(i)
        self.tree[lci] = self.lazy[i]
        self.tree[rci] = self.lazy[i]
        self.lazy[lci] = self.lazy[i]
        self.lazy[rci] = self.lazy[i]

        # reset pending state for current node
        del self.lazy[i]

    def update_range(
        self, qleft: int, qright: int, covered: bool, left: int, right: int, i: int
    ) -> None:
        """
        Add/remove tracked range to/from node i.
        - covered = True <-> add range.
        - covered = False <-> remove range.

        Notes:
        - Update range: [qleft, qright+1)
        - Node i manages range: [left, right+1).
        """
        # node's managed range is completely outside updated range
        if qright < left or right < qleft:
            return

        # node's managed range is completely inside updated range
        if qleft <= left and right <= qright:
            self.tree[i] = covered
            self.lazy[i] = covered  # propagate to children later
            return

        # === partial overlap ===

        # propagate pending updates to direct children
        self.__process_pending(i)

        # update children
        mid = (left + right) // 2
        lci = self.__lci(i)
        rci = self.__rci(i)
        self.update_range(qleft, qright, covered, left=left, right=mid, i=lci)
        self.update_range(qleft, qright, covered, left=mid + 1, right=right, i=rci)

        # child hasn't tracked any range and
        # update range is outside child's managed range
        if lci not in self.tree:
            self.tree[lci] = False
        if rci not in self.tree:
            self.tree[rci] = False

        # update node after updating children
        self.tree[i] = self.tree[lci] and self.tree[rci]

    def query_range(
        self, qleft: int, qright: int, left: int, right: int, i: int
    ) -> bool:
        """
        Return True if node tracks all items in intersection(managed_range, query_range).
        For the root, intersection(managed_range, query_range) = query_range.

        Notes:
        - Query range: [qleft, qright+1)
        - Node i manages range: [left, right+1).
        """
        # node's managed range is completely outside query range
        # (the root will not fall into this case)
        if qright < left or right < qleft:
            return True  # don't contribute to parent's result

        # node's managed range is completely inside query range
        if qleft <= left and right <= qright:
            if i not in self.tree:
                # node hasn't tracked any range
                self.tree[i] = False

            return self.tree[i]

        # === partial overlap ===

        # propagate pending updates to direct children
        self.__process_pending(i)

        # query both halves
        mid = (left + right) // 2
        left_res = self.query_range(
            qleft, qright, left=left, right=mid, i=self.__lci(i)
        )
        right_res = self.query_range(
            qleft, qright, left=mid + 1, right=right, i=self.__rci(i)
        )

        # aggregate result
        return left_res and right_res


class RangeModule:
    def __init__(self):
        self.st = SegmentTreeLazy()

        # segment tree root's managed range: [MIN, MAX)
        self.MIN = 1
        self.MAX = 10**9

    def addRange(self, left: int, right: int) -> None:
        self.st.update_range(
            qleft=left,
            qright=right - 1,
            covered=True,
            left=self.MIN,
            right=self.MAX - 1,
            i=0,
        )

    def removeRange(self, left: int, right: int) -> None:
        self.st.update_range(
            qleft=left,
            qright=right - 1,
            covered=False,
            left=self.MIN,
            right=self.MAX - 1,
            i=0,
        )

    def queryRange(self, left: int, right: int) -> bool:
        return self.st.query_range(
            qleft=left, qright=right - 1, left=self.MIN, right=self.MAX - 1, i=0
        )


"""
Complexity:
- Number of items = number of [i, i+1) intervals = O(max)
- The segment tree is full and balanced: 
  . height: h = O(log(max))
  . number of nodes: O(4*max) (see proof in segment_tree.md)

1. Time complexity: 
- init: O(1)
- process pending update: O(1)
- update_range: O(log(max))
  . At most 2 nodes per level (2 ends) can have range overlap partially with update range.
    -> At most 4 nodes are processed at each level.
    -> Work across level: O(4*h) = O(log(max))
- query_range: O(log(max)) (similar to update_range)

2. Space complexity: O(max) 
- 'st' (tree & lazy): O(4*max)
- recursion stack: O(h) = O(log(max))
"""
