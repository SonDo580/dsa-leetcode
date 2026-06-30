"""
https://leetcode.com/problems/minimum-operations-to-halve-array-sum/

You are given an array 'nums' of positive integers.
In one operation, you can choose any number from 'nums' and reduce it to exactly half the number.
(Note that you may choose this reduced number in future operations.)

Return the minimum number of operations to reduce the sum of nums by at least half.
"""

"""
Strategy:
- To minimize the number of operations, we need to maximize the amount reduced in each step
  -> Always halve the largest item in each iteration.
- Sorting is not efficient since the halved item can be added back.
  -> Use a max heap.
"""

import heapq


def halve_array_sum(nums: list[int]) -> int:
    current_sum: float = sum(nums)
    target_sum: float = current_sum / 2

    # simulate a max heap by negating the values
    heap: list[float] = [-num for num in nums]
    heapq.heapify(heap)

    operation_count: int = 0
    while current_sum > target_sum:
        max_num: int = heapq.heappop(heap)  # item with maximum absolute value
        current_sum += max_num / 2  # reduced the sum (max_num is negative)
        heapq.heappush(heap, max_num / 2)  # push the halved item back
        operation_count += 1

    return operation_count


"""
Complexity:
- Let n = len(nums).

1. Time complexity: O(n*log(n))
- Sum all items in 'nums': O(n)
- Heapify 'nums': O(n)
- Number of operations: O(n)
  In each iteration:
  . heappush and heappop: O(log(n))
=> Overall: O(n) + O(n) + O(n*log(n)) = O(n*log(n))

2. Space complexity: O(n) for the heap
"""
