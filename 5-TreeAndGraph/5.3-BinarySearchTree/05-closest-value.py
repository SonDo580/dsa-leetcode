# Given the root of a binary search tree and a target value,
# return the value in the BST that is closest to the target.
# If there are multiple answers, print the smallest.

# Example 1:
# Input: root = [4,2,5,1,3], target = 3.714286
# Output: 4

# Example 2:
# Input: root = [1], target = 4.428571
# Output: 1

# Constraints:
# The number of nodes in the tree is in the range [1, 10^4].
# 0 <= Node.val <= 10^9
# -10^9 <= target <= 10^9


from __future__ import annotations


class TreeNode:
    def __init__(
        self,
        val: int,
        left: TreeNode | None = None,
        right: TreeNode | None = None,
    ):
        self.val = val
        self.left = left
        self.right = right


# ===== Implementation =====
# - Perform a DFS
# - If target == current_node.val, just return it
# - If target < current_node.val, only explore the left subtree.
#   If target > current_node.val, only explore the right subtree.
#   Since all nodes in the other subtree have greater distance.
# - Record new min_distance and corresponding value if:
#   + current_node is root (nothing has been recorded)
#   + distance from current_node to target < min_distance so far
#   + distance from current_node to target == min_distance so far,
#     and current_node.val < current value that has min_distance


def closest_value(root: TreeNode, target: float) -> int:
    val_and_min_distance: tuple[int, float] | None = None
    stack: list[TreeNode] = [root]

    while stack:
        node = stack.pop()
        distance = abs(target - node.val)

        if distance == 0:
            return node.val

        if not val_and_min_distance or (
            distance < val_and_min_distance[1]
            or (
                distance == val_and_min_distance[1]
                and node.val < val_and_min_distance[0]
            )
        ):
            val_and_min_distance = (node.val, distance)

        if target < node.val and node.left:
            stack.append(node.left)
        if target > node.val and node.right:
            stack.append(node.right)

    return val_and_min_distance[0]


# ===== Complexity =====
# Let h be the height of the tree, n be the number of nodes
# - for a balanced BST: h ~ log(n)
# - for a skewed BST (like linked-list): h ~ n
#
# 1. Time complexity: O(h)
