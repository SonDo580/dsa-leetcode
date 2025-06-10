# Given an array of integers nums and an integer k, 
# return the total number of subarrays whose sum equals to k.

# A subarray is a contiguous non-empty sequence of elements within an array.

# Example 1:
# Input: nums = [1,1,1], k = 2
# Output: 2

# Example 2:
# Input: nums = [1,2,3], k = 3
# Output: 2

# Constraints:
# 1 <= nums.length <= 2 * 10^4
# -1000 <= nums[i] <= 1000
# -10^7 <= k <= 10^7


# ===== Implementation =====
# - At any given index i, the prefix sum up to i is 'current'.
#   If there is an index j whose prefix sum is current - k, 
#   the sum of subarray from j + 1 to i is current - (current - k) = k
# - Since there are negative numbers, the same prefix sum can occur multiple times.
#   -> Use a hashmap 'counts' to track how many time a prefix sum has occurred.
# - At every index i, the frequency of current - k is equal to 
#   the number of subarrays whose sum is equal to k that end at i.
# - Special case: Initialize counts[0] = 1 (for the empty prefix [])
#   This is needed because when current == k, the whole subarray from 0 to i should be counted.

def subarray_sum_equals_k(nums: list[int], k: int) -> int:
    counts: dict[int, int] = {}
    counts[0] = 1
    prefix_sum: int = 0
    total: int = 0

    for num in nums:
        prefix_sum += num
        if prefix_sum - k in counts:
            total += counts[prefix_sum - k]

        if prefix_sum not in counts:
            counts[prefix_sum] = 0
        counts[prefix_sum] += 1
    
    return total

# ===== Complexity =====
# Time complexity: O(n) - loop through 'nums'
# Space complexity: O(n) - for 'counts'