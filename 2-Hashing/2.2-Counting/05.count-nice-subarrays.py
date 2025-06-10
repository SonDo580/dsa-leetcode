# Given an array of integers nums and an integer k. 
# A continuous subarray is called nice if there are k odd numbers on it.
# Return the number of nice sub-arrays.

# Example 1:
# Input: nums = [1,1,2,1,1], k = 3
# Output: 2
# Explanation: The only sub-arrays with 3 odd numbers are [1,1,2,1] and [1,2,1,1].

# Example 2:
# Input: nums = [2,4,6], k = 1
# Output: 0
# Explanation: There are no odd numbers in the array.

# Example 3:
# Input: nums = [2,2,2,1,2,2,1,2,2,2], k = 2
# Output: 16

# Constraints:
# 1 <= nums.length <= 50000
# 1 <= nums[i] <= 10^5
# 1 <= k <= nums.length


# ===== Note =====
# - This problem is similar to '04.subarray-sum-equals-k'.
# - Instead of tracking prefix sum, we track number of odd numbers upto an index.
# - We also have the special case for the empty prefix (similar reasoning)

def nice_subarray_count(nums: list[int], k: int) -> int:
    counts: dict[int, int] = {}
    counts[0] = 1 
    odd_count = 0
    total = 0

    for num in nums:
        odd_count += num % 2
        if odd_count - k in counts:
            total += counts[odd_count - k]

        if odd_count not in counts:
            counts[odd_count] = 0
        counts[odd_count] += 1
    
    return total

# ===== Complexity =====
# Time complexity: O(n) - loop through 'nums'
# Space complexity: O(n) - for 'counts'