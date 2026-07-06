from __future__ import annotations


class TreeNode:
    def __init__(
        self, val: int, left: TreeNode | None = None, right: TreeNode | None = None
    ):
        self.val = val
        self.left = left
        self.right = right


# ===== Pre-order =====
# https://leetcode.com/problems/binary-tree-preorder-traversal/


def pre_order_dfs(root: TreeNode | None) -> list[int]:
    vals: list[int] = []

    def _dfs(node: TreeNode | None) -> None:
        if not node:
            return
        vals.append(node.val)
        _dfs(node.left)
        _dfs(node.right)

    _dfs(root)
    return vals


"""
Complexity:
- Let n = number of nodes
      h = tree height = O(n) for skewed tree

1. Time complexity: O(n) (each node is processed once)
2. Space complexity: O(h) for the recursion stack
"""


def pre_order_dfs_iter(root: TreeNode | None) -> list[int]:
    if not root:
        return []

    vals: list[int] = []
    stack: list[TreeNode] = [root]
    while stack:
        node = stack.pop()
        vals.append(node.val)

        # process order: left -> right
        # -> push order: right -> left
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)

    return vals


"""
Complexity:
1. Time complexity: O(n) (each node is processed once)
2. Space complexity: O(h) for the stack
"""


# ===== In-order =====
# https://leetcode.com/problems/binary-tree-inorder-traversal/


def in_order_dfs(root: TreeNode | None) -> list[int]:
    vals: list[int] = []

    def _dfs(node: TreeNode | None) -> None:
        if not node:
            return
        _dfs(node.left)
        vals.append(node.val)
        _dfs(node.right)

    _dfs(root)
    return vals


"""
Complexity:
1. Time complexity: O(n) (each node is processed once)
2. Space complexity: O(h) for the recursion stack
"""


def in_order_dfs_iter(root: TreeNode | None) -> list[int]:
    if not root:
        return []

    vals: list[int] = []
    stack: list[tuple[TreeNode, bool]] = [(root, False)]
    while stack:
        node, should_process = stack.pop()

        # process on the 2nd encounter, not the 1st encounter
        # (after 'right' is fully processed)
        if should_process:
            vals.append(node.val)
            continue  # children are pushed to stack in 1st encounter

        # process order: left -> node -> right
        # -> . push order: right -> node -> left
        #    . re-add node with should_process=True to process on next encounter
        if node.right:
            stack.append((node.right, False))
        stack.append((node, True))
        if node.left:
            stack.append((node.left, False))

    return vals


"""
Complexity:
1. Time complexity: O(n)
   (each node is added/removed twice, processed once)

2. Space complexity: O(h) for the stack
"""


# ===== Post-order =====
# https://leetcode.com/problems/binary-tree-postorder-traversal/


def post_order_dfs(root: TreeNode | None) -> list[int]:
    vals: list[int] = []

    def _dfs(node: TreeNode | None) -> None:
        if not node:
            return
        _dfs(node.left)
        _dfs(node.right)
        vals.append(node.val)

    _dfs(root)
    return vals


"""
Complexity:
1. Time complexity: O(n) (each node is processed once)
2. Space complexity: O(h) for the recursion stack
"""


def post_order_dfs_iter(root: TreeNode | None) -> list[int]:
    if not root:
        return []

    vals: list[int] = []
    stack: list[tuple[TreeNode, bool]] = [(root, False)]
    while stack:
        node, should_process = stack.pop()

        # process on the 2nd encounter, not the 1st encounter
        # (after 'left' and 'right' are fully processed)
        if should_process:
            vals.append(node.val)
            continue  # children are pushed to stack in 1st encounter

        # process order: left -> right -> node
        # -> . push order: node -> right -> left
        #    . re-add node with should_process=True to process on next encounter
        stack.append((node, True))
        if node.right:
            stack.append((node.right, False))
        if node.left:
            stack.append((node.left, False))

    return vals


"""
Complexity:
1. Time complexity: O(n) 
   (each node is added/removed twice, processed once)
2. Space complexity: O(h) for the stack
"""
