"""
https://leetcode.com/problems/binary-tree-level-order-traversal/

Given the root of a binary tree,
return the level order traversal of its nodes' values.
(i.e., from left to right, level by level).
"""

from __future__ import annotations


class TreeNode:
    def __init__(
        self, val, left: TreeNode | None = None, right: TreeNode | None = None
    ):
        self.val = val
        self.left = left
        self.right = right


# ===== Approach 1 =====
"""
- Store nodes along with their depths in the queue.
- Add nodes at the same depth to the same entry in answer.
"""
from collections import deque


def level_order(root: TreeNode | None) -> list[list[int]]:
    if not root:
        return []

    ans: list[list[int]] = []
    queue: deque[tuple[TreeNode, int]] = deque([(root, 0)])

    while queue:
        node, depth = queue.popleft()
        if depth > len(ans) - 1:
            ans.append([node.val])
        else:
            ans[-1].append(node.val)

        if node.left:
            queue.append((node.left, depth + 1))
        if node.right:
            queue.append((node.right, depth + 1))

    return ans


"""
Complexity:
- Let n = number of nodes

1. Time complexity: O(n) (each node is processed once)
2. Space complexity: O(n) for the queue
   (example: a perfect binary tree can contain (n + 1) / 2 nodes
    at the last level)
"""


# ===== Approach 2 =====
"""
- Store nodes in the queue
- Process all nodes in the queue in each iteration.
"""

def level_order(root: TreeNode | None) -> list[list[int]]:
    if not root:
        return []

    ans: list[list[int]] = []
    queue: deque[TreeNode] = deque([root])

    while queue:
        ans.append([])

        for _ in range(len(queue)):
            node = queue.popleft()
            ans[-1].append(node.val)

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

    return ans

"""
Complexity:
1. Time complexity: O(n) (each node is processed once)
2. Space complexity: O(n) for the queue
"""


# ===== Approach 2.1 =====
"""
(Without deque)

- Use 2 arrays as follow:
  . 1 array (queue) for nodes of the current level
  . 1 array (next_queue) for nodes of the next level
  . reassign next_queue to queue after processing the current level
    (avoid shifting elements when dequeue)
"""

def level_order(root: TreeNode | None) -> list[list[int]]:
    if not root:
        return []

    ans: list[list[int]] = []
    queue: list[TreeNode] = [root]

    while queue:
        ans.append([])
        next_queue: list[TreeNode] = []

        for node in queue:
            ans[-1].append(node.val)
            if node.left:
                next_queue.append(node.left)
            if node.right:
                next_queue.append(node.right)
        
        queue = next_queue

    return ans

"""
Complexity:
1. Time complexity: O(n) (each node is processed once)
2. Space complexity: O(n) for 2 queues
"""