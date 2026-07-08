"""
https://leetcode.com/problems/closest-binary-search-tree-value/

Given the root of a binary search tree and a target value,
return the value in the BST that is closest to the target.
If there are multiple answers, print the smallest.
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
- Perform DFS. Leverage BST property to prune branches.
  . If target == current_node.val, return current_node.val 
    (distance = 0 -> smallest possible). 
  . If target < current_node.val, only explore the left subtree.
    If target > current_node.val, only explore the right subtree.
    All nodes in the opposite subtree will have greater distance to target.
- Record new min_distance and corresponding value if:
  . distance < min_distance OR
    (distance == min_distance AND val < val_with_min_distance)
"""


def closest_value(root: TreeNode, target: float) -> int:
    min_dist = float("inf")
    val_with_min_dist = None

    # Pre-order DFS
    stack: list[TreeNode] = [root]
    while stack:
        node = stack.pop()
        dist = abs(target - node.val)

        if dist == 0:
            return node.val

        if dist < min_dist or (dist == min_dist and node.val < val_with_min_dist):
            # dist == min_dist -> val_with_min_dist is not None
            val_with_min_dist, min_dist = node.val, dist

        # Only explore 1 subtree
        if target < node.val and node.left:
            stack.append(node.left)
        if target > node.val and node.right:
            stack.append(node.right)

    return val_with_min_dist


"""
Complexity:
- Let n = number of nodes
      h = tree height
  . skewed tree -> h = O(n)
  . balanced tree -> h = O(log(n))

1. Time complexity: O(h)
2. Space complexity: O(h) for the stack (recursion / 'stack')
"""
