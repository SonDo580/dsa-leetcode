"""
https://leetcode.com/problems/find-median-from-data-stream/

The median is the middle value in an ordered integer list.
If the size of the list is even, there is no middle value,
and the median is the mean of the two middle values.

For example, for arr = [2,3,4], the median is 3.
For example, for arr = [2,3], the median is (2 + 3) / 2 = 2.5.
Implement the MedianFinder class:

MedianFinder() initializes the MedianFinder object.
void addNum(int num) adds the integer num from the data stream to the data structure.
double findMedian() returns the median of all elements so far. Answers within 10^-5 of the actual answer will be accepted.

Follow up:
- If all integer numbers from the stream are in the range [0, 100], how would you optimize your solution?
- If 99% of all integer numbers from the stream are in the range [0, 100], how would you optimize your solution?
"""

"""
Idea:
- With ordered data, the median is calculated from lesser half's greatest element 
  and greater half's smallest element.
- If there's an odd number of elements, pick from the half with greater size.
- Sorting is not practical since data is continuously added to.
  => Use min/max heap.

Implementation:
- Use a min heap that stores the greater half of the data,
  and a max heap that stores the lesser half of the data.
- If there is an even number of elements,
  the median is the average of the values at the top of both heaps
- If there is an odd number of elements,
  1 heap will have 1 extra element, and it is the median.
  (let's choose max heap arbitrarily)
- When adding to the heaps, make sure to keep the following constraints:
  + the difference between heap's sizes is 0 or 1.
  + all elements in the min heap >= all elements in the max heap.

===== Element adding algorithm =====
1. push 'num' to max heap
2. pop from max heap, and push that element onto min heap
3. After step 2, if min heap has 1 more element than max heap, 
   pop from min heap and push that element onto max heap.  

Explanation:
- ensure that all elements in min heap >= are elements in max heap.
- let the max heap store the extra elements when there is an odd number of elements.
"""

import heapq


class MedianFinder:
    def __init__(self):
        self._min_heap: list[int] = []
        self._max_heap: list[int] = []

    def add_num(self, num: int) -> None:
        heapq.heappush(self._max_heap, -num)
        heapq.heappush(self._min_heap, -heapq.heappop(self._max_heap))
        if len(self._min_heap) > len(self._max_heap):
            heapq.heappush(self._max_heap, -heapq.heappop(self._min_heap))

    def find_median(self) -> float:
        if len(self._max_heap) > len(self._min_heap):
            return -self._max_heap[0]
        return (self._min_heap[0] - self._max_heap[0]) / 2


"""
Complexity:

1. Time complexity:
- add_num: O(log n) (for heap push and pop)
- find_num: O(1)

2. Space complexity: O(n) (for storing the heaps)
"""
