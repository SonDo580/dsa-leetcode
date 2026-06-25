"""
https://leetcode.com/problems/3sum/

Given an integer array 'nums',
return all the triplets [nums[i], nums[j], nums[k]]
such that i != j, i != k, and j != k,
and nums[i] + nums[j] + nums[k] == 0.

Notice that the solution set must not contain duplicate triplets.
"""

"""
Idea:
- Keep 1 item fixed, then finding the other 2 items is '2sum' problem.
- To use '2 pointers', 'nums' must be sorted.
  We only need to return values -> don't need to track original indices.
"""


def three_sum(nums: list[int]) -> list[list[int]]:
    nums.sort()
    ans: list[list[int]] = []
    n = len(nums)

    i = 0
    while i < n - 2:  # i < j < k < n
        if nums[i] > 0:
            # nums[i] <= nums[j] <= nums[k]
            # -> nums[i] + nums[j] + nums[k] >= 3 * nums[i]
            # -> nums[i] + nums[j] + nums[k] > 3 * 0 (cannot == 0)
            break

        j = i + 1
        k = n - 1
        while j < k:
            sum3 = nums[i] + nums[j] + nums[k]
            if sum3 == 0:
                ans.append([nums[i], nums[j], nums[k]])

                # skip duplicate nums[j]
                while j < k and nums[j + 1] == nums[j]:
                    j += 1
                
                # increase nums[j] OR cause j > k
                # (staying the same only results in duplicate pairs)
                j += 1  

                # duplicate nums[k] will be skipped in subsequent iterations,
                # since it results in sum3 > 0 after nums[j] has increased
                k -= 1
            elif sum3 < 0:
                j += 1
            else:
                k -= 1

        # skip duplicate nums[i]
        while i < n - 1 and nums[i + 1] == nums[i]:
            i += 1
        i += 1  # increase nums[i] OR cause i > n - 1

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
