# Given the root of a binary tree, return the length of the diameter of the tree.
#
# The diameter of a binary tree is the length of the longest path between any two nodes in a tree.
# This path may or may not pass through the root.
#
# The length of a path between two nodes is represented by the number of edges between them.

# Example 1:
# Input: root = [1,2,3,4,5]
# 1 -> 2 -> 4
#   |    |-> 5
#   |-> 3
# Output: 3
# Explanation: 3 is the length of the path [4,2,1,3] or [5,2,1,3].

# Example 2:
# Input: root = [1,2]
# 1 -> 2
# Output: 1

# Constraints:
# The number of nodes in the tree is in the range [1, 10^4].
# -100 <= Node.val <= 100

from __future__ import annotations


class TreeNode:
    def __init__(
        self,
        val: int = 0,
        left: TreeNode | None = None,
        right: TreeNode | None = None,
    ):
        self.val = val
        self.left = left
        self.right = right


# ===== Idea =====
# - Find the longest path that passes through each node in the tree,
#   then choose the longest one.
# - For each node, find the longest possible path to a leaf on both sides,
#   then take the sum.
# - Base case: leaf node -> diameter = 0, max_depth = 0

# ===== Implementation note =====
# - To simplify calculation, let height correspond to number of nodes,
#   instead of number of edges.
# - Consider a node:
#   + left_height is the number of nodes on the longest path from node.left,
#     and also the number of edges starting from node
#   + similar for the right side.
# => length of longest path through node = left_height + right_height
# - Diameter of the current subtree is the max value of:
#   + diameter of left subtree
#   + diameter of right subtree
#   + length of longest path passing through current node
# - Base case can be "None" node, which has height = 0 and diameter = 0.
# - Leaf node now has height = 1, and diameter is still 0 as expected.


def binary_tree_diameter_recur(root: TreeNode) -> int:
    def dfs(node: TreeNode | None) -> tuple[int, int]:
        """
        Returns: - the diameter of the current subtree.
                 - the height of the node (max depth of current subtree).
        Note: height (max depth) here corresponds to number of nodes.
        """
        # "None" node -> diameter = 0; height = 0
        if node is None:
            return 0, 0

        # Calculate diameter and max depth of left and right subtree
        left_diameter, left_max_depth = dfs(node.left)
        right_diameter, right_max_depth = dfs(node.right)

        # Calculate length of longest path through current node
        max_path_length = left_max_depth + right_max_depth

        # Diameter of the current subtree is the max value of:
        # - diameter of left subtree
        # - diameter of right subtree
        # - length of longest path passing through current node
        diameter = max(max_path_length, left_diameter, right_diameter)

        # Calculate max_depth of current subtree
        max_depth = 1 + max(left_max_depth, right_max_depth)

        return diameter, max_depth

    return dfs(root)[0]  # only return the diameter for the whole tree
