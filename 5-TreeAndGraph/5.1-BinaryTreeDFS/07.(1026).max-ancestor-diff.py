"""
https://leetcode.com/problems/maximum-difference-between-node-and-ancestor/

Given the root of a binary tree,
find the maximum value v for which there exist different nodes a and b
where v = |a.val - b.val| and a is an ancestor of b.

A node a is an ancestor of b if either:
any child of a is equal to b or any child of a is an ancestor of b.
"""

from __future__ import annotations


class TreeNode:
    def __init__(
        self, val: int, left: TreeNode | None = None, right: TreeNode | None = None
    ):
        self.val = val
        self.left = left
        self.right = right


"""
Idea:
- Find max ancestor difference along each path and select the largest one
  -> Perform DFS to explore all paths.
     Find min and max value for each path.
- At each node, update the min and max value on path from root to node.
- Base case: go past a leaf (node = None)
  -> Calculate the max ancestor difference for the whole path.
- Select the larger result between going 'left' and going 'right'
  as max ancestor difference among all paths that go through a node.
"""


def max_ancestor_diff_recur(root: TreeNode | None) -> int:
    def dfs(node: TreeNode | None, min_val: int, max_val: int) -> int:
        """
        min_val: minimum value on path from root to node's parent.
        max_val: maximum value on path from root to node's parent.
        Returns: max ancestor difference among all paths through node.
        """
        if node is None:
            return max_val - min_val

        next_min_val = min(node.val, min_val)
        next_max_val = max(node.val, max_val)

        left_diff = dfs(node.left, next_min_val, next_max_val)
        right_diff = dfs(node.right, next_min_val, next_max_val)
        return max(left_diff, right_diff)

    return dfs(root, min_val=float("inf"), max_val=float("-inf"))


def max_ancestor_diff_iter(root: TreeNode) -> int:
    max_diff = -1  # max ancestor difference of the whole tree

    stack: list[tuple[TreeNode | None, int, int]] = [
        (root, float("inf"), float("-inf"))
    ]  # item: (current node, min_val, max_val)

    while stack:
        node, min_val, max_val = stack.pop()
        if node is None:
            max_diff = max(max_diff, max_val - min_val)
            continue

        next_min_val = min(node.val, min_val)
        next_max_val = max(node.val, max_val)

        stack.append((node.left, next_min_val, next_max_val))
        stack.append((node.right, next_min_val, next_max_val))

    return max_diff


"""
Complexity (both approaches):
- Let n = number of nodes
      h = tree height
  . worst case: skewed tree -> O(h) = O(n)
  . best case: complete tree -> O(h) = O(log(n))

1. Time complexity: O(n) (each node is processed once)
2. Space complexity: O(h) for stack (recursion stack / 'stack') 
"""
