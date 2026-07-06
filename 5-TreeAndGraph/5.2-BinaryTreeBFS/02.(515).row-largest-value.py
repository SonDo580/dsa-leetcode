"""
https://leetcode.com/problems/find-largest-value-in-each-tree-row/

Given the root of a binary tree,
return an array of the largest value in each row of the tree.
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


def largest_values(root: TreeNode | None) -> list[int]:
    if not root:
        return []

    result: list[int] = []
    queue: deque[TreeNode] = deque([root])

    while queue:
        current_length = len(queue)  # number of nodes in the current level
        current_max = float("-inf")  # maximum value of the current level

        for _ in range(current_length):
            node = queue.popleft()
            current_max = max(current_max, node.val)

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        result.append(current_max)

    return result


"""
Complexity:
- Let n = number of nodes

1. Time complexity: O(n) (each node is processed once)
2. Space complexity: O(n) for the queue
"""
