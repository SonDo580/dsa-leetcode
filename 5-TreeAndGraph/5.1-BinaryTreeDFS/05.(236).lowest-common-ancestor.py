"""
https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/

Given the root of a binary tree and two nodes p and q that are in the tree,
return the lowest common ancestor (LCA) of the two nodes.
The LCA is the lowest node in the tree that has both p and q as descendants
(note: a node is a descendant of itself).
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
Possibilities:
- Empty tree -> no LCA exists
- Root is p or q -> LCA = root
- p and q are in opposite subtrees (1 in 'left', the other in 'right')
  -> LCA = root
- p and q are in the same subtree ('left' or 'right')
  -> LCA is in that subtree
"""


def lowest_common_ancestor_recur(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    def _dfs(node: TreeNode | None) -> TreeNode | None:
        """
        Return the lowest ancestor of p or q in a subtree.

        Attention: result may not be LCA.
        - Propagate result to higher _dfs() call to decide.
        - We can be certain that result is LCA
          only if current subtree is root,
          OR p and q is found in opposite subtrees.
        """

        # Empty tree -> no ancestor exists
        if not node:
            return None

        # p or q is subtree root -> return subtree root
        # (lowest ancestor of p or q, may not be LCA)
        if node == p or node == q:
            return node

        # Check left and right subtrees
        left = _dfs(node.left)
        right = _dfs(node.right)

        # p and q are in opposite subtrees -> LCA = subtree root
        if left and right:
            return node

        # p and q are in the same subtree
        # -> return lowest ancestor of p or q in that subtree
        #    (may not be LCA)
        if left:
            return left
        else:
            return right

    return _dfs(root)


"""
Complexity:
- Let n = number of nodes
      h = tree height
  . worst case: skewed tree -> O(h) = O(n)
  . best case: complete tree -> O(h) = O(log(n))

1. Time complexity: O(n) (each node is processed once)
2. Space complexity: O(h) for recursion stack 
"""
