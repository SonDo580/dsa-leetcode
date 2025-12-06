"""
https://leetcode.com/problems/kth-largest-element-in-an-array

Given an integer array nums and an integer k,
return the kth largest element in the array.
Note that it is the kth largest element in the sorted order,
not the kth distinct element.
Can you solve it without sorting?
"""

# ========== Approach 1: Min Heap ==========
# ==========================================
"""
- Keep adding elements to a min heap.
- When the heap size exceed k, pop the smallest element.
- Return the min element in the heap at the end.
"""

import heapq


def find_kth_largest(nums: list[int], k: int) -> int:
    heap = []

    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k:
            heapq.heappop(heap)

    return heap[0]


"""
Complexity:

1. Time complexity:
- n iterations, heap operations in each iteration take O(log(k)) 
=> Overall: O(n * log(k))

2. Space complexity: O(k) for the heap
"""


# ========== Approach 2: Max Heap ==========
# ==========================================
"""
- Convert 'nums' to a heap.
- Pop k - 1 elements from the max heap.
- Return the max element in the heap at the end.
- Python's 'heapq' implements a min heap. 
  -> negate the values to simulate a max heap.
"""


def find_kth_largest(nums: list[int], k: int) -> int:
    heap = nums
    for i in range(len(heap)):
        heap[i] = -heap[i]
    heapq.heapify(heap)

    for i in range(k - 1):
        heapq.heappop(heap)
    return -heap[0]


"""
Complexity:

1. Time complexity:
- heapify 'nums': O(n)
- heappop k times takes O(k * log(n)) 
=> Overall: O(n + k * log(n))

2. Space complexity: O(1) (rearrange 'nums' in-place)
"""


# ========== Approach 3: Quick Select ==========
# ==============================================
# (see Sorting section)
