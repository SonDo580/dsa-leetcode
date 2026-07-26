"""
https://leetcode.com/problems/product-of-array-except-self/

Given an integer array 'nums', return an array answer such that
answer[i] is equal to the product of all the elements of nums except nums[i].

The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer.

You must write an algorithm that runs in O(n) time and without using the division operation.
"""

"""
Idea:
- Build prefix product and suffix product arrays.
  then ans[i] = prefix_product[i] * suffix_product[i]
  (may offset the index, depends on implementation)

Optimize:
- If there are at least 2 zeros in 'nums', all ans[i] = 0.
"""


class Solution:
    def productExceptSelf(self, nums: list[int]) -> list[int]:
        n = len(nums)

        # prefix_prod[i] = nums[0] * ... * nums[i-1]
        # prefix_prod[0] = 1 <-> empty prefix
        prefix_prod: list[int] = [1] * (n + 1)

        count_zeros = 0
        for i in range(1, n + 1):
            if nums[i - 1] == 0:
                count_zeros += 1
                if count_zeros == 2:
                    return [0] * n

            prefix_prod[i] = prefix_prod[i - 1] * nums[i - 1]

        # suffix_prod[i] = nums[i] * ... * num[n-1]
        # suffix_prod[n] = 1 <-> empty suffix
        suffix_prod: list[int] = [1] * (n + 1)
        for i in range(n - 1, -1, -1):
            suffix_prod[i] = suffix_prod[i + 1] * nums[i]

        ans: list[int] = []
        for i in range(n):
            ans.append(prefix_prod[i] * suffix_prod[i + 1])

        return ans


"""
Complexity:
- Let n = len(nums)

1. Time complexity: O(n)
- Build prefix_prod/suffix_prod: O(n)
- Find answer: O(n)

2. Space complexity: O(n) for 'prefix_prod' and 'suffix_prod'
"""
