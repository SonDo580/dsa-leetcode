"""
https://leetcode.com/problems/minimum-cost-to-connect-sticks/

You have some number of sticks with positive integer lengths.
These lengths are given as an array 'sticks',
where sticks[i] is the length of the ith stick.

You can connect any two sticks of lengths x and y into one stick by paying a cost of x + y.
You must connect all the sticks until there is only one stick remaining.

Return the minimum cost of connecting all the given sticks into one stick in this way.
"""

"""
Analysis:
- The sticks that are used earlier in the process will contribute more to the overall cost
  -> At every steps, we should combine the 2 shortest sticks.
- Sorting is not efficient since we have to reinsert the combined stick
  into correct position (binary search is O(log(n)), but shifting is O(n))
  -> Use a min heap.
"""

import heapq


def connect_sticks(sticks: list[str]) -> int:
    if len(sticks) == 1:
        return 0

    heapq.heapify(sticks)
    cost = 0

    while len(sticks) > 1:
        first = heapq.heappop(sticks)
        second = heapq.heappop(sticks)
        new_stick = first + second
        cost += new_stick
        heapq.heappush(sticks, new_stick)

    return cost


"""
Complexity:
- Let n = len(sticks)

1. Time complexity:
- heapify sticks: O(n)
- n - 1 iterations:
  + heap pop: 2*O(log(n))
  + heap push: O(log(n))
=> Overall: O(n*log(n))

2. Space complexity: O(1) (modify 'sticks' in-place)
  (if mutating is prohibited: O(n) for the heap)
"""
