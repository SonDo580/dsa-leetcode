# Given the root of a binary tree,
# find the number of nodes that are good.
# A node is good if the path between the root and
# the node has no nodes with a greater value.


class TreeNode:
    def __init__(self, val, left, right):
        self.val = val
        self.left = left
        self.right = right


def count_good_nodes_recursive(root: TreeNode) -> int:
    def dfs(node, current_max):
        """
        Return the number of good nodes in the subtree rooted at node,
        where the maximum value between root and node is current_max.
        """

        # If there are no nodes, there are no good nodes
        if not node:
            return 0

        # Count good nodes in the left and right subtrees
        left_count = dfs(node.left, max(current_max, node.val))
        right_count = dfs(node.right, max(current_max, node.val))

        count = left_count + right_count

        # Check if the current node is a good node
        if node.val >= current_max:
            count += 1

        return count

    return dfs(root, float("-inf"))


def count_good_nodes_iterative(root: TreeNode) -> int:
    # If there are no nodes, there are no good nodes
    if not root:
        return 0

    # Store the node and current maximum value between it and the root
    stack = [(root, float("-inf"))]
    count = 0

    while len(stack) > 0:
        node, current_max = stack.pop()

        # Check if the current node is a good node
        if node.val >= current_max:
            count += 1

        # Add the left and right nodes to the stack
        if node.left:
            stack.append((node.left, max(current_max, node.val)))
        if node.right:
            stack.append((node.right, max(current_max, node.val)))

    return count


# ===== Analysis =====
# Time complexity: O(n) where n is the number of nodes

# Space complexity: proportional to the height of the tree
# - worst case: O(n) when the tree is a straight line
# - best case: Ω(log n) when the tree is 'complete'

# complete tree: all nodes have 0 or 2 children and each level except the last is full
