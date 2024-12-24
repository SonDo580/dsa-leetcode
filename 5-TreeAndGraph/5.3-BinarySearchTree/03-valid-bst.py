# Given the root of a binary tree, determine if it is a valid BST.

# ===== Note =====
# - In a BST, all subtrees are also BSTs
# - An empty tree is technically a BST


class TreeNode:
    def __init__(self, val, left, right):
        self.val = val
        self.left = left
        self.right = right


def is_valid_bst_recursive(root: TreeNode) -> bool:
    def dfs(node, low, high):
        # An empty tree is a BST
        if not node:
            return True

        # (low, high) is the interval for allowed values
        if not (low < node.val < high):
            return False

        # all nodes in the left subtree should be less than node.val
        left_is_bst = dfs(node.left, low, node.val)

        # all nodes in the left subtree should be greater than node.val
        right_is_bst = dfs(node.right, node.val, high)

        # the left and right subtree must also be BSTs
        return left_is_bst and right_is_bst

    # the root node can be any value since it has no parents
    return dfs(root, float("-inf"), float("inf"))


def is_valid_bst_iterative(root: TreeNode) -> bool:
    stack = [(root, float('-inf'), float('inf'))]

    while len(stack) > 0:
        node, low, high = stack.pop()

        if not (low < node.val < high):
            return False

        if node.left:
            stack.append((node.left, low, node.val))

        if node.right:
            stack.append((node.right, node.val, high))

    return True

# ===== Analyze =====
# - Time and space complexity is O(n)
