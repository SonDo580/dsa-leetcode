"""
https://leetcode.com/problems/minimum-depth-of-binary-tree/

Given a binary tree, find its minimum depth.
The minimum depth is the number of nodes along the shortest path
from the root node down to the nearest leaf node.
"""

from __future__ import annotations


class TreeNode:
    def __init__(
        self, val, left: TreeNode | None = None, right: TreeNode | None = None
    ):
        self.val = val
        self.left = left
        self.right = right


def min_depth_recursive(root: TreeNode | None) -> int:
    if not root:
        return 0

    left_depth = min_depth_recursive(root.left)
    right_depth = min_depth_recursive(root.right)

    # the current node contribute 1 to the depth
    if not root.left:
        return right_depth + 1
    if not root.right:
        return left_depth + 1
    return min(left_depth, right_depth) + 1


def min_depth_iterative(root: TreeNode | None) -> int:
    if not root:
        return 0

    stack: list[tuple[TreeNode, int]] = [(root, 1)]  # item: (node, current_depth)
    min_depth = float("inf")

    while stack:
        node, depth = stack.pop()

        # node is leaf -> update min depth if needed
        if not node.left and not node.right and depth < min_depth:
            min_depth = depth

        if node.left:
            stack.append((node.left, depth + 1))
        if node.right:
            stack.append((node.right, depth + 1))

    return min_depth


"""
Complexity (both approaches):
- Let n = number of nodes
      h = tree height
  . worst case: skewed tree -> O(h) = O(n)
  . best case: complete tree -> O(h) = O(log(n))

1. Time complexity: O(n) (each node is processed once)
2. Space complexity: O(h) for stack (recursion stack / 'stack') 
"""
