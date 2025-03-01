# Given an integer array nums,
# return the length of the longest strictly increasing subsequence (LIS).

# Example 1:
# Input: nums = [10,9,2,5,3,7,101,18]
# Output: 4
# Explanation: The longest increasing subsequence is [2,3,7,101], therefore the length is 4.

# Example 2:
# Input: nums = [0,1,0,3,2,3]
# Output: 4

# Example 3:
# Input: nums = [7,7,7,7,7,7,7]
# Output: 1

# Constraints:
# 1 <= nums.length <= 2500
# -104 <= nums[i] <= 104

# Follow up: Can you come up with an algorithm that runs in O(n log(n)) time complexity?


# ===== Identify DP problem =====
# - ask for maximum subsequence length
# - taking an element will change the numbers we can take later

# ===== Analyze =====
# - state variable: index i
#   dp(i) returns the length of the LIS that ends with ith element
#
# - we can only use the current element if the previous element is
#   less than the current element
# -> recurrence relation:
#   dp(i) = max(dp(j) + 1) where j is in [0, i), nums[j] < nums[i]
#   (add 1 for current element)
#
# - base cases:
# every element is technically an increasing subsequence with length 1
#
# - we can find the length of the LIS that ends at each index,
#   then take the maximum of those.


# ===== Top-down =====
def length_of_LIS(nums: list[int]) -> int:
    def dp(i: int) -> int:
        max_len = 1

        if i in memo:
            return memo[i]

        for j in range(i):
            if nums[i] > nums[j]:
                max_len = max(max_len, dp(j) + 1)

        memo[i] = max_len
        return max_len

    memo: dict[int, int] = {}
    return max(dp(i) for i in range(len(nums)))


# ===== Bottom-up =====
def length_of_LIS(nums: list[int]) -> int:
    dp: list[int] = [1] * len(nums)

    for i in range(len(nums)):
        for j in range(i):
            if nums[i] > nums[j]:
                dp[i] = max(dp[i], dp[j] + 1)

    return max(dp)


# ===== Complexity for both implementations =====
# Time complexity: O(n^2) (because of the nested loop)
# Space complexity: O(n) (number of states)

# The space complexity can't be improved in bottom-up approach
# because the recurrence relation is not static
# - Static recurrence relation means the next state depends on
#   a fixed number of previous states
# - In this problem, each dp[i] depends on a variable number of
#   previous states (dp[j] where j in [0, i) and nums[i] > nums[j])
