"""
https://leetcode.com/problems/diameter-of-binary-tree/

Given the root of a binary tree, return the length of the diameter of the tree.

The diameter of a binary tree is the length of the longest path between any two nodes in a tree.
This path may or may not pass through the root.

The length of a path between two nodes is represented by the number of edges between them.
"""

from __future__ import annotations


class TreeNode:
    def __init__(
        self, val, left: TreeNode | None = None, right: TreeNode | None = None
    ):
        self.val = val
        self.left = left
        self.right = right


"""
Idea:
- Diameter of a tree is the max value among:
  . diameter of left subtree.
  . diameter of right subtree.
  . length of longest path through root.
- Length of longest path through a node 
  = left_height + right_height
  . child_height: 
    = number of nodes on the longest path from node[child] to a leaf.
    = number of edges on the longest path from node to a leaf if going [child].
- Node height = 1 + max(left_height, right_height)
- Base case: node = None (get past a leaf)
  . diameter = height = 0 (no nodes)
"""


def binary_tree_diameter_recur(root: TreeNode) -> int:
    def dfs(node: TreeNode | None) -> tuple[int, int]:
        """
        Returns:
        - diameter of the current subtree.
        - height of the current subtree
          (number of nodes on longest path from node to a leaf).
        """

        # Base case: get past a leaf
        if not node:
            return 0, 0

        # Calculate diameter and height of left and right subtree
        left_diameter, left_height = dfs(node.left)
        right_diameter, right_height = dfs(node.right)

        # Calculate length of longest path through current node
        max_path_length = left_height + right_height

        # Diameter of the current subtree is the max value among:
        # - diameter of left subtree
        # - diameter of right subtree
        # - length of longest path passing through current node
        diameter = max(max_path_length, left_diameter, right_diameter)

        # Calculate height of current subtree
        height = 1 + max(left_height, right_height)

        return diameter, height

    return dfs(root)[0]  # return the diameter of the whole tree


"""
Complexity:
- Let n = number of nodes
      h = tree height
  . worst case: skewed tree -> O(h) = O(n)
  . best case: complete tree -> O(h) = O(log(n))

1. Time complexity: O(n) (each node is processed once)
2. Space complexity: O(h) for recursion stack 
"""
