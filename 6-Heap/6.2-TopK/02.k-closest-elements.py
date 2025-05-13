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

def k_closest_elements(arr: list[int], k:int, x:int) -> list[int]:
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