"""
https://leetcode.com/problems/3sum-smaller/

Given an array of n integers 'nums' and an integer 'target',
find the number of index triplets i, j, k with 0 <= i < j < k < n
that satisfy the condition nums[i] + nums[j] + nums[k] < target.
"""

"""
Idea:
- Keep 1 item fixed -> finding the other 2 items is '2sum' problem.
- To use '2 pointers', 'nums' must be sorted
  (don't need to track original indices).
- Let's keep nums[k] fix by iterating k in [2..n-1] (i < j < k).
  The answer is the total of valid pairs (nums[i], nums[j]) for each nums[k],
  so that nums[i] + nums[j] < target - nums[k]
- For each nums[k]:
  . Start with i = 0; j = k - 1
  . If nums[i] + nums[j] < target - nums[k]:
    . There are j - i valid pairs (keep i and k fixed, moving j to the left,
      then we always have nums[i] + nums[j] < target - nums[k]). 
      Note that duplicates are allowed. 
    . Try next nums[i]: i += 1
  . Else (nums[i] + nums[j] >= target - nums[k]):
    . Since nums[k] is fixed, we need to decrease the sum nums[i] + nums[j]
    . The only choice is decreasing nums[j]: j -= 1
"""


def three_sum_smaller(nums: list[int], target: int) -> int:
    nums.sort()
    ans = 0  # number of valid triplets

    for k in range(2, len(nums)):
        i = 0
        j = k - 1
        while i < j:
            if nums[i] + nums[j] < target - nums[k]:
                ans += j - i
                i += 1
            else:
                j -= 1

    return ans


"""
Complexity:
- Let n = len(nums)

1. Time complexity: O(n^2)
- sort 'nums': O(n*log(n)) (timsort)
- main loop: O(n^2)

2. Space complexity: O(n)
- sorting: O(n) (timsort)
"""
