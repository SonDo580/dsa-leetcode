# Given the root of a binary tree,
# return an array of the largest value in each row of the tree.

from collections import deque


class TreeNode:
    def __init__(self, val, left, right):
        self.val = val
        self.left = left
        self.right = right


def largest_values(root: TreeNode) -> list[int]:
    if not root:
        return []

    result = []
    queue = deque([root])

    while len(queue) > 0:
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


# ===== Analyze =====
#
# Time complexity: O(n)
# - we visit each node only once, and O(1) work is done at each node
#
# Space complexity: O(n)
# - if the binary tree is 'perfect', the last level contains n/2 nodes
# -> the queue could hold up to O(n) nodes
