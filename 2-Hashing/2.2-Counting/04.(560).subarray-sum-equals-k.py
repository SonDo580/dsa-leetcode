"""
https://leetcode.com/problems/subarray-sum-equals-k/

Given an array of integers 'nums' and an integer k,
return the total number of subarrays whose sum equals to k.

A subarray is a contiguous non-empty sequence of elements within an array.
"""

"""
Idea:
- At any given index i, the prefix sum up to i is 'current'.
  If there is an index j whose prefix sum is current - k, 
  the sum of subarray from j + 1 to i is current - (current - k) = k
- Since there are negative numbers, the same prefix sum can occur multiple times.
  -> Use a hashmap 'cnt' to track how many time a prefix sum has occurred.
- At every index i, the frequency of current - k is equal to 
  the number of subarrays whose sum is equal to k that end at i.
- Special case: Initialize cnt[0] = 1 (for the empty prefix [])
  (When current == k, the whole subarray [0..i] should be counted).
"""

from collections import defaultdict


def subarray_sum_equals_k(nums: list[int], k: int) -> int:
    # count how many times a prefix sum has occurred
    cnt: defaultdict[int, int] = defaultdict(int)

    cnt[0] = 1
    prefix_sum: int = 0
    ans: int = 0

    for num in nums:
        prefix_sum += num
        ans += cnt[prefix_sum - k]
        cnt[prefix_sum] += 1

    return ans


"""
Complexity:
- Let n = len(nums)
1. Time complexity: O(n) - iterate through 'nums'
2. Space complexity: O(n) - for 'cnt' dict
"""

# === INEFFICIENT approaches ===
"""
- At each index i, we want to find subarrays that end at i
  whose sum is equal to k.

- Method 1: brute-force 
  . Iterate [0..i], ..., [i..i] to find the sum of each subarray
  -> O(n^2) for each index i, 
     O(n^3) for the whole array. 
  -> too inefficient.

- Method 2: prefix sum array
  . Build prefix sum array to calculate the sum of a subarray quickly.
  . At each i, iterate [0..i] and calculate the sum of each subarray
    [j..i] as prefix_sum[i] - prefix_sum[j - 1] (edge case: j=0).
  -> O(n) for each index i,
     O(n^2) for the whole array.
  -> slightly better but still inefficient.

=> Improvement (leading to the "main" approach):
- For a subarray [j..i] has sum equal to k:
  . prefix_sum[i] - prefix_sum[j - 1] = k
    -> prefix_sum[j - 1] = prefix_sum[i] - k
- To check quickly, add encountered prefix sum as key to a hash map.
  The value can be the list of indices, or frequency in our problem. 
"""


# === FAILED approach: sliding window ===
"""
- Use window constraint: sum <= k.
  If sum == k after maintenance, increase 'ans'.
- WHY failed: 'nums' contains negative number
  -> sum is not monotonic.
"""


def _subarray_sum_equals_k(nums: list[int], k: int) -> int:
    curr_sum: int = 0
    left: int = 0
    ans: int = 0

    for right, num in enumerate(nums):
        curr_sum += num

        while curr_sum > k:
            curr_sum -= nums[left]
            left += 1

        # non-empty: left <= right
        if left <= right and curr_sum == k:
            ans += 1

    return ans
