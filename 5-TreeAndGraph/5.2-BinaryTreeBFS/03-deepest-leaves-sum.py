# Given the root of a binary tree, return the sum of values of its deepest leaves.

# Example 1:
# Input: root = [1,2,3,4,5,null,6,7,null,null,null,null,8]
# Output: 15 (7 + 8)

# Example 2:
# Input: root = [6,7,8,2,7,1,3,9,null,1,4,null,null,null,5]
# Output: 19

# Constraints:
# The number of nodes in the tree is in the range [1, 10^4].
# 1 <= Node.val <= 100

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


# ===== Reword =====
# Sum of values of its deepest leaves
# <=> Sum of all node values in the deepest level


from collections import deque


def deepest_leaves_sum(root: TreeNode) -> int:
    queue: deque[TreeNode] = deque([root])
    last_sum = 0  # sum of node values in the last processed level

    while queue:
        current_length = len(queue)  # number of nodes in the current level
        current_sum = 0  # sum of node values in the current level

        for _ in range(current_length):
            node = queue.popleft()
            current_sum += node.val

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        last_sum = current_sum

    return last_sum


# ===== Complexity =====
# 1. Time complexity: O(n)
# - we visit each node once, and O(1) work is done at each node
#
# 2. Space complexity: O(n)
# - if the binary tree is 'perfect', the last level contains n/2 nodes
# -> the queue could hold up to O(n) nodes
