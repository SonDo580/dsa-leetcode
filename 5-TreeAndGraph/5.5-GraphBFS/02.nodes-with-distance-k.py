# Given the root of a binary tree, 
# a target node target in the tree, and an integer k, 
# return an array of the values of all nodes 
# that have a distance k from the target node.

# ===== Analyze =====
# - In binary tree, we only have pointers from parents to children
#   -> finding nodes at distance k in target's subtree is easy
#   -> need a different approach to find nodes that are not in the subtree

# ===== Strategy =====
# - Traverse the tree and find the parent of each node
#   + Approach 1: Convert the binary tree into an undirected graph 
#     by assigning every node a parent pointer (mutate)
#   + Approach 2: Use a hashmap to store the parents of the nodes
# - Then perform a BFS starting at target, and return all the nodes
#   that are in queue after k steps

from typing import List
from collections import deque

class TreeNode:
    def __init__(self, val, left, right):
        self.val = val
        self.left = left
        self.right = right

def distance_k_nodes_impure(root: TreeNode, target: TreeNode, k: int) -> List[int]:
    def dfs(node, parent):
        """Add a parent pointer for each node"""
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

    while len(queue) > 0 and distance < k:
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