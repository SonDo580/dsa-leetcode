# Given a binary tree, find its minimum depth.
# The minimum depth is the number of nodes along the shortest path 
# from the root node down to the nearest leaf node.
# Note: A leaf is a node with no children.

# Example 1:
# Input: root = [3,9,20,null,null,15,7]
# 3 -> 9
#   |-> 20 -> 15
#          |-> 7
# Output: 2

# Example 2:
# Input: root = [2,null,3,null,4,null,5,null,6]
# Output: 5

# Constraints:
# The number of nodes in the tree is in the range [0, 10^5].
# -1000 <= Node.val <= 1000

class TreeNode:
    def __init__(
        self,
        val: int = 0,
        left: "TreeNode" | None = None,
        right: "TreeNode" | None = None,
    ):
        self.val = val
        self.left = left
        self.right = right


def min_depth_recursive(root: TreeNode | None) -> int:
    if not root:
        return 0

    left_depth = min_depth_recursive(root.left)
    right_depth = min_depth_recursive(root.right)

    if not root.left:
        return right_depth + 1
    if not root.right:
        return left_depth + 1
    return min(left_depth, right_depth) + 1


def min_depth_iterative(root: TreeNode | None) -> int:
    if not root:
        return 0

    stack = [(root, 1)]
    min_depth = float("inf")

    while stack:
        node, depth = stack.pop()
        if not node.left and not node.right and depth < min_depth:
            min_depth = depth

        if node.left:
            stack.append((node.left, depth + 1))
        if node.right:
            stack.append((node.right, depth + 1))

    return min_depth
