"""
https://leetcode.com/problems/remove-stones-to-minimize-the-total/

You are given a 0-indexed integer array 'piles',
where piles[i] represents the number of stones in the ith pile,
and an integer k. You should apply the following operation exactly k times:

Choose any piles[i] and remove floor(piles[i] / 2) stones from it.
Notice that you can apply the operation on the same pile more than once.

Return the minimum possible total number of stones remaining after applying the k operations.
"""

"""
Analysis:
- To have the minimum number of stones remaining, 
  we should remove as much stones as possible at each step
  -> Select the pile with the most number of stones at each step
- Number of stones in a pile change after each operation.
  -> Sorting is not efficient since we have to reinsert updated item
     (binary search is O(log(n)), but shifting is O(n)).
  -> Use a max heap.
"""

import heapq


def min_stones(piles: list[int], k: int) -> int:
    # Simulate a max heap by negating the values
    piles = [-pile for pile in piles]
    heapq.heapify(piles)

    # Iterate k times
    for _ in range(k):
        # Retrieve the pile with the most number of stones
        max_pile = -heapq.heappop(piles)

        # Remove half of the stones from that pile
        heapq.heappush(piles, -(max_pile - max_pile // 2))

    # Return the total number of stones left
    return -sum(piles)


"""
Complexity:

1. Time complexity: O(n + k*log(n))
- heapify 'piles': O(n)
- k iterations:
  . heap push and pop: O(log(n))
- sum over remaining 'piles': O(n)

2. Space complexity: O(1) (reassign and mutate 'piles')
   (if mutating is now allowed: O(n) for the heap)
"""