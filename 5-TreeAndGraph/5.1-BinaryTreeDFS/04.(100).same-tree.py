"""
https://leetcode.com/problems/same-tree/

Given the roots of two binary trees p and q,
check if they are the same tree.
Two binary trees are the same tree if they are structurally identical
and the nodes have the same values.
"""

from __future__ import annotations


class TreeNode:
    def __init__(
        self, val: int, left: TreeNode | None = None, right: TreeNode | None = None
    ):
        self.val = val
        self.left = left
        self.right = right


def is_same_tree_recursive(p: TreeNode, q: TreeNode) -> bool:
    # Both are empty trees -> true
    if not p and not q:
        return True

    # 1 tree is empty but the other is not -> false
    if not p or not q:
        return False

    # Values of current nodes are different -> false
    if p.val != q.val:
        return False

    # The left and right subtrees of both trees must also be the same
    return is_same_tree_recursive(p.left, q.left) and is_same_tree_recursive(
        p.right, q.right
    )


def is_same_tree_iterative(p: TreeNode, q: TreeNode) -> bool:
    stack: list[tuple[TreeNode | None, TreeNode | None]] = [
        (p, q)
    ]  # item: pair of subtrees to compare

    while len(stack) > 0:
        p, q = stack.pop()

        # Both trees are empty -> pass current iteration
        if not p and not q:
            continue

        # 1 tree is empty but the other is not -> false
        if not p or not q:
            return False

        # Values of current nodes are different -> false
        if p.val != q.val:
            return False

        stack.append((p.left, q.left))
        stack.append((p.right, q.right))

    return True


"""
Complexity (both approaches):
- Let n = number of nodes
      h = tree height
  . worst case: skewed tree -> O(h) = O(n)
  . best case: complete tree -> O(h) = O(log(n))

1. Time complexity: O(n) (each node is processed once)
2. Space complexity: O(h) for stack (recursion stack / 'stack') 
"""
