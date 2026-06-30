"""
https://leetcode.com/problems/k-closest-points-to-origin/

Given an array of points where points[i] = [xi, yi]
represents a point on the X-Y plane and an integer k,
return the k closest points to the origin (0, 0).

The distance between two points on the X-Y plane is the Euclidean distance (i.e., √(x1 - x2)2 + (y1 - y2)2).

You may return the answer in any order.
The answer is guaranteed to be unique (except for the order that it is in).
"""

# ===== Approach 1.1: Max Heap =====
# ==================================
"""
- Add the points and corresponding distances to a max heap
  (simulate a max heap with heapq by negating the distance)
- When the heap size exceeds k, remove the item with greatest distance.
- Extract the points from the heap in the end.
"""

import heapq


def k_closest_points(points: list[list[int]], k: int) -> list[list[int]]:
    heap: list[tuple[int, list[int]]] = []  # max heap

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


# ===== Approach 1.2: Min Heap =====
# ==================================
"""
- Add all points and corresponding distances to a min heap
- Pop k smallest-distance items from the heap and add to result.
"""


def k_closest_points(points: list[list[int]], k: int) -> list[list[int]]:
    heap: list[tuple[int, list[int]]] = []  # min heap

    for point in points:
        x, y = point
        distance_squared = x**2 + y**2
        heapq.heappush(heap, (distance_squared, point))

    ans: list[list[int]] = []
    for _ in range(k):
        ans.append(heapq.heappop(heap)[1])

    return ans


"""
Complexity:

1. Time complexity:
- Add n items to min heap: O(n * log(n))
- Pop k items from min heap: O(k * log(n))
=> Overall: O((n + k)*log(n))

2. Space Complexity: O(n) for the heap
"""


# ===== Approach 2: Quick Select =====
# ====================================
# (see Sorting section)
