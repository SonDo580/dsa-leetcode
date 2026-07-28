"""
https://leetcode.com/problems/subsets-ii/

Given an integer array 'nums'  that may contain duplicates,
return all possible subsets (the power set).

The solution set must not contain duplicate subsets.
Return the solution in any order.
"""

"""
Idea:
- Use backtracking to find all valid subsets.
- At each nums[i], we can include/exclude it in current subset being built.
- If x has multiple instances in nums:
  . include instance k-1, exclude instance k <-> exclude instance k-1, include instance k
    (result in duplicate subsets)
  -> Don't include instance k if exclude instance k-1.
- We can check faster if all instances of the same x are adjacent.
  And order in subset is not important.
  -> Sort 'nums'.
- Use a set / boolean array 'used' where
  used[i] indicates nums[i] is used in current subset.
  -> Optimize: Use bit mask.

Manipulate 'used':
- ith bit = 1 -> nums[i] is included
  ith bit = 0 -> nums[i] is not included
- Check if ith bit is 1 (nums[i] is included in current subset):
  . method 1: ((used >> i) & 1) == 1
  . method 2: (used & (1 << k)) != 0  (> 0 to be exact)
- Flip ith bit (include/exclude nums[i] from current subset):
  . used ^ (1 << k)
"""


def get_bit(n: int, i: int) -> int:
    """Return ith bit of n."""
    return (n >> i) & 1


def flip_bit(n: int, i: int) -> int:
    """Return new n with ith bit flipped."""
    return n ^ (1 << i)


class Solution:
    def subsetsWithDup(self, nums: list[int]) -> list[list[int]]:
        ans: list[list[int]] = []
        nums.sort()

        def choose(i: int, curr: list[int], used: int) -> None:
            """Include or exclude nums[i] in current subset."""
            if i == len(nums):  # process all 'nums'
                ans.append(curr[:])
                return

            # option 1: exclude nums[i]
            choose(i + 1, curr, used)

            # option 2: include nums[i] if don't generate duplicates
            if i == 0 or nums[i - 1] != nums[i] or get_bit(used, i - 1):
                curr.append(nums[i])
                choose(i + 1, curr, flip_bit(used, i))
                curr.pop()

        choose(i=0, curr=[], used=0)
        return ans


"""
Complexity:
- Each 'choose' call is a node in recursion tree.

1. Time complexity: O(n * 2^n) + O(2^n) = O(n * 2^n)
- Sort 'nums': O(n*log(n))
- Number of distinct subsets (leaf nodes): O(2^n) (= 2^n if all numbers are distinct)
  Clone 'curr' at each leaf node: O(n)
  -> Total work at leaves: O(n * 2^n)
- . Branching factor: 2
  . Recursion depth (exclude last level for leaves): O(n-1)
  -> Number of internal nodes: O(2^(n-1)) = O(2^n)
  -> Total work at internal nodes: O(2^n)

2. Space complexity: O(n)
- Sort 'nums': O(n) (timsort)
- recursion stack: O(n)
- 'curr': O(n)
"""