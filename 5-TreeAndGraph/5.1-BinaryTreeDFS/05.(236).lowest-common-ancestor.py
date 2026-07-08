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


def lowest_common_ancestor(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
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


# === Another approach ===
"""
- For a node to be a common ancestor of p and q:
  . node is an ancestor of p
  . AND node is an ancestor of q
- For a node to be an ancestor of p:
  . node == p
  . OR node.left is an ancestor of p
  . OR node.right is an ancestor of p
  (Similar for q)

=> Use DFS (post-order traversal) to calculate result of a node
   based on results from its children.
   . Return: (is_ancestor_of_p, is_ancestor_of_q)
   . The lowest common ancestor is the 1st common ancestor found
     through DFS (lower nodes are processed before higher nodes).  
"""


def lowest_common_ancestor(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    ans = None

    def is_ancestor_of_pq(node: TreeNode | None) -> tuple[bool, bool]:
        """Return (is_node_ancestor_of_p, is_node_ancestor_of_q)."""
        nonlocal ans

        # # Optional optimization
        # if ans:  # already found the valid answer
        #     return False, False  # dummy values (not used by higher calls)

        if not node:
            return False, False

        is_left_ancestor_of_p, is_left_ancestor_of_q = is_ancestor_of_pq(node.left)
        is_right_ancestor_of_p, is_right_ancestor_of_q = is_ancestor_of_pq(node.right)
        is_node_ancestor_of_p = (
            node == p or is_left_ancestor_of_p or is_right_ancestor_of_p
        )
        is_node_ancestor_of_q = (
            node == q or is_left_ancestor_of_q or is_right_ancestor_of_q
        )

        # Only record the 1st common ancestor encountered (lowest)
        if not ans and is_node_ancestor_of_p and is_node_ancestor_of_q:
            ans = node

        return is_node_ancestor_of_p, is_node_ancestor_of_q

    is_ancestor_of_pq(root)
    return ans
