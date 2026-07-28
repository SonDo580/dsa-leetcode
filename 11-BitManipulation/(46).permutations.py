"""
https://leetcode.com/problems/permutations/

Given an array 'nums' of distinct integers,
return all the possible permutations.
You can return the answer in any order.
"""

"""
Idea:
- Use backtracking to generate all possible permutations. States needed:
  . 'current': current permutation being built.
  . 'used': track indices of used numbers
            (use set / boolean array / bitmask)
- Valid result found when len(curr) = len(nums)
  (included each number once).

Represent 'used' with bitmask:
- ith bit = 1 <-> nums[i] is included.
- Get ith bit (to check if nums[i] is used): (used >> i) & 1
- Flip ith bit (to include/exclude nums[i]): used & (1 << i)
"""


def get_bit(n: int, i: int) -> int:
    return (n >> i) & 1


def flip_bit(n: int, i: int) -> int:
    return n & (1 << i)


class Solution:
    def permute(self, nums: list[int]) -> list[list[int]]:
        n = len(nums)
        ans: list[list[int]] = []

        def build(curr: list[int], used: list[bool]):
            if len(curr) == n:  # included each number once
                # Mutate 'curr' across 'build' calls -> clone when adding
                ans.append(curr[:])
                return

            for i in range(n):
                if get_bit(used, i):
                    continue
                curr.append(nums[i])
                build(curr, flip_bit(used, i))
                curr.pop()

        build(curr=[], used=0)
        return ans


"""
Complexity:
- Each 'build' call is a node in recursion tree
- Recursion depth: O(n)

1. Time complexity: O(n * n!) + O(n * n!) = O(n * n!)
- Number of permutations = number of leaves = n!
  Clone 'curr' to add to result: O(n)
  -> Total work at leaves: O(n * n!) 
- Iterate through 'nums' in each node: O(n)
  Number of nodes:
  . 1st level: spawn n branches (no numbers have been used)
  . 2nd level: each node spawns n-1 branches
  . ...
  -> Number of nodes: n + n*(n - 1) + ... n! ~= e * n!
  -> Loop work across nodes: O(n * n!)

2. Space complexity: O(n)
- recursion stack: O(n).
- 'curr': O(n).
"""


# === Proof: n + n*(n - 1) + ... n! ~= e * n! ===
""" 
n + n*(n - 1) + ... n!
= n! + n*(n-1)*...*3*2 + ... + n*(n-1) + n
= n! * (1 + 1/1! + 1/2! + ... + 1/(n-1)!)

Taylor series expansion for Euler's number:
. e^x = sum(x^k / k!)
. x = 1 
  -> e^1 = 1 + 1/1! + 1/2! + ... + 1/(n-1)!
  -> e * n! = n! * (1 + 1/1! + 1/2! + ... + 1/(n-1)!)
"""