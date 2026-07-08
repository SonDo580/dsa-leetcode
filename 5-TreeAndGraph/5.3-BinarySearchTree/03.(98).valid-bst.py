"""
https://leetcode.com/problems/validate-binary-search-tree/

Given the root of a binary tree, determine if it is a valid BST.
"""

"""
Note:
- In a BST, all subtrees are also BSTs.
- An empty tree is considered a BST.
- All nodes in node.left subtree must have val < node.val
- All nodes in node.right subtree must have val > node.val

Idea:
- Each subtree will have a range of allowed values.
- node's allowed value range is (low..high).
  -> . low < node.val < high
     . node.left's value range is (low..node.val)
     . node.right's value range is (node.val..high)
- root's allowed value range is (-inf, inf).
- Note: value range is for the whole subtree, not just subtree root.
"""


from __future__ import annotations


class TreeNode:
    def __init__(
        self, val: int, left: TreeNode | None = None, right: TreeNode | None = None
    ):
        self.val = val
        self.left = left
        self.right = right


def is_valid_bst_recursive_v1(root: TreeNode | None) -> bool:
    def dfs(node: TreeNode | None, low: int, high: int) -> bool:
        """
        Return True if 'node' subtree is a valid BST,
        given allowed value range (low..high).
        """

        # an empty tree is considered a BST
        if not node:
            return True

        # (low..high) is allowed value range
        if not (low < node.val < high):
            return False

        # left subtree's allowed value range: (low..node.val)
        left_is_bst = dfs(node.left, low, node.val)

        # right subtree's allowed value range: (node.val..high)
        right_is_bst = dfs(node.right, node.val, high)

        # the left and right subtrees must also be BSTs
        return left_is_bst and right_is_bst

    return dfs(root, low=float("-inf"), high=float("inf"))


def is_valid_bst_recursive_v2(root: TreeNode | None) -> bool:
    is_bst: bool = True  # can be updated to False once

    def dfs(node: TreeNode | None, low: int, high: int) -> None:
        """
        Check if 'node' subtree is a valid BST,
        given allowed value range (low..high).
        """
        nonlocal is_bst
        if not is_bst:
            return

        # an empty tree is considered a BST
        if not node:
            return

        # (low..high) is allowed value range
        if not (low < node.val < high):
            is_bst = False
            return

        # left subtree's allowed value range: (low..node.val)
        dfs(node.left, low, node.val)
        if not is_bst:
            return

        # right subtree's allowed value range: (node.val..high)
        dfs(node.right, node.val, high)
        if not is_bst:
            return

    dfs(root, low=float("-inf"), high=float("inf"))
    return is_bst


def is_valid_bst_iterative(root: TreeNode | None) -> bool:
    if not root:
        return True

    stack: list[tuple[TreeNode, int, int]] = [(root, float("-inf"), float("inf"))]

    while stack:
        node, low, high = stack.pop()

        if not (low < node.val < high):
            return False

        if node.left:
            stack.append((node.left, low, node.val))

        if node.right:
            stack.append((node.right, node.val, high))

    return True


"""
Complexity (both approaches):
- Let n = number of nodes
      h = tree height
  . skewed tree -> h = O(n)
  . balanced tree -> h = O(log(n))

1. Time complexity: O(n)
- iterative approach can break early.
- recursive-v1 approach must visit and process all nodes.
- recursive-v2 approach must visit all nodes, but can skip processing.

2. Space complexity: O(h) for the stack (recursion / 'stack')
"""


# === Alternative ===
"""
- The subtree 'node' is a valid BST if
  . node.left and node.right are valid BSTs
  . max_val(node.left) < node.val < min_val(node.right)
- Base case:
  . leaf is a valid BST with min_val = max_val = node.val
"""


def is_valid_bst(root: TreeNode | None) -> bool:
    if not root:
        return True

    def dfs(node: TreeNode) -> tuple[bool, int, int]:
        """Return (is_bst, min_val, max_val) for a non-empty tree."""
        # In case node is a leaf
        is_bst = True
        min_val = max_val = node.val

        if node.left:
            left_is_bst, left_min_val, left_max_val = dfs(node.left)
            is_bst = is_bst and left_is_bst and left_max_val < node.val
            min_val = left_min_val

        if node.right:
            right_is_bst, right_min_val, right_max_val = dfs(node.right)
            is_bst = is_bst and right_is_bst and right_min_val > node.val
            max_val = right_max_val

        return is_bst, min_val, max_val

    return dfs(root)[0]    


"""
Complexity:
1. Time complexity: O(n)
2. Space complexity: O(h) for the stack (recursion / 'stack')
"""
