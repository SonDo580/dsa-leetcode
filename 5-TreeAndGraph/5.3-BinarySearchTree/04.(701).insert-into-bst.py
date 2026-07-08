"""
https://leetcode.com/problems/insert-into-a-binary-search-tree/

You are given the root node of a binary search tree (BST) and a value to insert into the tree.
Return the root node of the BST after the insertion.
It is guaranteed that the new value does not exist in the original BST.

Notice that there may exist multiple valid ways for the insertion,
as long as the tree remains a BST after insertion.
You can return any of them.
"""

from __future__ import annotations


class TreeNode:
    def __init__(
        self, val: int, left: TreeNode | None = None, right: TreeNode | None = None
    ):
        self.val = val
        self.left = left
        self.right = right


def insert_into_bst_recur(root: TreeNode | None, val: int) -> TreeNode:
    if not root:
        return TreeNode(val)

    if val < root.val:
        root.left = insert_into_bst_recur(root.left, val)
    elif val > root.val:
        root.right = insert_into_bst_recur(root.right, val)
    return root


"""
Complexity:
- Let n = number of nodes
      h = tree height
  . skewed tree -> h = O(n)
  . balanced tree -> h = O(log(n))

1. Time complexity: O(h)
2. Space complexity: O(h) for the recursion stack
"""


def insert_into_bst_iter(root: TreeNode | None, val: int) -> TreeNode:
    if not root:
        return TreeNode(val)

    current = root
    while current:
        if val < current.val:
            # insert into the left subtree
            if not current.left:
                current.left = TreeNode(val)
                break
            current = current.left
        elif val > current.val:
            # insert into the right subtree
            if not current.right:
                current.right = TreeNode(val)
                break
            current = current.right
        else:
            break  # val already exists

    return root


"""
Complexity:
1. Time complexity: O(h)
2. Space complexity: O(1)
"""
