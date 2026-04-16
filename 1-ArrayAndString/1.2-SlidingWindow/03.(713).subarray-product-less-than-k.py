"""
https://leetcode.com/problems/subarray-product-less-than-k/

Given an array of positive integers 'nums' and an integer k,
return the number of subarrays where the product of all the elements
in the subarray is strictly less than k.

For example, given the input nums = [10, 5, 2, 6], k = 100,
the answer is 8. The subarrays with products less than k are:

[10], [5], [2], [6], [10, 5], [5, 2], [2, 6], [5, 2, 6]
"""

"""
Monotonicity of window constraint:
- Since 'nums' only contains positive numbers
-> Extend (right) increases the product
   Shrink (left) decreases the product

Number of valid sub-arrays:
- If product(nums[left..right]) < k
  then all product(nums[left..i]) < k for i in [left..right]
  and all product(nums[i..right]) < k for i in [left..right]
  -> Number of valid sub-arrays that ends at right:
     . count = right - left + 1 (window length)
- DON'T also count (nums[left..i] for i in [left..right]),
  since they have been counted in previous iterations of 'right' 
  (while extending from 'left' to current 'right').

- Why don't count valid sub-arrays that starts from left:
  . For a given 'right', after the shrinking, 
    [left..right] is the longest window that ends at 'right'.
  . But we do not know when a 'left' will stop being valid.
"""


def subarray_count(nums: list[int], k: int) -> int:
    left = 0
    count = 0
    current_product = 1

    for right in range(len(nums)):
        current_product *= nums[right]

        while current_product >= k and left <= right:
            current_product //= nums[left]
            left += 1

        # add the number of valid sub-arrays that ends at right
        count += right - left + 1

    return count


"""
Complexity:

1. Time complexity: O(n)
- 'right' moves n times.
- 'left' moves at most n times.

2. Space complexity: O(1)
"""

# ===== A more "convoluted" approach =====
"""
- Count number of valid 'right' positions for a 'left'
  before it is forced to increment.
- Number of valid sub-arrays that starts at 'left':
  (= number that ends at 'right')
  . count = right - left + 1 (window length)
"""


def subarray_count(nums: list[int], k: int) -> int:
    left = 0
    count = 0
    current_product = 1
    n = len(nums)

    for right in range(n):
        current_product *= nums[right]

        while current_product >= k and left <= right:
            # add the number of valid sub-arrays that starts at left
            # (ends at right-1 since nums[right] makes the window invalid)
            count += (right - 1) - left + 1

            current_product //= nums[left]
            left += 1

    # Handle the last valid window [left..n-1]
    while left <= n - 1:
        count += (n - 1) - left + 1
        left += 1

    return count
