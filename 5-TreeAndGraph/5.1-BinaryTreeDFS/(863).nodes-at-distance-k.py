"""
https://leetcode.com/problems/all-nodes-distance-k-in-binary-tree/

Given the root of a binary tree, the value of a target node 'target',
and an integer k, return an array of the values of all nodes
that have a distance k from the target node.

You can return the answer in any order.
"""

# === Approach 1: Tree traversal ===
"""
Idea:
- node's depth = number of edges from root to node
- Nodes at distance k from 'target' is either:
  . 1) Nodes at depth k in target subtree.
  . 2) The ancestor at distance k from 'target'.
  . 3) Nodes in opposite branch of an ancestor (doesn't contains 'target').
       If an ancestor is at distance d from 'target',
       nodes at depth k - d on the opposite branch of that ancestor
       is at distance (d + k - d = k) from 'target'.
- In both cases, we need to collect node values at a certain depth:
  . both BFS and DFS can be used.
- To get distance from 'target' to each of its ancestors, use DFS:
  . base case: distance(target, target) = 0
  . distance(parent, target) = distance(child, target) + 1
    if child contains 'target' (distance(child, target) is not None)
"""

from __future__ import annotations
from collections import deque


class TreeNode:
    def __init__(
        self, val: int, left: TreeNode | None = None, right: TreeNode | None = None
    ):
        self.val = val
        self.left = left
        self.right = right


def distance_k(root: TreeNode, target: TreeNode, k: int) -> list[int]:
    ans: list[int] = []

    def _dfs(node: TreeNode | None) -> int | None:
        """
        1) Return distance d from 'node' to 'target'
           (depth of target in current subtree).
           If 'target' is not in current subtree, return None.

        2) Collect node values at distance k from 'target':
        - nodes at depth k in 'target' subtree.
        - nodes at depth d - k in 'node' subtree
          that doesn't contain 'target'.
        """

        # Empty tree doesn't contain 'target'
        if not node:
            return None

        if node == target:  # case (1)
            # Collect nodes at depth k in 'target' subtree
            _collect_vals_dfs_recur(node, depth=0, target_depth=k)
            return 0

        left_dist_to_target = _dfs(node.left)
        right_dist_to_target = _dfs(node.right)

        if left_dist_to_target is None and right_dist_to_target is None:
            # Current subtree doesn't contain 'target'
            return None

        if left_dist_to_target is not None:
            child_dist_to_target = left_dist_to_target
            opposite = node.right
        else:  # right_dist_to_target is not None
            child_dist_to_target = right_dist_to_target
            opposite = node.left
        assert child_dist_to_target is not None

        node_dist_to_target = child_dist_to_target + 1
        remaining_dist = k - node_dist_to_target

        if remaining_dist == 0:  # case (2)
            ans.append(node.val)
        elif remaining_dist > 0:  # case (3)
            _collect_vals_dfs_recur(
                opposite, depth=0, target_depth=remaining_dist - 1
            )  # -1 to exclude the edge from 'node' to 'opposite'

        return node_dist_to_target

    def _collect_vals_dfs_recur(
        node: TreeNode | None, depth: int, target_depth: int
    ) -> None:
        """Collect node values at target_depth of current subtree."""
        if not node:
            return

        if depth == target_depth:
            ans.append(node.val)
            return

        _collect_vals_dfs_recur(node.left, depth + 1, target_depth)
        _collect_vals_dfs_recur(node.right, depth + 1, target_depth)

    def _collect_vals_dfs_iter(root: TreeNode | None, target_depth: int) -> None:
        """Collect node values at target_depth of current subtree."""
        if not root:
            return

        stack: list[tuple[TreeNode, int]] = [(root, 0)]
        while stack:
            node, depth = stack.pop()
            if depth == target_depth:
                ans.append(node.val)
                continue  # skip lower nodes
            if node.left:
                stack.append((node.left, depth + 1))
            if node.right:
                stack.append((node.right, depth + 1))

    def _collect_vals_bfs(root: TreeNode | None, target_depth: int) -> None:
        """Collect node values at target_depth of current subtree."""
        if not root:
            return

        queue: deque[TreeNode] = deque([root])
        level = 0
        while queue:
            # Process all nodes at current level
            curr_len = len(queue)
            for _ in range(curr_len):
                node = queue.popleft()
                if level == target_depth:
                    ans.append(node.val)
                    continue  # skip lower nodes
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

            level += 1

    _dfs(root)
    return ans


"""
Complexity:
- Let n = number of nodes
      h = tree's height

1. Time complexity: O(n) (each node is visited once or twice)

2. Space complexity: O(h) or O(n + h)
- DFS: O(h)
- Collect values: O(h) or O(n)
  . DFS: O(h) for stack (recursion / 'stack')
  . BFS: O(n) for 'queue'
"""


# === Approach 2: Convert to bidirectional graph ===
# (see 'Graph BFS' section)
