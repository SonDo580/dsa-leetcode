# Given the root of a binary tree,
# find the length of the longest path from the root to a leaf.

# => Reframe: how many nodes are in the longest path from the root to a left

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def max_depth(root: TreeNode) -> int:
    if not root:
        return 0

    left_max_depth = max_depth(root.left)
    right_max_depth = max_depth(root.right)

    # the current node contribute 1 to the depth
    return 1 + max(left_max_depth, right_max_depth)
