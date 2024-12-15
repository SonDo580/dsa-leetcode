# Given the root of a binary tree and an integer targetSum,
# return true if there exists a path from the root to a leaf
# such that the sum of the nodes on the path is equal to targetSum,
# and return false otherwise.


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def has_path_sum(root: TreeNode, target_sum: int) -> bool:
    def dfs(node, current_sum):
        """
        Return true if a path starting with node has a sum
        equal to target_sum, if we already have current_sum
        contributed towards the sum.
        """

        if not node:
            return False

        current_sum += node.val

        # check if the node is a leaf
        if not node.left and not node.right:
            return current_sum == target_sum

        # only 1 path need to be equal to target_sum
        return dfs(node.left, current_sum) or dfs(node.right, current_sum)

    return dfs(root, 0)
