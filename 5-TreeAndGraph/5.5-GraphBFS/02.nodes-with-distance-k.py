# Given the root of a binary tree,
# a target node target in the tree, and an integer k,
# return an array of the values of all nodes
# that have a distance k from the target node.

from __future__ import annotations


class TreeNode:
    def __init__(self, val: int, left: TreeNode | None, right: TreeNode | None):
        self.val = val
        self.left = left
        self.right = right


# ===== Analyze =====
# - In binary tree, we only have pointers from parents to children
#   -> finding nodes at distance k in target's subtree is easy
#   -> need a different approach to find nodes that are not in the subtree

# ===== Strategy =====
# - Create an undirected graph from the tree:
#   Traverse the tree (DFS or BFS) and find the parent of each node.
#   + Approach 1: Assign every node a parent pointer (mutate).
#   + Approach 2: Use a hashmap to store the parents of the nodes.
# - Perform a BFS starting from target, and return all the nodes
#   that are in queue after k steps

from collections import deque


# Approach 1 (mutate): Assign every node a parent pointer
def distance_k_nodes_impure(root: TreeNode, target: TreeNode, k: int) -> list[int]:
    def dfs(node: TreeNode | None, parent: TreeNode | None):
        """Add a parent pointer for node"""
        if not node:
            return

        node.parent = parent
        dfs(node.left, node)
        dfs(node.right, node)

    # Traverse the tree and add a parent pointer for each node
    dfs(root, None)

    # Start a BFS from target
    queue = deque([target])
    seen = {target}
    distance = 0

    while queue and distance < k:
        current_length = len(queue)

        for _ in range(current_length):
            node = queue.popleft()

            for neighbor in [node.left, node.right, node.parent]:
                if neighbor and neighbor not in seen:
                    seen.add(neighbor)
                    queue.append(neighbor)

        distance += 1

    # Return all node values at distance k
    return [node.val for node in queue]


# ===== Complexity =====
# Time complexity: O(n) - visit each node once, constant work at each node
# Space complexity: O(n) - for recursion call stack, 'queue', 'seen'


# Approach 2 ("safer"): Use a hashmap to store the parents of the nodes.
def distance_k_nodes_pure(root: TreeNode, target: TreeNode, k: int) -> list[int]:
    # Store the parents of the nodes
    # (each node has 1 parent, except for the root)
    parents: dict[TreeNode, TreeNode | None] = {}
    # Note:
    # - objects in Python are hashable by default
    # - their hash value is derived from their object identity

    def dfs(node: TreeNode | None, parent: TreeNode | None):
        """Record parent for node"""
        if not node:
            return

        parents[node] = parent
        dfs(node.left, node)
        dfs(node.right, node)

    # Traverse the tree and record parent for each node
    dfs(root, None)

    # Start a BFS from target
    queue = deque([target])
    seen = {target}
    distance = 0

    while queue and distance < k:
        current_length = len(queue)

        for _ in range(current_length):
            node = queue.popleft()

            for neighbor in [node.left, node.right, parents[node]]:
                if neighbor and neighbor not in seen:
                    seen.add(neighbor)
                    queue.append(neighbor)

        distance += 1

    # Return all node values at distance k
    return [node.val for node in queue]


# ===== Complexity =====
# Time complexity: O(n) (same as approach 1)
# Space complexity: O(n) (same as approach 1 + space for 'parent_dict')
