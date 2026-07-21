"""
https://leetcode.com/problems/my-calendar-iii/

A k-booking happens when k events have some non-empty intersection
(i.e., there is some time that is common to all k events.)

You are given some events [startTime, endTime), after each given event,
return an integer k representing the maximum k-booking between all the previous events.

Implement the MyCalendarThree class:
- MyCalendarThree() Initializes the object.
- int book(int startTime, int endTime):
  . Returns an integer k representing the largest integer such that
    there exists a k-booking in the calendar.
"""

"""
Idea:
- Use a segment tree where each node manages a half-open interval
  . We need the combined interval to be continuous:
    -> . left child manages range [0, mid + 1)
       . right child manages range [mid + 1, right) 
    -> . If  node's managed range is [left, right),
         pass 'right-1' as argument to query/update method.
       . If query/update range is [qleft, qright)
         pass 'qright-1' as argument to query/update method
         for correct comparison with 'right-1'.
- Number of items is not known in advance
  -> Use hashmap for internal data structures.
- Use lazy propagation for efficient range update.
- Node's value is the maximum number of events in a single intersection
  in node's managed range.
  -> book's result is root's value after inserting the event.
- Insert event (segment tree's update range):
  . If node's range is outside update range, skip.
  . If node's range is fully contained in update range:
    . New event intersects with all previous events that 
      have part of interval in node's range.
      -> 1 more event to the intersection with the most events
      -> node's val += 1
    . Save pending update to propagate to children later:
      . lazy[i] += 1 
        (Each child also has 1 more event in the intersection with the most events)
  . If node's range partially overlaps with update range:
    . Propagate pending update to children.
    . Update children.
    . Combine result from children:
      . tree[i] = max(tree[lci], tree[rci])
        (The intersection with the most events is managed by 1 child.
         If both children have the same value, pick either one.)
"""

from collections import defaultdict


class SegmentTreeLazy:
    def __init__(self):
        # node's value
        # = maximum number of events in a single intersection in node's range
        self.tree: defaultdict[int, int] = defaultdict(int)  # default = 0

        # lazy[i] = number of events to add to values of children of node i
        self.lazy: defaultdict[int, int] = defaultdict(int)  # default = 0

    def __process_pending(self, i: int) -> None:
        """
        Propagate pending update to direct children of node i
        (Node i has been updated).
        """
        if i not in self.lazy:
            return  # no pending updates

        # propagate update to direct children
        lci = 2 * i + 1
        rci = 2 * i + 2
        inc = self.lazy[i]
        self.tree[lci] += inc
        self.tree[rci] += inc
        self.lazy[lci] += inc
        self.lazy[rci] += inc

        # reset pending state
        del self.lazy[i]

    def update_range(
        self, qleft: int, qright: int, left: int, right: int, i: int
    ) -> None:
        """
        Update segment tree when adding event with interval [qleft, qright+1)
        Node's managed range is [left, right+1).
        """
        # node is outside update range
        if qright < left or right < qleft:
            return

        # node is fully contained in update range
        if qleft <= left and right <= qright:
            self.tree[i] += 1
            self.lazy[i] += 1
            return

        # === partial overlap

        # propagate pending update to children to ensure correct values
        self.__process_pending(i)

        # update children
        mid = (left + right) // 2
        lci = 2 * i + 1
        rci = 2 * i + 2
        self.update_range(qleft, qright, left=left, right=mid, i=lci)
        self.update_range(qleft, qright, left=mid + 1, right=right, i=rci)

        # update node after updating children
        self.tree[i] = max(self.tree[lci], self.tree[rci])

    @property
    def root_val(self) -> int:
        """Maximum number of events in a single intersection."""
        return self.tree[0]


class MyCalendarThree:
    def __init__(self):
        self.st = SegmentTreeLazy()

        # segment tree's root manages range [0, 10**9)
        self.MIN = 0
        self.MAX = 10**9

    def book(self, start_time: int, end_time: int) -> int:
        self.st.update_range(
            qleft=start_time,
            qright=end_time - 1,
            left=self.MIN,
            right=self.MAX - 1,
            i=0,
        )
        return self.st.root_val


"""
Complexity:
- Max number of nodes: O(4*max) = O(max)    (max = 10**9)
- The tree is balanced -> height: h = O(log(max))

1. Time complexity:
- init: O(1)
- book (update_range): O(log(max))
  . O(1) in case node's range is outside or completely inside update range.
  . In case of partial overlap, at most 2 nodes (boundaries) can spawn recursive calls,
    (2 calls for each node)
    -> At most 4 nodes are processed at each level
    -> Work across level: O(4*h) = O(log(max)) 

2. Space complexity: O(max)
- 'st': O(max) for 'tree' and 'lazy' 
- recursion stack: O(h) = O(log(max))
"""
