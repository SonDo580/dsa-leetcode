# Given a binary array nums,
# return the maximum length of a contiguous subarray with an equal number of 0 and 1.

# Example 1:
# Input: nums = [0,1]
# Output: 2
# Explanation: [0, 1] is the longest contiguous subarray with an equal number of 0 and 1.

# Example 2:
# Input: nums = [0,1,0]
# Output: 2
# Explanation: [0, 1] (or [1, 0]) is a longest contiguous subarray with equal number of 0 and 1.

# Example 3:
# Input: nums = [0,1,1,1,1,1,0,0,0]
# Output: 6
# Explanation: [1,1,1,0,0,0] is the longest contiguous subarray with equal number of 0 and 1.

# Constraints:
# 1 <= nums.length <= 10^5
# nums[i] is either 0 or 1


# ===== Strategy =====
# - Try to find the longest subarray that end at index i
# - Let say there are index j so that the subarray from j to i
#   contains equal count_0 and count_1.
# - That means the difference between count_0 and count_1
#   of subarray [0, i] is equal to that of subarray [0, j - 1]
#
# => Solution:
# - Build a hash map that map (count_1 - count_0) to the
#   indices that end the prefixes.
# - At each index i, check the hashmap for the end indices of the prefixes
#   that has the same difference, then take the min one.
# - To improve space complexity, only store the min index for each group.
# - If count_1 == count count_0 at i, the whole subarray [0, i] is valid.
#   No need to store difference = 0 in the hash map.


def subarray_max_length(nums: list[int]) -> int:
    difference_first_occurrence = {}
    max_length = 0  # stay 0 if nums contains all 1's or all 0's
    difference = 0  # (count_1 - count_0) so far

    for i, num in enumerate(nums):
        difference += 1 if num == 1 else -1

        if difference == 0:
            max_length = i + 1
            continue

        if difference in difference_first_occurrence:
            max_length = max(max_length, i - difference_first_occurrence[difference])
        else:
            difference_first_occurrence[difference] = i

    return max_length


# ===== Complexity =====
# 1. Time complexity: O(n)
# - loop through nums, each iteration takes O(1)
#
# 2. Space complexity: O(n)
# - the difference map can grow to size n if nums contains all 1's or all 0's
