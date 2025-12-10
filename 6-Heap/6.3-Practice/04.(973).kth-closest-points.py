"""
https://leetcode.com/problems/k-closest-points-to-origin/

Given an array of points where points[i] = [xi, yi]
represents a point on the X-Y plane and an integer k,
return the k closest points to the origin (0, 0).

The distance between two points on the X-Y plane is the Euclidean distance (i.e., √(x1 - x2)2 + (y1 - y2)2).

You may return the answer in any order.
The answer is guaranteed to be unique (except for the order that it is in).
"""

# ===== Approach 1: Max Heap =====
# ================================
"""
- Add the points and corresponding distances to a max heap
  (simulate a max heap with heapq by negating the distance)
- When the heap size exceeds k, remove the item with greatest distance.
- Extract the points from the heap in the end.
"""

import heapq


def k_closest_points(points: list[list[int]], k: int) -> list[list[int]]:
    heap = []

    for point in points:
        x, y = point
        distance_squared = x**2 + y**2

        heapq.heappush(heap, (-distance_squared, point))
        if len(heap) > k:
            heapq.heappop(heap)

    return [point for _, point in heap]


"""
Complexity:

1. Time complexity:
- n iterations, heap operations in each iteration costs O(log(k))
- Extract points from final heap: O(k)
=> Overall: O(n*log(k) + k)

2. Space Complexity: O(k) for the heap
"""

# ===== Approach 2: Quick Select =====
# ====================================
# (see Sorting section)