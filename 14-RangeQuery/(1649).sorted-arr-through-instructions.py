"""
https://leetcode.com/problems/create-sorted-array-through-instructions/

Given an integer array 'instructions',
you are asked to create a sorted array from the elements in instructions.
You start with an empty container 'nums'.
For each element from left to right in instructions, insert it into 'nums'.

The cost of each insertion is the minimum of the following:
- The number of elements currently in nums that are strictly less than instructions[i].
- The number of elements currently in nums that are strictly greater than instructions[i].

For example, if inserting element 3 into nums = [1,2,3,5],
the cost of insertion is min(2, 1) (elements 1 and 2 are less than 3, element 5 is greater than 3)
and 'nums' will become [1,2,3,3,5].

Return the total cost to insert all elements from instructions into 'nums'.
Since the answer may be large, return it modulo 10^9 + 7
"""

# === Approach 1: Insert incrementally + binary search ===
"""
- Keep 'nums' in sorted order.
- For an item x (an instruction):
  . Use bisect left to find smallest i such that nums[i] >= x
    -> number of smaller items = i
  . Use bisect right to find smallest j such that nums[j] > x
    (j = len(nums) <-> x > all items in 'nums')
    -> number of greater items = len(nums) - j
  . Insert x into 'nums' at j
    (may reduce shifting compared to inserting at i, same time complexity)
"""

from bisect import bisect_left, bisect_right


class Solution:
    def createSortedArray(self, instructions: list[int]) -> int:
        nums: list[int] = []
        cost: int = 0

        for x in instructions:
            i = bisect_left(nums, x)
            j = bisect_right(nums, x)
            smaller_cnt = i
            greater_cnt = len(nums) - j
            cost += min(smaller_cnt, greater_cnt)

            nums.insert(j, x)

        return cost % 1_000_000_007


"""
Complexity:
- Let n = len(instructions)
      l = len(nums) (0 -> 1 -> ... -> n)

1. Time complexity: O(n^2)
- Work in each iteration: O(l)
  . bisect left/right: O(log(l))
  . insert: O(l)
-> For n iterations:
  . T = sum(O(l) for l in [0..n-1]) = O(n^2)

2. Space complexity: O(n) for 'nums'
"""


# === Approach 2: Array to count items per rank ===
# (exceed time limit)
"""
- Produce 'ranks' array (same as approach 2).
- Find number of smaller items for each item (rank of each item).
  Equal items will have the same rank:
  . Produce final 'nums' = sorted(instructions)
  . For each item in 'instructions',
    find smallest i such that nums[i] >= x (bisect left / lower bound)
    -> i = rank of x
- Use 'count' array to count number of inserted items for each rank.
- When inserting an item of rank 'rank':
  . smaller_count = sum(count[i] for i in [0..rank-1])
  . greater_count = sum(count[i] for i in [rank+1..max_rank])
"""


def _produce_ranks(instructions: list[int]) -> tuple[list[int], int]:
    """Return rank of each number and max rank."""
    nums = sorted(instructions)
    ranks: list[int] = []
    max_rank = -1

    for x in instructions:
        idx = bisect_left(nums, x)
        max_rank = max(max_rank, idx)
        ranks.append(idx)

    return ranks, max_rank


class Solution:
    def createSortedArray(self, instructions: list[int]) -> int:
        ranks, max_rank = _produce_ranks(instructions)
        count = [0] * (max_rank + 1)  # number of items per rank
        cost: int = 0

        for i in range(len(instructions)):
            rank = ranks[i]
            smaller_cnt = sum(count[i] for i in range(0, rank))
            greater_cnt = sum(count[i] for i in range(rank + 1, max_rank + 1))
            cost += min(smaller_cnt, greater_cnt)
            count[rank] += 1

        return cost

"""
Complexity:
- Let n = len(instructions)
  -> max_rank = O(n) (worst case: all numbers are unique)

1. Time complexity: O(n*log(n) + n^2) = O(n^2)
- Produce 'ranks': O(n*log(n))
  . sort array: O(n*log(n))
  . bisect left for n items: O(n*log(n))
- Iterate over 'count' for each instruction: O(n)
  -> For n instructions: O(n^2)

2. Space complexity: O(n)
- (sorted) 'nums': O(n)
- 'ranks': O(n)
- 'count': O(n)
"""


