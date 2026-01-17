"""
https://leetcode.com/problems/house-robber-iii/

The thief has found himself a new place for his thievery again.
There is only one entrance to this area, called 'root'.

Besides the 'root', each house has one and only one parent house.
After a tour, the smart thief realized that all houses in this place form a binary tree.
It will automatically contact the police if two directly-linked houses were broken into on the same night.

Given the root of the binary tree,
return the maximum amount of money the thief can rob without alerting the police.
"""

"""
Analysis:
- At each node, we can either:
  . rob it -> accumulate the money, cannot rob the left and right houses.
  . skip it -> can rob the left and right houses.
- We can reach a state (node, can_rob) through multiple paths -> use DP.
"""

"""
- Let dp(node, can_rob) be the maximum of money that can be robbed from current subtree,
  where can_rob denotes whether we can rob current node.
- The result is dp(root, True).
- At each node:
  . if not can_rob: can rob the left and right houses
  . if can_rob:
    . skip current house -> can rob the left and right houses
    . rob current house -> accumulate money, cannot rob the left and right houses
    . pick the action that results in more money.
- Base case: node is None -> amount = 0
"""


class TreeNode:
    def __init__(self, val: int):
        self.val = val
        self.left: TreeNode | None = None
        self.right: TreeNode | None = None


# ===== Top-down =====
from functools import cache


def rob(root: TreeNode | None) -> int:
    @cache
    def dp(node: TreeNode | None, can_rob: bool) -> int:
        if node is None:
            return 0

        if not can_rob:
            return dp(node.left, True) + dp(node.right, True)

        take = node.val + dp(node.left, False) + dp(node.right, False)
        skip = dp(node.left, True) + dp(node.right, True)
        return max(skip, take)

    return dp(root, True)


"""
Complexity:
- Let n = number of nodes
      h = tree's height

1. Time complexity: O(n * 2) = O(n)

2. Space complexity: O(n)
- memoization table: O(n * 2)
- recursion stack: O(h)
"""


# ===== Optimize space: Post-order traversal =====
"""
- Calculate the results for children before parent.
  Each node is visited exactly once.
  -> Pass the results upward without memoization.
- Instead of using a function with a can_rob boolean, return 2 values:
  . take: max money if we rob this node.
  . skip: max money if we skip this node.
"""


def rob(root: TreeNode | None) -> int:
    def dfs(node: TreeNode | None) -> tuple[int, int]:
        """Return maximum amount of money if we rob or skip this node."""
        if node is None:
            return (0, 0)

        # Visit children first
        left_take, left_skip = dfs(node.left)
        right_take, right_skip = dfs(node.right)

        # Option 1: rob this node -> must skip both children
        take = node.val + left_skip + right_skip

        # Option 2: skip this node -> rob or skip each child
        skip = max(left_take, left_skip) + max(right_take, right_skip)

        return take, skip

    return max(dfs(root))


"""
Complexity:

1. Time complexity: O(n) (each node is visited exactly once)

2. Space complexity: O(h) for recursion stack
"""
