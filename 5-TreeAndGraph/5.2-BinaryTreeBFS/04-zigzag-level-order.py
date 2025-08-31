# Given the root of a binary tree,
# return the zigzag level order traversal of its nodes' values.
# (i.e., from left to right, then right to left for the next level and alternate between).

# Example 1:
# Input: root = [3,9,20,null,null,15,7]
# Output: [[3],[20,9],[15,7]]

# Example 2:
# Input: root = [1]
# Output: [[1]]
# Example 3:

# Input: root = []
# Output: []


from __future__ import annotations


class TreeNode:
    def __init__(
        self,
        val: int = 0,
        left: TreeNode | None = None,
        right: TreeNode | None = None,
    ):
        self.val = val
        self.left = left
        self.right = right


from collections import deque


def zigzag_level_order(root: TreeNode | None) -> list[list[int]]:
    if not root:
        return []

    queue: deque[TreeNode] = deque([root])
    right_to_left: bool = False  # traversal direction for current level
    traversal_order: list[list[int]] = []

    while queue:
        current_length = len(queue)  # number of nodes in current level
        current_order: list[int] = []  # traversal order for current level

        for _ in range(current_length):
            node = queue.popleft()
            current_order.append(node.val)

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        if right_to_left:
            current_order.reverse()
        traversal_order.append(current_order)

        # Reverse traversal direction for the next level
        right_to_left = not right_to_left

    return traversal_order


# ===== Complexity =====
# Let n be the number of nodes in the tree
#
# 1. Time complexity:
# - We visit each node once, and O(1) work is done at each node: O(n)
# - The reversing of current_order across 'even' levels: O(n)
# => Overall: O(n)
#
# 2. Space complexity:
# - If the binary tree is perfect, the last level contains n/2 nodes
#  -> queue and current_order takes O(n) space
# - traversal_order need space for all nodes: O(n)
# => Overall: O(n)
