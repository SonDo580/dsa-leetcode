# Given the root of a binary tree,
# find the maximum value v for which there exist different nodes a and b
# where v = |a.val - b.val| and a is an ancestor of b.
#
# A node a is an ancestor of b if either:
# any child of a is equal to b or any child of a is an ancestor of b.

# Example 1:
# Input: root = [8,3,10,1,6,null,14,null,null,4,7,13]
# 8 -> 3 -> 1
#   |    |-> 6 -> 4
#   |          |-> 7
#   |-> 10 -> .
#          |-> 14 -> 13
#                 |-> .
# Output: 7
# Explanation: We have various ancestor-node differences, some of which are given below :
# |8 - 3| = 5
# |3 - 7| = 4
# |8 - 1| = 7
# |10 - 13| = 3
# Among all possible differences, the maximum value of 7 is obtained by |8 - 1| = 7.

# Example 2:
# Input: root = [1,null,2,null,0,3]
# 1 -> .
#   |-> 2 -> .
#         |-> 0 -> 3
#               |-> .
# Output: 3

# Constraints:
# The number of nodes in the tree is in the range [2, 5000].
# 0 <= Node.val <= 10^5


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


# ===== Strategy =====
# - Find max ancestor difference along each path and select the largest one
#   -> perform DFS to explore all paths
# - Set initial min and max value as the root value.
# - For each node, update the min and max value upto that point.
# - Base case: when we reach a "None" node, the path is "finalized" 
#   -> calculate the max ancestor difference for the whole path.
# - Build up the final result in a "bottom-up" manner: 
#   For each node, compare max ancestor difference of left and right,
#   Take the larger one as max ancestor difference for a path that go through that node.

def max_ancestor_diff_recur(root: TreeNode) -> int:
    def dfs(node: TreeNode | None, min_val: int, max_val: int) -> int:
        """
        min_val: the minimum value along the path to current node
        max_val: the maximum value along the path to current node
        Returns: the maximum ancestor difference among all paths through current node
        """
        if node is None:
            return max_val - min_val

        next_min_val = min(node.val, min_val)
        next_max_val = max(node.val, max_val)

        left_diff = dfs(node.left, next_min_val, next_max_val)
        right_diff = dfs(node.right, next_min_val, next_max_val)
        return max(left_diff, right_diff)

    return dfs(root, root.val, root.val)
