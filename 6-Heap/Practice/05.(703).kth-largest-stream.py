"""
https://leetcode.com/problems/kth-largest-element-in-a-stream/

You are part of a university admissions office and need to keep track of
the kth highest test score from applicants in real-time.
This helps to determine cut-off marks for interviews and
admissions dynamically as new applicants submit their scores.

You are tasked to implement a class which, for a given integer k,
maintains a stream of test scores and continuously returns
the kth highest test score after a new score has been submitted.
More specifically, we are looking for the kth highest score
in the sorted list of all scores.

Implement the KthLargest class:
. KthLargest(int k, int[] nums) Initializes the object with
  the integer k and the stream of test scores nums.
. int add(int val) Adds a new test score val to the stream
  and returns the element representing the kth largest element
  in the pool of test scores so far.
"""

"""
Idea:
- Data arrive constantly 
  -> Sorting is not efficient
     (inserting a new item takes O(log(n)) + O(n) = O(n) 
     for binary search and shifting).
  -> Use a heap.
      
Implementation:
- Keep adding elements to a min heap.
- Pop the smallest element when the heap size exceed k.
- The smallest element in the heap is the kth largest element of the stream.
"""

from heapq import heappush, heappop


class KthLargest:
    def __init__(self, k: int, nums: list[int]):
        self.k = k
        self.heap: list[int] = []
        for num in nums:
            self.add(num)

    def add(self, val: int) -> int:
        heappush(self.heap, val)
        if len(self.heap) > self.k:
            heappop(self.heap)
        return self.heap[0]


"""
Complexity:
- Let n = len(nums)

1. Time complexity:
- 'add' method: O(log(k))
- '__init__' method: O(n*log(k))

2. Space complexity: O(k) for the heap
"""
