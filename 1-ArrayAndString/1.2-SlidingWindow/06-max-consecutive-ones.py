# Given a binary array nums and an integer k, 
# return the maximum number of consecutive 1's in the array 
# if you can flip at most k 0's.

# Example 1:
# Input: nums = [1,1,1,0,0,0,1,1,1,1,0], k = 2
# Output: 6
# Explanation: [1,1,1,0,0,1,1,1,1,1,1]
#                         x         x

# Example 2:
# Input: nums = [0,0,1,1,0,0,1,1,1,0,1,1,0,0,0,1,1,1,1], k = 3
# Output: 10
# Explanation: [0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,1,1,1,1]
#                       x x       x

# Constraints:
# 1 <= nums.length <= 10^5
# nums[i] is either 0 or 1.
# 0 <= k <= nums.length

# => Reframe the question:
# The longest subarray that contains at most k zeros

def longest_ones(nums: list[int], k: int) -> int:
    left = 0
    count_zero = 0
    max_length = 0

    for right in range(len(nums)):
        if nums[right] == 0:
            count_zero += 1

        while count_zero > k:
            if nums[left] == 0:
                count_zero -= 1
            left += 1
        
        max_length = max(max_length, right - left + 1)

    return max_length