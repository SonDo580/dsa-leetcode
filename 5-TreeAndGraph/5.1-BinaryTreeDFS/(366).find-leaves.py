"""
https://leetcode.com/problems/find-leaves-of-binary-tree/

Given the root of a binary tree, collect a tree's nodes as if you were doing this:
- Collect all the leaf nodes.
- Remove all the leaf nodes.
- Repeat until the tree is empty.
"""

"""
Idea:
- Collect nodes with the same height into the same group
  (node height = max number of edges from node to a leaf)
  . group index in result array = node height
- Perform DFS (post-order traversal):
  . height = 1 + max(left_height, right_height)
  . base case: leaf height = 0 
"""


from __future__ import annotations


class TreeNode:
    def __init__(
        self, val, left: TreeNode | None = None, right: TreeNode | None = None
    ):
        self.val = val
        self.left = left
        self.right = right


def find_leaves(root: TreeNode | None) -> list[list[int]]:
    ans: list[list[int]] = []

    def _dfs(node: TreeNode | None) -> int:
        """
        Return current node height.
        Add node value to the ans[height] entry.
        """
        if not node:
            return -1

        left_height = _dfs(node.left)
        right_height = _dfs(node.right)
        height = 1 + max(left_height, right_height)

        if height == len(ans):  # need new entry
            ans.append([])
        ans[height].append(node.val)

        return height

    _dfs(root)
    return ans


"""
Complexity:
- Let n = number of nodes
      h = tree height
  . worst case: skewed tree -> h = O(n)
  . best case: balanced tree -> h = O(log(n))

1. Time complexity: O(n) (each node is processed once)
2. Space complexity: O(h) for the recursion stack
"""
