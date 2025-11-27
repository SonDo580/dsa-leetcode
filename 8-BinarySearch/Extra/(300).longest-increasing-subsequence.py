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
# (see DynamicProgramming section)

# ===== Approach 2: Binary search =====
# =====================================
"""
Analysis:
- For an increasing subsequence of length L, we should try to find
  the smallest possible ending value (tail), because that gives
  more opportunity to extend the subsequence later.
  -> Let's use a list 'tails' where tails[L] is the smallest tail 
     for any subsequence of length L + 1.

- A subsequence with length L + 1 must end with a value strictly 
  larger than the tail of a subsequence with length L.
  -> 'tails' is strictly increasing (tails[0] < tails[1] < ...)

- For a new element 'x':
  + If 'x' is greater than all tails (compare with tails[-1]),
    append it to 'tails' (extend the longest found subsequence).
  + Otherwise, 'x' can serve as a better (smaller) tail for some
    existing subsequence length.
    -> find the left most index i such that tails[i] >= x,
       then replace tails[i] = x

- Since 'tails' is strictly increasing, we can perform binary search
  to find the first element >= x (bisect_left/lower_bound operation)

- The length of the LIS is the final length of 'tails'.
"""

import bisect


def length_of_LIS(nums: list[int]) -> int:
    tails: list[int] = []

    for num in nums:
        if len(tails) == 0 or tails[-1] < num:
            tails.append(num)
        else:
            idx = bisect.bisect_left(tails, num)
            tails[idx] = num

    return len(tails)


"""
Complexity:
- Let n = nums.length

1. Time complexity: 
- Iterate through 'nums': O(n)
- bisect_left: O(log(n))
=> Overall: O(n * log(n))

2. Space complexity: O(n) for 'tails'
"""


# ===== Extra: Find 1 specific LIS =====
# ======================================
"""
- We can modify the algorithm to reconstruct 1 LIS
- Let's maintain:
  + 'tails': stores smallest tail for subsequence lengths (same as before).
  + 'tail_indices': stores index in 'nums' for each value in 'tails'.
  + 'previous': previous[i] = index of the previous element in the LIS ending at nums[i].

- When nums[i] updates tails[k], the predecessor of nums[i] is at tail_indices[k - 1]
  -> set previous[i] = tail_indices[k - 1]

- At the end, the LIS ends with tail_indices[-1].
  Follow 'previous' backwards to reconstruct the LIS.
"""


def LIS(nums: list[int]) -> int:
    tails: list[int] = []
    tail_indices: list[int] = []
    previous = [-1] * len(nums)

    for i, num in enumerate(nums):
        if len(tails) == 0 or tails[-1] < num:
            tails.append(num)
            tail_indices.append(i)
            if len(tails) > 1:
                previous[i] = tail_indices[-2]
        else:
            idx = bisect.bisect_left(tails, num)
            tails[idx] = num
            tail_indices[idx] = i
            previous[i] = tail_indices[idx - 1]

    # reconstruct the LIS
    reversed_lis: list[int] = []
    k = tail_indices[-1]  # index of last element in LIS
    while k != -1:
        reversed_lis.append(nums[k])
        k = previous[k]  # trace backwards

    return list(reversed(reversed_lis))
