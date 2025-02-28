# Given the root of a binary tree,
# imagine yourself standing on the right side of it.
# Return the values of the nodes you can see ordered from top to bottom.

# Reframe: Find values of all rightmost nodes at each level

from collections import deque


class TreeNode:
    def __init__(self, val, left, right):
        self.val = val
        self.left = left
        self.right = right


def right_side_view(root: TreeNode) -> list[int]:
    if not root:
        return []

    result = []
    queue = deque([root])

    while queue:
        current_length = len(queue)

        # add value of the rightmost node for the current level
        result.append(queue[-1].val)

        # process all nodes for the current level
        for _ in range(current_length):
            node = queue.popleft()

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

    return result


# ===== Analyze =====
#
# Time complexity: O(n)
# - we visit each node only once, and O(1) work is done at each node
#
# Space complexity: O(n)
# - if the binary tree is 'perfect', the last level contains n/2 nodes
# -> the queue could hold up to O(n) nodes
