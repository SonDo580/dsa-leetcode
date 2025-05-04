# The median is the middle value in an ordered integer list.
# If the size of the list is even, there is no middle value,
# and the median is the mean of the two middle values.

# For example, for arr = [2,3,4], the median is 3.
# For example, for arr = [2,3], the median is (2 + 3) / 2 = 2.5.
# Implement the MedianFinder class:

# MedianFinder() initializes the MedianFinder object.
# void addNum(int num) adds the integer num from the data stream to the data structure.
# double findMedian() returns the median of all elements so far. Answers within 10-5 of the actual answer will be accepted.

# Example 1:
# Input:
# ["MedianFinder", "addNum", "addNum", "findMedian", "addNum", "findMedian"]
# [[], [1], [2], [], [3], []]
#
# Output:
# [null, null, null, 1.5, null, 2.0]
#
# Explanation:
# MedianFinder medianFinder = new MedianFinder();
# medianFinder.addNum(1);    // arr = [1]
# medianFinder.addNum(2);    // arr = [1, 2]
# medianFinder.findMedian(); // return 1.5 (i.e., (1 + 2) / 2)
# medianFinder.addNum(3);    // arr[1, 2, 3]
# medianFinder.findMedian(); // return 2.0

# Constraints:
# -10^5 <= num <= 10^5
# There will be at least one element in the data structure before calling findMedian.
# At most 5 * 10^4 calls will be made to addNum and findMedian.

# Follow up:
# - If all integer numbers from the stream are in the range [0, 100], how would you optimize your solution?
# - If 99% of all integer numbers from the stream are in the range [0, 100], how would you optimize your solution?


# ===== Problem summary =====
# Find the middle element in a dataset that is continuously added to

# ===== Strategy =====
# - Use a min heap that stores the greater half of the data,
#   and a max heap that stores the lesser half of the data.
# - If there is an even number of elements,
#   the median is the average of the values at the top of both heaps
# - If there is an odd number of elements,
#   1 heap will have 1 extra element, and it is the median.
#   (let's choose max heap arbitrarily)
# - When adding to the heaps, make sure to keep the following constraints:
#   + the difference between heap's sizes stay the same or within 1.
#   + all elements in the min heap >= all elements in the max heap.

# ===== Element adding algorithm =====
# 1. push 'num' to max heap
# 2. pop from max heap, and push that element onto min heap
# 3. After step 2, if min heap has more element than max heap, 
#    pop from min heap and push that element onto max heap.  
# 
# Explanation:
# - Step 2: ensure that all elements in min heap >= are elements in max heap.
# - Step 3: let the max heap store the extra elements when there is an odd number of elements.

# Note: simulate a max heap by negating the values (since 'heapq' implements min heap)

import heapq


class MedianFinder:
    def __init__(self):
        self._min_heap = []
        self._max_heap = []

    def add_num(self, num: int) -> None:
        heapq.heappush(self._max_heap, -num)
        heapq.heappush(self._min_heap, -heapq.heappop(self._max_heap))
        if len(self._min_heap) > len(self._max_heap):
            heapq.heappush(self._max_heap, -heapq.heappop(self._min_heap))

    def find_median(self) -> float:
        if len(self._max_heap) > len(self._min_heap):
            return -self._max_heap[0]
        return (self._min_heap[0] - self._max_heap[0]) / 2


# ===== Complexity =====
# Time complexity:
# - add_num: O(log n) (for heap push and pop)
# - find_num: O(1)
#
# Space complexity: O(n) (for storing the heaps)
