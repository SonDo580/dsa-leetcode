"""
https://leetcode.com/problems/permutations/

Given an array 'nums' of distinct integers,
return all the possible permutations.
You can return the answer in any order.
"""

"""
Idea:
- Use backtracking to generate all possible permutations. States needed:
  . 'current': numbers in current permutations.
  . 'used': track indices of used numbers
            (use set / boolean array / bitmask)
- Valid result found when len(curr) = len(nums).
"""


def get_permutations(nums: list[int]) -> list[list[int]]:
    n = len(nums)
    ans: list[list[int]] = []

    def build(curr: list[int], used: list[bool]):
        if len(curr) == n:
            # Mutate 'curr' across 'build' calls -> clone when adding
            ans.append(curr[:])
            return

        for i in range(n):
            if not used[i]:
                curr.append(nums[i])
                used[i] = True
                build(curr, used)
                curr.pop()
                used[i] = False

    build(curr=[], used=[False] * n)
    return ans


"""
Complexity:
- Each 'build' call is a node in recursion tree
- Recursion depth: O(n)

1. Time complexity: O(n * n!)
- Iterate through 'nums' in each node: O(n)
  Number of nodes:
  . 1st level: spawn n branches (no numbers have been used)
  . 2nd level: each node spawns n-1 branches
  . ...
  -> Number of nodes: n + n*(n - 1) + ... n! ~~ e * n! 
  -> Loop work across nodes: O(n * n!)
- Total number of permutations (number of leaf nodes): n!.
  Clone 'curr' to add to result: O(n)
  -> Total time to clone 'curr': O(n * n!) 
=> Overall: O(n * n!) + O(n * n!) = O(n * n!)

2. Space complexity: O(n)
- recursion stack: O(n).
- 'curr': O(n).
- 'used': O(n).
"""

# === (Extra) Proof: n + n*(n - 1) + ... n! ~~ e ===
""" 
n + n*(n - 1) + ... n!
= n! + n*(n-1)*...*3*2 + ... + n*(n-1) + n
= n! * (1 + 1/1! + 1/2! + ... + 1/(n-1)!)

Taylor series expansion for Euler's number:
. e^x = sum(x^k / k!)
. evaluated at x = 1
  e^1 = 1 + 1/1! + 1/2! + ... + 1/(n-1)!
"""
