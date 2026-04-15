"""
https://leetcode.com/problems/number-of-ways-to-split-array/

Given an integer array 'nums', find the number of ways to
split the array into two parts so that the first section
has a sum greater than or equal to the sum of the second section.
The second section should have at least one number.
"""


# ====== Approach 1: Prefix sum =====
def ways_to_split_array(nums: list[int]) -> int:
    # prefix_sum[i] = sum([0..i])
    prefix_sum = [nums[0]]
    for i in range(1, len(nums)):
        prefix_sum.append(nums[i] + prefix_sum[-1])

    count_ways = 0
    for i in range(len(nums) - 1):
        left_sum = prefix_sum[i]
        right_sum = prefix_sum[-1] - left_sum
        if left_sum >= right_sum:
            count_ways += 1

    return count_ways


"""
Complexity:

1. Time complexity: O(n)
- build prefix_sum: O(n)
- try splitting at each position: O(n)

2. Space complexity: O(n) for prefix_sum
"""


# ====== Approach 2: Update sums incrementally =====
# (reduce space complexity)
def ways_to_split_array_2(nums: list[int]) -> int:
    total = sum(nums)
    count_ways = 0
    left_sum = 0

    for i in range(len(nums) - 1):
        left_sum += nums[i]
        right_sum = total - left_sum
        if left_sum >= right_sum:
            count_ways += 1

    return count_ways


"""
Complexity:

1. Time complexity: O(n) 
- calculate total: O(n)
- try splitting at each position: O(n)

2. Space complexity: O(1)
"""
