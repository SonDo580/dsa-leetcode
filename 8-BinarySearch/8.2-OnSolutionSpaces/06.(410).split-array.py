"""
https://leetcode.com/problems/split-array-largest-sum

Given an integer array 'nums' and an integer k,
split 'nums' into k non-empty sub-arrays such that
the largest sum of any sub-array is minimized.

Return the minimized largest sum of the split.
A sub-array is a contiguous part of the array.
"""

"""
- Let S be the largest sum of any sub-array.
  -> Check if we can split the array into k non-empty sub-arrays
     where each sub-array's sum <= S.
- Validity check:
  . Iterate through 'nums' and accumulate sum for each sub-array
    (reset for new sub-array).
  . If encounter a single num > S -> cannot split
  . Keep adding items to current sub-array if sum still <= S, 
    as long as each remaining sub-array can have at least 1 item.
  . Success if: can split to k non-empty sub-arrays
- Why try adding as much items to 1 sub-array as possible (greedy):
  . To reduce the average sum of remaining sub-arrays
    -> increase the chance that sub-array's sum <= S.
- S's range:
  . min: min(nums) (at least 1 element) 
  . max: sum(nums)
- We can binary search for optimal S (minimum valid).
"""


def split_array(nums: list[int], k: int) -> int:
    def can_split(max_sum: int, remaining_k: int) -> bool:
        """
        Return True if 'nums' can be split into k non-empty sub-arrays
        where each sub-array's sum <= max_sum
        """
        curr_sum = 0  # current sub-array's sum

        n = len(nums)
        for i, num in enumerate(nums):
            if num > max_sum:
                return False
            if curr_sum + num <= max_sum and n - i >= remaining_k:
                curr_sum += num  # expand current sub-array
            else:
                remaining_k -= 1
                curr_sum = num  # start a new sub-array

        if curr_sum <= max_sum:  # check last sub-array validity
            remaining_k -= 1

        return remaining_k == 0

    left = min(nums)  # min (non-empty) sub-array sum
    right = sum(nums)  # max sub-array sum
    while left <= right:
        mid = (left + right) // 2
        if can_split(mid, k):
            # search better solution (smaller max_sum)
            right = mid - 1
        else:
            # search valid solution (greater max_sum)
            left = mid + 1
    return left


"""
Complexity:
- Let n = len(nums), min = min(nums), max = sum(nums)

1. Time complexity:
- binary search: O(log(max-min))= O(log(max))
- check validity: O(n)
=> Overall: O(n*log(max))

2. Space complexity: O(1)
"""
