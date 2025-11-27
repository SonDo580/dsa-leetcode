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
