"""
https://leetcode.com/problems/longest-increasing-subsequence

Given an integer array 'nums',
return the length of the longest strictly increasing subsequence.

Example 1:
Input: nums = [10,9,2,5,3,7,101,18]
Output: 4
Explanation: The longest increasing subsequence is [2,3,7,101], therefore the length is 4.

Example 2:
Input: nums = [0,1,0,3,2,3]
Output: 4

Example 3:
Input: nums = [7,7,7,7,7,7,7]
Output: 1

Constraints:
1 <= nums.length <= 2500
-10^4 <= nums[i] <= 10^4

Follow up: Can you come up with an algorithm that runs in O(n * log(n)) time complexity?
"""

# ===== Approach 1: DP =====
# ==========================
"""
Identify DP problem:
- ask for maximum subsequence length.
- taking an element affects elements we can take later.

Solution:
- Let dp[i] be the length of the LIS that ends with nums[i].
- We can add nums[i] to subsequences that end with nums[j] (0 <= j < i)
  if nums[j] < nums[i] (strictly increasing).
  -> dp[i] = max(dp[j] + 1) where j is in [0, i) and nums[j] < nums[i]
- Base case: every element is a subsequence with length 1.
- Find the length of the LIS that ends at each index,
  and take the maximum of those.
"""


# ----- Bottom-up -----
def length_of_LIS(nums: list[int]) -> int:
    n = len(nums)
    dp: list[int] = [1] * n

    for i in range(n):
        for j in range(i):
            if nums[i] > nums[j]:
                dp[i] = max(dp[i], dp[j] + 1)

    return max(dp)


"""
1. Time complexity: O(n^2)
- build 'dp': O(n^2)
- find max(dp): O(n)

2. Space complexity: O(n) for 'dp' array
- Space complexity cannot be improved since the recurrence relation is not static:
  + Static recurrence relation means the next state depends on
    a fixed number of previous states.
  + In this problem, each dp[i] depends on a variable number of
    previous states (dp[j] where j in [0, i) and nums[i] > nums[j]).
"""


# ----- Top-down -----
def length_of_LIS(nums: list[int]) -> int:
    memo: dict[int, int] = {}

    def dp(i: int) -> int:
        if i in memo:
            return memo[i]

        max_len = 1
        for j in range(i):
            if nums[i] > nums[j]:
                max_len = max(max_len, dp(j))

        memo[i] = max_len
        return max_len

    return max(dp(i) for i in range(len(nums)))


"""
1. Time complexity: O(n^2)
- Find dp(i): O(n) (because of caching)
  Repeat for n elements.

2. Space complexity: O(n)
- memo: O(n)
- recursion stack: O(1) (because of caching)
"""


# ===== Approach 2: Binary search =====
# (see BinarySearch section)


# ===== Extra: Find 1 specific LIS =====
# ======================================
"""
- We can modify the algorithm to reconstruct 1 LIS
- Let's use:
  + 'dp': dp[i] = the length of 1 LIS that ends with nums[i]
  + 'prev': prev[i] = index of the previous element in 1 LIS ending at nums[i].
                      (or -1 if nums[i] starts a subsequence)
- Update both 'dp' and 'prev' at each step.
- At the end, reconstruct 1 LIS:
  + Find the ending index of the LIS.
  + Walk 'prev' backwards.               
"""


def LIS(nums: list[int]) -> int:
    n = len(nums)
    dp: list[int] = [1] * n
    prev: list[int] = [-1] * n

    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i] and dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
                prev[i] = j

    # Find the ending index of the LIS
    lis_len = max(dp)
    k = dp.index(lis_len)

    # Reconstruct the LIS
    reversed_lis: list[int] = []
    while k != -1:
        reversed_lis.append(nums[k])
        k = prev[k]  # trace backwards

    return list(reversed(reversed_lis))


"""
Complexity:

1. Time complexity:
- Build 'dp' and 'prev': O(n^2)
- Find ending index of LIS: O(n)
- Recover LIS (trace then reverse): O(n)
=> Overall: O(n^2)

2. Space complexity:
- 'dp': O(n)
- 'prev': O(n)
=> Overall: O(n)
"""
