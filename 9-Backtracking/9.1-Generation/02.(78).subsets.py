"""
https://leetcode.com/problems/subsets/

Given an integer array 'nums' of unique elements,
return all possible subsets (the power set).

The solution set must not contain duplicate subsets.
Return the solution in any order.
"""

"""
Idea:
- Use backtracking to generate all unique subsets. States needed:
  . 'current': the subset being built
  . start: only add items in nums[start:]
- We need 'start' to avoid duplicates. Because order doesn't matter for subset,
  only combine in 1 direction (forward).
- All numbers are distinct & combine in 1 direction
  -> The resulting subsets will be unique.
- Since subsets can have any length, every node's 'current' is an answer 
  (including the root []).
"""


def get_subsets(nums: list[int]) -> list[list[int]]:
    n = len(nums)
    ans: list[list[int]] = []

    def build(current: list[int], start: int):
        # Mutate 'curr' across 'build' calls -> clone when adding
        ans.append(current[:])

        if start == n:
            return

        for j in range(start, n):
            current.append(nums[j])
            build(current, j + 1)
            current.pop()

    build(current=[], start=0)
    return ans


"""
Complexity:
- Each 'build' call is a node in recursion tree.

1. Time complexity: O(n * 2^n)
- Each number can either be included or not included in a subset
  -> Number of distinct subsets: 2^n
  -> Number of nodes = Number of distinct subsets = 2^n
- Clone 'curr' list (per node): O(n)
  -> Clone 'curr' list (across nodes): O(n * 2^n) 
- Total loop work = number of branches spawn
                  = number of nodes - 1   (exclude root)
                  = O(2^n)
=> Overall: O(n * 2^n) + O(2^n) = O(n * 2^n)
  
2. Space complexity: O(n)
- recursion stack: O(n)
- 'curr': O(n)
"""
