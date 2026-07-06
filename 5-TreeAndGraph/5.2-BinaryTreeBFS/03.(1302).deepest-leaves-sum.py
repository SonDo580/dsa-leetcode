"""
https://leetcode.com/problems/deepest-leaves-sum/

Given the root of a binary tree,
return the sum of values of its deepest leaves.
"""

"""
Reframe problem: Find sum of node values at last level.
"""

from __future__ import annotations
from collections import deque


class TreeNode:
    def __init__(
        self, val: int, left: TreeNode | None = None, right: TreeNode | None = None
    ):
        self.val = val
        self.left = left
        self.right = right


def deepest_leaves_sum(root: TreeNode | None) -> int:
    if not root:
        return 0

    queue: deque[TreeNode] = deque([root])
    current_sum = 0  # sum of node values in the current level

    while queue:
        current_sum = 0  # reset for each new level
        current_length = len(queue)  # number of nodes at current level
        for _ in range(current_length):
            node = queue.popleft()
            current_sum += node.val

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

    return current_sum


"""
Complexity:
- Let n = number of nodes

1. Time complexity: O(n) (each node is processed once)
2. Space complexity: O(n) for the queue
"""
