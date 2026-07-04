"""
https://leetcode.com/problems/subsets-ii/

Given an integer array 'nums' that may contain duplicates,
return all possible subsets (the power set).

The solution set must not contain duplicate subsets.
Return the solution in any order.
"""

"""
Idea:
- Use backtracking to find all subsets. States needed.
  . curr: current subset being built.
  . i: current item to choose (put in current subset or not)
- Add 'curr' to result after considering all numbers
  . when i == len(nums).

- Since 'nums' contains duplicates, the above solution can lead 
  to duplicate subsets.
  Example: [1, 2, 2]
  . used_indices = {0, 1} -> subset: {1, 2}
  . used_indices = {0, 2} -> subset: {1, 2} (duplicate)
- Deduplication strategy:
  . Let say a number 'num' has a few instances in 'nums'
  . If a subset includes ith instance and excludes (i-1)th instance of 'num',
    we should skip it (stop exploring that path).
    (The result set is the same as excluding ith instance and including ith instance).
	-> extra state needed to check inclusion: 'used'
	   (can be set / boolean array / bitmask)
- Optimize: If the instances of each 'num' are adjacent,
  we can check the above condition quickly.
  -> . Sort the original 'nums' array.
     . Stop exploring current path if nums[i]) is included
       but nums[i - 1] is excluded, and nums[i - 1] == nums[i] .
"""


def subsets_with_dup(nums: list[int]) -> list[list[int]]:
    n = len(nums)
    ans: list[list[int]] = []

    nums.sort()  # to check duplicate quickly

    def choose(i: int, curr: list[int], used: list[bool]) -> None:
        """include or exclude nums[i] in current subset."""
        if i == n:  # considered all 'nums'
            # Clone since we mutate 'curr' across 'choose' calls
            ans.append(curr[:])
            return

        # Option 1: exclude nums[i]
        choose(i + 1, curr, used)

        # Option 2: include nums[i]
        if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:
            return  # skip if generating duplicate subset
        curr.append(nums[i])
        used[i] = True
        choose(i + 1, curr, used)
        curr.pop()
        used[i] = False

    choose(i=0, curr=[], used=[False] * n)
    return ans


"""
Complexity:
- Each 'choose' call is a node in recursion tree.

1. Time complexity: O(n * 2^n)
- Sort 'nums': O(n*log(n))
- Number of distinct subsets (leaf nodes): O(2^n) (= 2^n if all numbers are distinct)
  Clone 'curr' at each leaf node: O(n)
  -> Total work at leaves: O(n * 2^n)
- Number of internal nodes: O(2^(n-1)) = O(2^n)
  . Branching factor: 2
  . Recursion depth (exclude last level for leaves): O(n-1)
  -> Total work at internal nodes: O(2^n) * O(1) = O(2^n)
=> Overall: O(n * 2^n) + O(2^n) = O(n * 2^n)

2. Space complexity: O(n)
- Sort 'nums': O(n) (timsort)
- recursion stack: O(n)
- 'curr': O(n)
- 'used': O(n)
"""
