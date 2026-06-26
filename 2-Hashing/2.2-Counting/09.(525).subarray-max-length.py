"""
https://leetcode.com/problems/contiguous-array/

Given a binary array 'nums',
return the maximum length of a contiguous subarray
with an equal number of 0 and 1.
"""

"""
Idea:
- Try to find the longest valid subarray that end at index i
- Consider index j so that the subarray from j to i
  contains equal count_0 and count_1.
- That means the difference between count_0 and count_1
  of subarray [0, i] is equal to that of subarray [0, j - 1]

Implementation:
- count_0, count_1 is the number of 0's and 1's in a prefix.
  . diff = count_1 - count_0
- Build a hash map that maps 'diff' to end indices of prefixes.
- At each index i, check the hash map for end indices of prefixes
  with the same 'diff'. To form longest subarray, choose the min index.
  -> Only need the min index for each group with the same 'diff'.
- If diff == 0, the whole subarray [0, i] is valid.
  -> No need to store diff = 0 in the hash map.
"""


def subarray_max_length(nums: list[int]) -> int:
    # map (count_1 - count_0) to prefix's end index
    # only 1st prefix's end index for each difference is recorded
    diff_1st_idx: dict[int, int] = {}

    max_len = 0  # stay 0 if 'nums' contains all 1's or all 0's
    diff = 0  # (count_1 - count_0) so far

    for i, num in enumerate(nums):
        diff += 1 if num == 1 else -1

        if diff == 0:
            # [0..i] is longest valid subarray that ends at i
            max_len = i + 1
            continue

        if diff in diff_1st_idx:
            # [val+1..i] is longest valid subarray that ends at i
            max_len = max(max_len, i - diff_1st_idx[diff])
        else:
            # only record for 1st prefix
            diff_1st_idx[diff] = i

    return max_len


"""
Complexity:
- Let n = len(nums)

1. Time complexity: O(n)

2. Space complexity: O(n) for 'diff'
(worst case: n differences when 'nums' contains all 1's or all 0's)
"""
