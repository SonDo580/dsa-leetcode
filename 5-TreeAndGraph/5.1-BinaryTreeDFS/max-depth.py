# Given the root of a binary tree,
# find the length of the longest path from the root to a leaf.

# => Reframe: how many nodes are in the longest path from the root to a left


# Note:
# - in normal context: the depth of the root is 0
# - the 'depth' in this problem is the number of nodes on the path
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def max_depth_recursive(root: TreeNode) -> int:
    if not root:
        return 0

    left_max_depth = max_depth_recursive(root.left)
    right_max_depth = max_depth_recursive(root.right)

    # the current node contribute 1 to the depth
    return 1 + max(left_max_depth, right_max_depth)


def max_depth_iterative(root: TreeNode) -> int:
    if not root:
        return 0

    # associate the current depth with each node on the stack

    stack = [(root, 1)]
    max_depth = 0

    while len(stack) > 0:
        node, depth = stack.pop()
        max_depth = max(max_depth, depth)

        if node.left:
            stack.append((node.left, depth + 1))
        if node.right:
            stack.append((node.right, depth + 1))

    return max_depth

# ===== Analysis =====
# Time complexity: O(n) where n is the number of nodes

# Space complexity: proportional to the height of the tree
# - worst case: O(n) when the tree is a straight line
# - best case: Ω(log n) when the tree is 'complete' 

# complete tree: all nodes have 0 or 2 children and each level except the last is full