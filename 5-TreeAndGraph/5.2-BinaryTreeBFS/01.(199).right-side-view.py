"""
https://leetcode.com/problems/binary-tree-right-side-view/

Given the root of a binary tree,
imagine yourself standing on the right side of it.
Return the values of the nodes you can see ordered from top to bottom.
"""

"""
Reframe problem: Find value of rightmost node at each level
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


def right_side_view(root: TreeNode | None) -> list[int]:
    if not root:
        return []

    result: list[int] = []
    queue: deque[TreeNode] = deque([root])

    while queue:
        current_length = len(queue)

        # Record value of the rightmost node at current level
        result.append(queue[-1].val)

        # Process all nodes at current level
        for _ in range(current_length):
            node = queue.popleft()
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

    return result


"""
Complexity:
- Let n = number of nodes

1. Time complexity: O(n) (each node is processed once)
2. Space complexity: O(n) for the queue
"""
