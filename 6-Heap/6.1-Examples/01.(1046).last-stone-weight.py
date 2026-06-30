"""
https://leetcode.com/problems/last-stone-weight/

You are given an array of integers 'stones' where stones[i] is the weight of the ith stone.

We are playing a game with the stones.
On each turn, we choose the heaviest two stones and smash them together.
Suppose the heaviest two stones have weights x and y with x <= y.
The result of this smash is:
- If x == y, both stones are destroyed, and
- If x != y, the stone of weight x is destroyed, and the stone of weight y has new weight y - x.

At the end of the game, there is at most one stone left.

Return the weight of the last remaining stone.
If there are no stones left, return 0.
"""

"""
Analysis:
- We need a way to quickly identify the next heaviest stone 
  after removing the heaviest stone.
- If the stones are always destroyed, we can just sort the input array.
  Buf a weight-reduced stone may be added back.
=> Use a max heap.

Implementation:
- Add all stones to max heap.
- In each pass:
  . heappop 2 times to get 2 heaviest stones. 
  . (may) heappush the weight-reduced stone back.
- Note: with heapq, simulate max heap by negating the value. 
"""

import heapq


def last_stone_weight(stones: list[int]) -> int:
    # Simulate a max heap:
    # - negate the values put on the heap
    # - reverse the sign again when popping items
    stones = [-stone for stone in stones]
    heapq.heapify(stones)

    while len(stones) > 1:
        # Get the 2 heaviest stones
        first = -heapq.heappop(stones)
        second = -heapq.heappop(stones)

        # If both stones are not destroyed after the smash,
        # add the weight-reduced stone back to the heap
        weight_diff = abs(first - second)
        if weight_diff > 0:
            heapq.heappush(stones, -weight_diff)

    # Return the weight of the last remaining stone or 0
    return -stones[0] if stones else 0


"""
Complexity:
1. Time complexity: O(n*log(n))
- Heapify: O(n)
- In each iteration, at least 1 stone is destroyed 
  -> at most n - 1 iterations
- In each iteration: 
  . perform 2 pops and possibly 1 push on the heap -> O(log(n))
=> Overall: O(n) + O(n*log(n)) = O(n*log(n))

2. Space complexity: O(1) since we mutate the input 'stones'
   (if modifying input is prohibited, O(n) for the heap)

===== Time complexity (in more details) =====:
- There are at most n - 1 iterations (1 stone is destroyed each time).
  In that case the heap start at size n, and reduced by 1 each time until it reaches 1
- The total cost of heap operations:
  O(log(n)) + O(log(n-1)) + O(log(n-2)) + ... + O(log(2)) + O(log(1))
  = O(log(n * (n-1) * (n-2) * ... * 2 * 1))
  = O(log(n!))
  ~= O(log(sqrt(2*pi*n)) + n*log(n/e))
  ~= O(0.5*log(2*pi) + 0.5*log(n) + n*log(n) - n*log(e))
  ~= O(n*log(n))
Note: n! ~= sqrt(2*pi*n) * (n/e)^n    (Stirling approximation)
"""
