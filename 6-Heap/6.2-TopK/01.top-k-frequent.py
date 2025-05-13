# Given an integer array nums and an integer k, 
# return the k most frequent elements. 
# You may return the answer in any order.

# Example 1:
# Input: nums = [1,1,1,2,2,3], k = 2
# Output: [1,2]

# Example 2:
# Input: nums = [1], k = 1
# Output: [1]

# Constraints:
# 1 <= nums.length <= 10^5
# -10^4 <= nums[i] <= 10^4
# k is in the range [1, the number of unique elements in the array].
# It is guaranteed that the answer is unique.
 
# Follow up: Your algorithm's time complexity must be better than O(n log n),
# where n is the array's size.

from collections import Counter
import heapq

def top_k_frequent(nums: list[int], k: int) -> list[int]:
    frequency_dict = Counter(nums)
    heap = []

    for num, freq in frequency_dict.items():
        # push the tuple (frequency, num)
        heapq.heappush(heap, (freq, num)) 

        # pop item with min frequency when heap size exceed k
        if len(heap) > k:
            heapq.heappop(heap) 
    
    return [item[1] for item in heap]

# ===== Complexity =====
# Time complexity:
# - Create frequency dictionary: O(n)
# - At most n iteration:
#   + heap operations: O(log(k)) (max heap size is k)
# => overall: O(n*log(k))
# 
# Space complexity:
# - frequency dictionary: O(n)
# - heap: O(k)
# => overall: O(n + k)

