from collections import deque


class TreeNode:
    def __init__(self, val, left, right):
        self.val = val
        self.left = left
        self.right = right


def bfs(root: TreeNode):
    queue = deque([root])

    while len(queue) > 0:
        node = queue.popleft()
        print(node.val)

        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)


# ===== Without using built-in deque =====
#
# - Use 2 arrays as follow:
#   + 1 array (queue) for nodes of the current level
#   + 1 array (next_queue) for nodes of the next level
#   -> reassign next_queue to queue after processing the current level
#      (avoid shifting elements when dequeue)


def bfs_with_2_queues(root: TreeNode):
    queue = [root]

    while len(queue) > 0:
        # Use next_queue to collect nodes of the next level
        next_queue = []

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


# ===== Analyze =====
#
# Time complexity:
# - With an efficient queue, the dequeue and enqueue operations are O(1)
# - We visit each node only once
# -> Overall: O(n) - same as DFS
