# Given a sorted integer array arr, two integers k and x,
# return the k closest integers to x in the array.
# The result should also be sorted in ascending order.

# An integer a is closer to x than an integer b if:
# |a - x| < |b - x|, or
# |a - x| == |b - x| and a < b

# Example 1:
# Input: arr = [1,2,3,4,5], k = 4, x = 3
# Output: [1,2,3,4]

# Example 2:
# Input: arr = [1,1,2,3,4,5], k = 4, x = -1
# Output: [1,1,2,3]

# Constraints:
# 1 <= k <= arr.length
# 1 <= arr.length <= 10^4
# arr is sorted in ascending order.
# -10^4 <= arr[i], x <= 10^4

import heapq


def k_closest_elements(arr: list[int], k: int, x: int) -> list[int]:
    heap = []

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


# ===== Complexity =====
# Time complexity:
# - n iterations:
#   + heap operations: O(log(k))
# - extract elements from heap: O(k)
# - sort the results: O(k(log(k)))
# => overall: O((n + k)*log(k))
#
# Space complexity:
# - heap: O(k)
# - result list: O(k)
# - sorting: O(k)
# => overall: O(k)


# ===== A more efficient approach =====
# - if x is not in the range of arr, slice the first or last k elements 
# - since the array are sorted, we can use binary search to find x,
#   then expand to both ends until k elements are collected.
#   + if x is found at i: include it in result and start searching from i - 1 and i + 1
#   + if x is not found: start collecting from the 2 closest elements
#
# Time complexity:
# - binary search: O(log(n))
# - expansion: O(k)
# - sorting: O(k*log(k))
# => overall: O(log(n) + k*log(k))
#
# Space complexity: 
# - result list: O(k)
# - sorting: O(k)
# => overall: O(k)


def k_closest_elements(arr: list[int], k: int, x: int) -> list[int]:
    if x > arr[len(arr) - 1]:
        return arr[-k:]
    if x < arr[0]:
        return arr[:k]

    result = []
    index, back_ptr, forth_ptr = _binary_search(arr, x)
    if index != -1:
        result.append(x)
        back_ptr = index - 1
        forth_ptr = index + 1

    while back_ptr >= 0 and forth_ptr < len(arr) and len(result) < k:
        if abs(arr[back_ptr] - x) < abs(arr[forth_ptr] - x):
            result.append(arr[back_ptr])
            back_ptr -= 1
        elif abs(arr[back_ptr] - x) > abs(arr[forth_ptr] - x):
            result.append(arr[forth_ptr])
            forth_ptr += 1
        else:
            # use the smaller element if distances are the same
            result.append(arr[back_ptr])  
            back_ptr -= 1

    # Handle reaching boundary on 1 side
    while back_ptr >= 0 and len(result) < k:
        result.append(arr[back_ptr])  
        back_ptr -= 1
    while forth_ptr < len(arr) and len(result) < k:
        result.append(arr[forth_ptr])
        forth_ptr += 1

    return sorted(result)

def _binary_search(arr: list[int], target: int) -> tuple[int, int, int] :
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