"""
https://leetcode.com/problems/partition-array-such-that-maximum-difference-is-k/

Given an integer array 'nums' and an integer k,
split 'nums' into subsequences,
where each subsequence's maximum and minimum element is within k of each other.
What is the minimum number of subsequences needed?

For example, given nums = [3, 6, 1, 2, 5] and k = 2, the answer is 2.
The subsequences are [3, 1, 2] and [6, 5].
"""

"""
Idea:
- To minimize the number of groups, we need to maximize the number of elements in each group.
- Start with the smallest number x, we want all elements in the range [x, x + k] to be grouped.
  . If we exclude numbers in the range, the next group needs to start from a smaller number.
    This limits the range of elements that can be grouped by 2 groups.
- Keep doing this with a different x until we iterate through the whole array.
- For each subsequence, we only care about the maximum and minimum element.
  Order doesn't matter, because we only need to count the number of subsequences.
  -> We can sort the array for easier grouping
     (and thus counting subsets instead of subsequences).
"""


def partition_array(nums: list[int], k: int) -> int:
    # sort nums in ascending order
    nums.sort()

    count_groups = 1
    x = nums[0]  # current smallest element

    for i in range(1, len(nums)):
        # add a new group after the upper bound is reached
        if nums[i] - x > k:
            x = nums[i]
            count_groups += 1

    return count_groups


"""
Complexity:
- Let n = len(nums)

1. Time complexity:
- sort 'nums': O(n*log(n))
- iterate through 'nums': O(n)
=> Overall: O(n*log(n))

2. Space complexity: O(n) for sorting (timsort)
"""
