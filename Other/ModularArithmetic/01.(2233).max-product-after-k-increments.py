"""
https://leetcode.com/problems/maximum-product-after-k-increments/

You are given an array of non-negative integers 'nums' and an integer k.
In one operation, you may choose any element from 'nums' and increment it by 1.
Return the maximum product of nums after at most k operations, modulo 10^9 + 7
"""

"""
Analysis:
- Consider any 2 element x and y such that x > y
  . (x + 1) * y = xy + y
  . (y + 1) * x = xy + x
  . Since x > y, the later product is greater
-> We should greedily increment the smallest element at every step.

Implementation:
- Convert 'nums' to a min heap, 
- Repeat k times: pop the min item, increment, push back.
- Multiply the numbers, then apply modulo operation.
- The number can get very large 
  -> should apply modulo operation incrementally
  . x*y mod n = ((x mod n)*y mod n
"""


import heapq


def max_product(nums: list[int], k: int) -> int:
    heapq.heapify(nums)

    for _ in range(k):
        heapq.heappush(nums, heapq.heappop(nums) + 1)

    MOD = 1_000_000_007

    result = 1
    for num in nums:
        result = (result * num) % MOD

    return result


"""
Complexity:
- Let n = len(nums)

1. Time complexity: O(n + k*log(n))
- Heapify 'nums': O(n)
- Heap push/pop k times: O(k*log(n))
- Aggregate result: O(n)

2. Space complexity: O(n) for the heap
"""
