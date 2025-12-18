from __future__ import annotations


class TreeNode:
    def __init__(
        self, val, left: TreeNode | None = None, right: TreeNode | None = None
    ):
        self.val = val
        self.left = left
        self.right = right


# ===== Pre-order =====
def pre_order_dfs(root: TreeNode | None):
    if not root:
        return
    print(root.val)
    pre_order_dfs(root.left)
    pre_order_dfs(root.right)


"""
Complexity:
- Let n = number of nodes
      h = tree height

1. Time complexity: O(n) (each node is processed once)
2. Space complexity: O(h) for the recursion stack
"""


def pre_order_dfs_iter(root: TreeNode | None):
    if not root:
        return

    stack: list[TreeNode] = [root]
    while stack:
        node = stack.pop()
        print(node.val)

        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)


"""
Complexity:
1. Time complexity: O(n) (each node is processed once)
2. Space complexity: O(h) for the stack
"""


# ===== In-order =====
def in_order_dfs(root: TreeNode | None):
    if not root:
        return
    in_order_dfs(root.left)
    print(root.val)
    in_order_dfs(root.right)


"""
Complexity:
1. Time complexity: O(n) (each node is processed once)
2. Space complexity: O(h) for the recursion stack
"""


def in_order_dfs_iter(root: TreeNode | None):
    if not root:
        return

    stack: list[tuple[TreeNode, bool]] = [(root, False)]
    while stack:
        node, should_process = stack.pop()
        if should_process:
            print(node.val)
            continue

        if node.right:
            stack.append((node.right, False))
        stack.append((node, True))
        if node.left:
            stack.append((node.left, False))


"""
Complexity:
1. Time complexity: O(n) (each node is processed twice)
2. Space complexity: O(h) for the stack
"""


# ===== Post-order =====
def post_order_dfs(root: TreeNode | None):
    if not root:
        return
    post_order_dfs(root.left)
    post_order_dfs(root.right)
    print(root.val)


"""
Complexity:
1. Time complexity: O(n) (each node is processed once)
2. Space complexity: O(h) for the recursion stack
"""


def post_order_dfs_iter(root: TreeNode | None):
    if not root:
        return

    stack: list[tuple[TreeNode, bool]] = [(root, False)]
    while stack:
        node, should_process = stack.pop()
        if should_process:
            print(node.val)
            continue

        stack.append((node, True))
        if node.right:
            stack.append((node.right, False))
        if node.left:
            stack.append((node.left, False))


"""
Complexity:
1. Time complexity: O(n) (each node is processed twice)
2. Space complexity: O(h) for the stack
"""
