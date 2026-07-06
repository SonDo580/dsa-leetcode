"""
https://leetcode.com/problems/maximum-depth-of-binary-tree/

Given the root of a binary tree,
find the length of the longest path from the root to a leaf.

The depth is the number of nodes on the path.
"""

from __future__ import annotations


class TreeNode:
    def __init__(
        self, val, left: TreeNode | None = None, right: TreeNode | None = None
    ):
        self.val = val
        self.left = left
        self.right = right


def max_depth_recursive(root: TreeNode | None) -> int:
    if not root:
        return 0

    left_max_depth = max_depth_recursive(root.left)
    right_max_depth = max_depth_recursive(root.right)

    # the current node contribute 1 to the depth
    return 1 + max(left_max_depth, right_max_depth)


def max_depth_iterative(root: TreeNode | None) -> int:
    if not root:
        return 0

    stack: list[tuple[TreeNode, int]] = [(root, 1)]  # item: (node, current_depth)
    max_depth = 0

    while len(stack) > 0:
        node, depth = stack.pop()
        max_depth = max(max_depth, depth)

        if node.left:
            stack.append((node.left, depth + 1))
        if node.right:
            stack.append((node.right, depth + 1))

    return max_depth


"""
Complexity (both approaches):
- Let n = number of nodes
      h = tree height
  . worst case: skewed tree -> O(h) = O(n)
  . best case: complete tree -> O(h) = O(log(n))

1. Time complexity: O(n) (each node is processed once)
2. Space complexity: O(h) for stack (recursion stack / 'stack') 
"""
