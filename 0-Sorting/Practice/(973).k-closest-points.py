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
# (see Heap section)


# ===== Approach 2: Quick Select =====
# ====================================
"""
- Randomly choose a pivot.
- Partitions 'points' into 3 portions
  . distance_x < distance_pivot -> go to 'left'.
  . distance_x == distance_pivot -> go to 'mid'.
  . distance_x > distance_pivot -> go to 'right'.
- Check 3 cases:
  . k < len(left)
    -> the kth closest points is in 'left'
    -> recurse on 'left' with the same k.
  . k <= len(left) + len(mid)
    -> the kth closest points is 'left' + 'mid'
       (slice the 'mid' array if needed, prioritize closer points in 'left')
  . otherwise:
    -> the kth closest points include 'left' + 'mid' and some in 'right'
    -> recurse on 'right' with k = k - (len(left) + len(mid))
- Space-optimized:
  . Rearrange 'points' in-place instead of creating 3 extra arrays.
  . Iteratively reduce the search space without recursion.
"""

import random


def k_closest(points: list[list[int]], k: int) -> list[list[int]]:
    return quick_select(points, k, start=0, end=len(points) - 1)


def quick_select(
    points: tuple[int, int], k: int, start: int, end: int
) -> list[tuple[int, int]]:
    while start <= end:
        pivot = points[random.randint(start, end)]
        pivot_distance_squared = _get_distance_squared(pivot)

        # Push points with distance < pivot_distance to left
        mid_start = start
        for i in range(start, end + 1):
            if _get_distance_squared(points[i]) < pivot_distance_squared:
                points[mid_start], points[i] = points[i], points[mid_start]
                mid_start += 1

        # Push points with distance > pivot_distance to right
        mid_end = end
        for i in range(end, mid_start - 1, -1):
            if _get_distance_squared(points[i]) > pivot_distance_squared:
                points[mid_end], points[i] = points[i], points[mid_end]
                mid_end -= 1

        # Search all k points in 'left'
        if k < mid_start - start:
            end = mid_start - 1

        # Result = all points in 'left' + some/all points in 'mid'
        elif k <= mid_end - start + 1:
            return points[start : start + k]

        # Search remaining points in 'right'
        # (all points in 'left' and 'mid' are in result)
        else:
            k -= mid_end - start + 1
            start = mid_end + 1


def _get_distance_squared(point: tuple[int, int]) -> int:
    x, y = point
    return x**2 + y**2


"""
Complexity:

1. Time complexity:
- We process only 1 partition in each iteration.
  + Average case: (balanced partition)
    . T = n + n / 2 + n / 4 + ...
  + Worst case: pivot is always the smallest/largest element
    . T = n + (n - 1) + (n - 2) + ...
=> Overall:
   . Average case: O(n)
   . Worst case: O(n^2)

2. Space Complexity: O(1)
"""
