# You are given an integer array nums consisting of n elements,
# and an integer k.

# Find a contiguous subarray whose length is equal to k
# that has the maximum average value and return this value.
# Any answer with a calculation error less than 10-5 will be accepted.

# Example 1:
# Input: nums = [1,12,-5,-6,50,3], k = 4
# Output: 12.75000
# Explanation: Maximum average is (12 - 5 - 6 + 50) / 4 = 51 / 4 = 12.75

# Example 2:
# Input: nums = [5], k = 1
# Output: 5.00000

# Constraints:
# n == nums.length
# 1 <= k <= n <= 10^5
# -10^4 <= nums[i] <= 10^4

def subarray_max_average(nums: list[int], k: int) -> float:
    current_sum = 0
    for i in range(k):
        current_sum += nums[i]

    max_average = current_sum / k

    for i in range(k, len(nums)):
        current_sum += nums[i] - nums[i - k]
        max_average = max(max_average, current_sum / k)

    return max_average
