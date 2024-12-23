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


# ===== Analyze =====
#
# Time complexity:
# - With an efficient queue, the dequeue and enqueue operations are O(1)
# - We visit each node only once
# -> Overall: O(n) - same as DFS
