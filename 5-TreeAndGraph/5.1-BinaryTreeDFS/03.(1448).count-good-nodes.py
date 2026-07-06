"""
https://leetcode.com/problems/count-good-nodes-in-binary-tree/

Given the root of a binary tree,
find the number of nodes that are good.
A node is good if the path between the root and
the node has no nodes with a greater value.
"""

from __future__ import annotations


class TreeNode:
    def __init__(
        self, val: int, left: TreeNode | None = None, right: TreeNode | None = None
    ):
        self.val = val
        self.left = left
        self.right = right


def count_good_nodes_recursive(root: TreeNode) -> int:
    def dfs(node: TreeNode | None, current_max: int) -> int:
        """
        Return the number of good nodes in the subtree rooted at node.
        The maximum value from root to node's parent is current_max.
        """
        if not node:  # no nodes -> no good nodes
            return 0

        # Count good nodes in the left and right subtrees
        left_count = dfs(node.left, max(current_max, node.val))
        right_count = dfs(node.right, max(current_max, node.val))
        count = left_count + right_count

        if node.val >= current_max:  # current node is a good node
            count += 1

        return count

    return dfs(root, current_max=float("-inf"))


def count_good_nodes_iterative(root: TreeNode) -> int:
    stack = [(root, float("-inf"))]  # item: (node, current_max)
    count = 0

    while len(stack) > 0:
        node, current_max = stack.pop()
        if node.val >= current_max:  # current node is a good node
            count += 1

        if node.left:
            stack.append((node.left, max(current_max, node.val)))
        if node.right:
            stack.append((node.right, max(current_max, node.val)))

    return count


"""
Complexity (both approaches):
- Let n = number of nodes
      h = tree height
  . worst case: skewed tree -> O(h) = O(n)
  . best case: complete tree -> O(h) = O(log(n))

1. Time complexity: O(n) (each node is processed once)
2. Space complexity: O(h) for stack (recursion stack / 'stack') 
"""
