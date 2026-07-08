"""
https://leetcode.com/problems/path-sum/

Given the root of a binary tree and an integer 'targetSum',
return true if there exists a path from the root to a leaf
such that the sum of the nodes on the path is equal to 'targetSum',
and return false otherwise.
"""

from __future__ import annotations


class TreeNode:
    def __init__(
        self, val: int, left: TreeNode | None = None, right: TreeNode | None = None
    ):
        self.val = val
        self.left = left
        self.right = right


def has_path_sum_recursive(root: TreeNode | None, target_sum: int) -> bool:
    def dfs(node: TreeNode | None, current_sum: int) -> bool:
        """
        Return True if any path through node has sum = target_sum.
        Path from root to node's parent has sum = current_sum
        """
        if not node:
            return False

        current_sum += node.val

        # node is a leaf -> check if path sum == target_sum
        if not node.left and not node.right:
            return current_sum == target_sum

        # Return True if any path through node has sum == target_sum
        return dfs(node.left, current_sum) or dfs(node.right, current_sum)

    return dfs(root, 0)


def has_path_sum_iterative(root: TreeNode| None, target_sum: int) -> bool:
    if not root:
        return False

    stack: list[tuple[TreeNode, int]] = [(root, 0)]  # item: (node, current_sum)

    while len(stack) > 0:
        node, current_sum = stack.pop()
        current_sum += node.val

        # Check sum if node is a leaf
        if not node.left and not node.right:
            if current_sum == target_sum:
                return True

        if node.left:
            stack.append((node.left, current_sum))
        if node.right:
            stack.append((node.right, current_sum))

    return False


"""
Complexity (both approaches):
- Let n = number of nodes
      h = tree height
  . worst case: skewed tree -> O(h) = O(n)
  . best case: complete tree -> O(h) = O(log(n))

1. Time complexity: O(n) (each node is processed once)
2. Space complexity: O(h) for stack (recursion stack / 'stack') 
"""
