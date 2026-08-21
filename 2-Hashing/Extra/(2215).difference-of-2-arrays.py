"""
https://leetcode.com/problems/find-the-difference-of-two-arrays/

Given 2 0-indexed integer arrays nums1 and nums2,
return a list answer of size 2 where:
- answer[0] is a list of all distinct integers in nums1 which are not present in nums2.
- answer[1] is a list of all distinct integers in nums2 which are not present in nums1.

Note that the integers in the lists may be returned in any order.
"""

"""
Idea:
- Build the set of distinct integers in nums1 and in nums2.
- Iterate through set(nums1), add x to answer[0] if x  is not in set(nums2).
- Iterate through set(nums2), add x to answer[1] if x  is not in set(nums1).
"""


class Solution:
    def findDifference(self, nums1: list[int], nums2: list[int]) -> list[list[int]]:
        set1 = set(nums1)
        set2 = set(nums2)
        ans: list[list[int]] = [[], []]
        for x in set1:
            if x not in set2:
                ans[0].append(x)
        for x in set2:
            if x not in set1:
                ans[1].append(x)
        return ans


"""
Complexity:
- Let m = len(nums1), n = len(nums2)

1. Time complexity: O(m + n)
2. Space complexity: O(m + n)
"""


# === Use set difference ===
class Solution:
    def findDifference(self, nums1: list[int], nums2: list[int]) -> list[list[int]]:
        set1 = set(nums1)
        set2 = set(nums2)
        return [list(set1 - set2), list(set2 - set1)]
