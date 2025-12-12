"""
https://leetcode.com/problems/maximum-subarray-min-product/

The min-product of an array is equal to the minimum value
in the array multiplied by the array's sum.
. For example, the array [3,2,5] (minimum value is 2)
  has a min-product of 2 * (3+2+5) = 2 * 10 = 20.

Given an array of integers 'nums',
return the maximum min-product of any non-empty subarray of 'nums'.
Since the answer may be large, return it modulo 10^9 + 7.

Note that the min-product should be maximized before performing the modulo operation.
Testcases are generated such that the maximum min-product without modulo will fit in a 64-bit signed integer.

Constraints:
1 <= nums.length <= 10^5
1 <= nums[i] <= 10^7
"""

"""
Idea:
- For each element x:
  . Find the longest subarray that contains x and has min = x
  . Calculate the total_sum of the subarray
  . Calculate min_product = x * total_sum
  Compare the results for all elements to find the maximum min_product.
- To find the longest subarray that contains x and has min = x
  + Find the left bound:
`   . Iterate through nums 
    . Keep pushing elements onto a stack
    . Before pushing x, pop all elements >= x off the stack.
    . The left bound is (top_of_stack + 1) if the stack is not empty.
      The default left bound is 0 (when the stack is empty).
  + Find the right bound: 
    . Use similar algorithm but iterate in reverse.
    . The right bound is (top_of_stack -1 1) if the stack is not empty.
      The default right bound is n - 1 (when the stack is empty).
- To calculate subarray sum efficiently, build the prefix sum array. 
  . prefixSum[i] = total sum of elements up to i
  . prefixSum[j] - prefixSum[i - 1] = total sum of elements in range [i, j] (if i > 0)
"""


def max_sum_min_product(nums: list[int]) -> int:
    n = len(nums)
    left_bounds: list[int] = [0] * n
    right_bounds: list[int] = [n - 1] * n

    # Find left bound for each subarray that has min = nums[i]
    stack: list[int] = []  # store indices
    for i in range(n):
        while stack and nums[stack[-1]] >= nums[i]:
            stack.pop()
        if stack:
            left_bounds[i] = stack[-1] + 1
        stack.append(i)

    # Find right bound for each subarray that has min = nums[i]
    stack = []  # reset stack
    for i in range(n - 1, -1, -1):
        while stack and nums[stack[-1]] >= nums[i]:
            stack.pop()
        if stack:
            right_bounds[i] = stack[-1] - 1
        stack.append(i)

    # Build prefix sum array
    prefix_sum: list[int] = []
    current_sum = 0
    for i in range(n):
        current_sum += nums[i]
        prefix_sum.append(current_sum)

    # Find maximum min_product
    # (all numbers are positive so products are positive)
    result: int = -1
    for i in range(n):
        subarray_sum = prefix_sum[right_bounds[i]]
        if left_bounds[i] > 0:
            subarray_sum -= prefix_sum[left_bounds[i] - 1]
        min_product = nums[i] * subarray_sum
        result = max(result, min_product)

    return result % 1_000_000_007


"""
Complexity:

1. Time complexity:
- Find left and right bounds: O(n)
- Build prefix sum array: O(n)
- Find maximum min-product: O(n)  
=> Overall: O(n)

2. Space Complexity: O(n)
- 'left_bounds', 'right_bounds', 'prefix_sum' arrays: both O(n)
"""