# === Approach 3: Segment tree ===
# (optimize counting items per rank)
"""
Idea:
- Produce 'ranks' array (same as approach 2)
- Use a segment tree with the root manages the whole range of ranks.
  . node's value is number of items with rank in node's managed range
    -> node's value = left_child's value + right_child's value.
- Iterate through original instructions:
  . For each item x with rank 'rank', query how many items have been 
    inserted into range [0, rank-1] and range [rank+1, max_rank] 
    (number of smaller/greater items inserted)
  . Calculate cost = min(smaller_count, greater_count)
  . Update segment tree to reflect that x has been inserted
    . increase number of items with rank = 'rank'. 
"""


class SegmentTree:
    def __init__(self, max_rank: int):
        # - nodes manage range of ranks
        # - node's value = number of inserted items with rank in node's managed range
        self.tree = [0] * 4 * (max_rank + 1)  # rank is 0-indexed

    def update(self, rank: int, left: int, right: int, i: int) -> None:
        """Update when inserting an item with rank 'rank'."""
        if left == right:  # reached leaf node
            self.tree[i] += 1
            return

        mid = (left + right) // 2
        lci = 2 * i + 1
        rci = 2 * i + 2

        if rank <= mid:  # target is in left subtree
            self.update(rank, left, mid, lci)
        else:  # target is in right subtree
            self.update(rank, mid + 1, right, rci)

        # update node after updating child
        self.tree[i] = self.tree[lci] + self.tree[rci]

    def query_range(
        self, qleft: int, qright: int, left: int, right: int, i: int
    ) -> int:
        """Return number of inserted items with rank in [qleft..qright]."""
        if qleft > qright:
            # querying smaller_count for min rank or greater_count for max rank
            return 0

        # node's range is outside query range
        if qright < left or right < qleft:
            return 0

        # node's range is completely inside query range
        # -> return precomputed value
        if qleft <= left and right <= qright:
            return self.tree[i]

        # partial overlap -> query both halves then aggregate
        mid = (left + right) // 2
        left_res = self.query_range(qleft, qright, left, mid, 2 * i + 1)
        right_res = self.query_range(qleft, qright, mid + 1, right, 2 * i + 2)
        return left_res + right_res


class Solution:
    def createSortedArray(self, instructions: list[int]) -> int:
        ranks, max_rank = _produce_ranks(instructions)
        st = SegmentTree(max_rank)
        cost: int = 0

        for i in range(len(instructions)):
            rank = ranks[i]
            smaller_cnt = st.query_range(
                qleft=0, qright=rank - 1, left=0, right=max_rank, i=0
            )
            greater_cnt = st.query_range(
                qleft=rank + 1, qright=max_rank, left=0, right=max_rank, i=0
            )
            cost += min(smaller_cnt, greater_cnt)
            st.update(rank, left=0, right=max_rank, i=0)

        return cost % 1_000_000_007


"""
Complexity:
- Let n = len(instructions)
  -> max_rank = O(n) (worst case: all numbers are unique)
- Segment tree is full and balanced
  -> . number of nodes: O(4*n)
     . height: h = O(log(4*n)) = O(n)

1. Time complexity:
- Produce 'ranks': O(n*log(n))
  . sort array: O(n*log(n))
  . bisect left for n items: O(n*log(n))
- Init 'st': O(4*n) = O(n)
- Perform st.query and st.update for n numbers: O(n*log(n))
  . st.update: O(h) = O(log(n))
    . Each update follow exactly 1 path from root to a leaf
  . st.query: O(log(n))
    . At most 2 nodes per level can spawn extra calls, 2 calls per node
      (Only boundaries can overlap partially with query range)
      -> At most 4 nodes are processed at each level.
      -> Work across levels: O(4*h) = O(log(n)) 

2. Space complexity: O(n)
- (sorted) 'nums': O(n)
- 'ranks': O(n)
- 'st': O(n)
- recursion stack: O(h) = O(log(n))
"""
