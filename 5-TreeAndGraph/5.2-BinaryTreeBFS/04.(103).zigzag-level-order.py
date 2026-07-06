"""
https://leetcode.com/problems/binary-tree-zigzag-level-order-traversal/

Given the root of a binary tree,
return the zigzag level order traversal of its nodes' values.
(i.e., from left to right, then right to left for the next level and alternate between).
"""

"""
Idea:
- Perform level-order traversal.
- At even levels, traverse in reverse direction
  (traverse normally then reverse the collected result).
  -> . method 1: use a variable to indicate direction.
     . method 2: track current level.
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


def zigzag_level_order(root: TreeNode | None) -> list[list[int]]:
    if not root:
        return []

    queue: deque[TreeNode] = deque([root])
    right_to_left: bool = False  # traversal direction for current level
    ans: list[list[int]] = []

    while queue:
        current_length = len(queue)  # number of nodes at current level
        current_vals: list[int] = []  # node values at current level

        for _ in range(current_length):
            node = queue.popleft()
            current_vals.append(node.val)

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        if right_to_left:
            current_vals.reverse()
        ans.append(current_vals)

        # Reverse traversal direction for the next level
        right_to_left = not right_to_left

    return ans


"""
Complexity:
- Let n = number of nodes

1. Time complexity: O(n) 
- Each node is processed once with O(1) work.
- Reversing current_vals across even levels: O(n).

2. Space complexity: O(n) for the queue.
"""


# === Alternative: track current level ===
# (same complexity)
def zigzag_level_order(root: TreeNode | None) -> list[list[int]]:
    if not root:
        return []

    queue: deque[TreeNode] = deque([root])
    ans: list[list[int]] = []
    level: int = 0

    while queue:
        level += 1
        current_length = len(queue)  # number of nodes at current level
        current_vals: list[int] = []  # node values at current level

        for _ in range(current_length):
            node = queue.popleft()
            current_vals.append(node.val)

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        if level & 1 == 0:  # level % 2 == 0
            current_vals.reverse()
        ans.append(current_vals)

    return ans
