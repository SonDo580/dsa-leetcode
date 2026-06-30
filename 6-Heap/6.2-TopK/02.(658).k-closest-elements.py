"""
https://leetcode.com/problems/find-k-closest-elements/

Given a sorted integer array 'arr' (ascending), two integers k and x,
return the k closest integers to x in the array.
The result should also be sorted in ascending order.

An integer a is closer to x than an integer b if:
|a - x| < |b - x|, or           (smaller distance)
|a - x| == |b - x| and a < b    (smaller integer if distances are equal)
"""

"""
Idea:
- Add items in 'arr' to a max heap (by distance to x).
- When the heap size exceeds k, pop the item with largest distance to x.
- In the end, the k closest items to x remain on the heap.
"""

import heapq


def k_closest_elements(arr: list[int], k: int, x: int) -> list[int]:
    heap: list[tuple[int, int]] = []

    for num in arr:
        # compute the distance
        distance = abs(x - num)

        # negate the values to simulate a max heap
        heapq.heappush(heap, (-distance, -num))

        # pop 1 item when the heap size exceed k
        # - pop item with largest distance first
        # - if distances are the same, pop largest number
        if len(heap) > k:
            heapq.heappop(heap)

    return sorted([-item[1] for item in heap])


"""
Complexity:
- Let n = len(arr)

1. Time complexity:
- n iterations:
  . heap operations: O(log(k))
- extract elements from heap: O(k)
- sort the results: O(k*log(k))
=> Overall: O((n + k)*log(k))

Space complexity:
- heap: O(k)
- sorting results: O(k) (timsort)
=> Overall: O(k)
"""


# === Alternative approach: binary search & expand =====
"""
- If x is not in the range of arr, slice the first or last k elements
  (compare x with 1st and last element to decide).
- Since the array are sorted, we can use binary search to find x,
  then expand to both ends until k elements are collected.
  + If x is found at i: include it in result and start searching from i - 1 and i + 1.
  + If x is not found: start collecting from the 2 closest elements.
"""


def k_closest_elements(arr: list[int], k: int, x: int) -> list[int]:
    if x > arr[len(arr) - 1]:
        return arr[-k:]
    if x < arr[0]:
        return arr[:k]

    result: list[int] = []
    index, back_ptr, forth_ptr = _binary_search(arr, x)
    if index != -1:
        result.append(x)
        back_ptr = index - 1
        forth_ptr = index + 1

    while back_ptr >= 0 and forth_ptr < len(arr) and len(result) < k:
        if abs(arr[back_ptr] - x) <= abs(arr[forth_ptr] - x):
            # use the smaller element if distances are the same
            result.append(arr[back_ptr])
            back_ptr -= 1
        else:
            result.append(arr[forth_ptr])
            forth_ptr += 1

    # Handle reaching boundary on 1 side (prioritize smaller side)
    while back_ptr >= 0 and len(result) < k:
        result.append(arr[back_ptr])
        back_ptr -= 1
    while forth_ptr < len(arr) and len(result) < k:
        result.append(arr[forth_ptr])
        forth_ptr += 1

    # result is currently in ascending order of distance_to_x
    # -> sort to be in ascending order of value
    return sorted(result)


def _binary_search(arr: list[int], target: int) -> tuple[int, int, int]:
    """
    If target is found, return its index in 1st slot.
    Otherwise, return indices of 2 closest elements in 2nd and 3rd slots.
    """
    left = 0
    right = len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        current = arr[mid]
        if current == target:
            return mid, -1, -1
        if current > target:
            right = mid - 1
        else:
            left = mid + 1
    return -1, right, left


"""
Complexity:

1. Time complexity:
- Binary search for x: O(log(n))
- Expansion: O(k)
- Sort output: O(k*log(k))
=> Overall: O(log(n) + k*log(k))

2. Space complexity: O(k) for sorting output (timsort)
"""
