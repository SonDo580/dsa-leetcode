"""
Binary Search Tree operations:
- search
- insert
- delete
"""

from __future__ import annotations


class TreeNode:
    def __init__(
        self, val: int, left: TreeNode | None = None, right: TreeNode | None = None
    ):
        self.val = val
        self.left = left
        self.right = right


def search(root: TreeNode | None, val: int) -> TreeNode | None:
    """Lookup node by value."""
    if not root:
        return None

    if val < root.val:
        return search(root.left)
    if val > root.val:
        return search(root.right)
    return root  # val == root.val


def insert(root: TreeNode | None, val: int) -> TreeNode:
    """
    Create node from value and insert it.
    Return the (possibly new) root.
    """
    if not root:
        return TreeNode(val)

    if val < root.val:
        root.left = insert(root.left, val)
    elif val > root.val:
        root.right = insert(root.right, val)
    return root


def delete(root: TreeNode | None, val: int) -> TreeNode | None:
    """
    Delete a node from a tree.
    Return the (possibly new) root.

    There are 3 cases:
    - 1) node has no children: just remove it.
    - 2) node has one child: replace the node with its only child.
    - 3) node has 2 children:
         . find node's successor (leftmost node in node.right)
         . replace node's value with successor's value
         . delete the successor:
           (successor is the leftmost node in node.right
            -> no left child
            -> deletion will hit case 1 or case 2)
    """
    if not root:
        return root

    if val < root.val:
        root.left = delete(root.left, val)
    elif val > root.val:
        root.right = delete(root.right, val)
    else:  # target node found

        # Node has no children or 1 child
        if not root.left:
            return root.right
        if not root.right:
            return root.left

        # Node has 2 children
        successor = _find_min(root.right)
        root.val = successor.val
        root.right = delete(root.right, successor.val)

    return root


def _find_min(node: TreeNode) -> TreeNode:
    """Find the minimum node in a BST (the left-most one)"""
    current = node
    while current.left:
        current = current.left
    return current


"""
Complexity (both search/insert/delete):
- Let n = number of nodes
      h = tree height
  . worst case: skewed tree -> h = O(n)
  . best case: balanced tree -> h = O(log(n))

1. Time complexity: O(h)
2. Space complexity: O(h) for recursion stack
"""
