from collections import deque


from __future__ import annotations


class TreeNode:
    def __init__(
        self, val, left: TreeNode | None = None, right: TreeNode | None = None
    ):
        self.val = val
        self.left = left
        self.right = right


def bfs(root: TreeNode):
    queue: deque[TreeNode] = deque([root])

    while len(queue) > 0:
        node = queue.popleft()
        print(node.val)

        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)


"""
Complexity:
- Let n = number of nodes

1. Time complexity: O(n) (each node is processed once)
2. Space complexity: O(n) for the queue
"""


# ===== Without deque =====
"""
- Use 2 arrays as follow:
  . 1 array (queue) for nodes of the current level
  . 1 array (next_queue) for nodes of the next level
  . reassign next_queue to queue after processing the current level
    (avoid shifting elements when dequeue)
"""


def bfs_with_2_queues(root: TreeNode):
    queue: list[TreeNode] = [root]

    while len(queue) > 0:
        # Use next_queue to collect nodes in the next level
        next_queue: list[TreeNode] = []

        for node in queue:
            # Process current node
            print(node.val)

            # Add the children to next_queue
            if node.left:
                next_queue.append(node.left)
            if node.right:
                next_queue.append(node.right)

        # Re-assign next_queue to queue
        queue = next_queue


"""
Complexity:
1. Time complexity: O(n) (each node is processed once)
2. Space complexity: O(n) for 2 queues
"""
