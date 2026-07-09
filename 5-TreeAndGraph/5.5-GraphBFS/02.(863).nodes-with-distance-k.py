"""
https://leetcode.com/problems/all-nodes-distance-k-in-binary-tree/

Given the root of a binary tree,
a target node 'target' in the tree, and an integer k,
return an array of the values of all nodes
that have a distance k from the target node.
"""

from __future__ import annotations


class TreeNode:
    def __init__(self, val: int, left: TreeNode | None, right: TreeNode | None):
        self.val = val
        self.left = left
        self.right = right


"""
Analysis:
- In binary tree, we only have pointers from parents to children
  -> finding nodes at distance k in target's subtree is easy
  -> need a different approach to find nodes that are not in target subtree

Idea:
- Create an undirected graph from the tree:
  Traverse the tree (DFS or BFS) and find the parent of each node.
  . Approach 1: Assign every node a parent pointer (mutate).
  . Approach 2: Use a hashmap to store the parents of the nodes.
- Perform a BFS starting from target, and return all the nodes
  that are in queue after k steps.
"""

from collections import deque


# === Approach 1 (mutate): Assign every node a parent pointer ===
def distance_k_nodes_impure(root: TreeNode, target: TreeNode, k: int) -> list[int]:
    def dfs(node: TreeNode | None, parent: TreeNode | None):
        """Add parent pointer for node."""
        if not node:
            return
        node.parent = parent
        dfs(node.left, node)
        dfs(node.right, node)

    # Create undirected graph: add parent pointer for each node
    dfs(root, None)

    # BFS from target
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


"""
Complexity:
- Let n = number of nodes, h = tree height
  . skewed tree: h = O(n)
  . balanced tree: h = O(log(n))
- Number of edges: E = n - 1

1. Time complexity: O(n) 
- tree DFS: O(n)
- graph BFS: O(n + E) = O(n)

2. Space complexity: O(n + h) 
- tree DFS:
  . recursion stack: O(h)
- graph BFS:
  . 'queue': O(n)
  . 'seen': O(n)
"""


# === Approach 2: Use a hashmap to store the parents ===
def distance_k_nodes_pure(root: TreeNode, target: TreeNode, k: int) -> list[int]:
    # Store the parents of the nodes
    # (each node has 1 parent, except for the root)
    parents: dict[TreeNode, TreeNode | None] = {}

    def dfs(node: TreeNode | None, parent: TreeNode | None):
        """Record parent for node"""
        if not node:
            return
        parents[node] = parent
        dfs(node.left, node)
        dfs(node.right, node)

    # Create undirected graph: record parent for each node
    dfs(root, None)

    # BFS from target
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


"""
Complexity:

1. Time complexity: O(n) 
- tree DFS: O(n)
- graph BFS: O(n + E) = O(n)

2. Space complexity: O(n + h)
- 'parents' dict: O(n)
- tree DFS:
  . recursion stack: O(h)
- graph BFS: 
  . 'queue': O(n)
  . 'seen': O(n)
"""


# === Approach 3: Tree traversal ===
# (see 'Tree DFS' section)
