# Given an integer array nums and an integer k,
# return the kth largest element in the array.
# Note that it is the kth largest element in the sorted order,
# not the kth distinct element.
# Can you solve it without sorting?

# Example 1:
# Input: nums = [3,2,1,5,6,4], k = 2
# Output: 5

# Example 2:
# Input: nums = [3,2,3,1,2,4,5,5,6], k = 4
# Output: 4

# Constraints:
# 1 <= k <= nums.length <= 10^5
# -10^4 <= nums[i] <= 10^4

# ===== Implementation =====
# - Keep adding numbers to a min heap
# - When the heap size exceed k, pop the smallest element
# - Return the min element in the heap at the end

import heapq


def find_kth_largest(nums: list[int], k: int) -> int:
    heap = []

    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k:
            heapq.heappop(heap)

    return heap[0]


# ===== Complexity =====
# Time complexity:
# - n iterations:
#   + heap operations: O(log(k)) (heap size is at most k)
# => overall: O(n*log(k))
#
# Space complexity: O(k) for the heap
