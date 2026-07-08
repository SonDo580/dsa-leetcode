"""
https://leetcode.com/problems/minimum-absolute-difference-in-bst/

Given the root of a BST,
return the minimum absolute difference between
the values of any two different nodes in the tree.
"""

"""
Naive approach:
- Go through the tree and put all values in an array.
- Loop over all pairs to find the minimum difference.
-> Time complexity: O(n + n^2) = O(n^2)

Better approach:
- Traverse the tree to collect values into an array.
- Sort the array.
- Iterate over the sorted array and check adjacent elements.
-> Time complexity: O(n + n*log(n) + n) = O(n*log(n))

Leverage BST property:
- Perform in-order traversal to collect node values in sorted order.
- Iterate over the sorted array and check adjacent elements.
-> Time complexity: O(n + n) = O(n)
"""


from __future__ import annotations


class TreeNode:
    def __init__(
        self, val: int, left: TreeNode | None = None, right: TreeNode | None = None
    ):
        self.val = val
        self.left = left
        self.right = right


# === Use recursive in-order DFS ===
def get_minimum_difference(root: TreeNode | None) -> int:
    sorted_vals: list[int] = []

    def _in_order_dfs(node: TreeNode | None) -> None:
        if not node:
            return
        _in_order_dfs(node.left)
        sorted_vals.append(node.val)
        _in_order_dfs(node.right)

    _in_order_dfs(root)

    min_diff = float("inf")
    for i in range(1, len(sorted_vals)):
        min_diff = min(min_diff, sorted_vals[i] - sorted_vals[i - 1])

    return min_diff


"""
Complexity:
- Let n = number of nodes
      h = tree height

1. Time complexity:
- DFS: O(n)
- find min_diff: O(n)

2. Space complexity: O(n + h)
- DFS recursion stack: O(h)
- 'sorted_vals': O(n)
"""


# === Use iterative in-order DFS ===
def get_minimum_difference_iterative(root: TreeNode | None) -> int:
    sorted_vals: list[int] = []
    stack: list[TreeNode] = []
    current: TreeNode | None = root

    while stack or current:
        if current:
            stack.append(current)
            current = current.left
        else:
            current = stack.pop()
            sorted_vals.append(current.val)
            current = current.right

    min_diff = float("inf")
    for i in range(1, len(sorted_vals)):
        min_diff = min(min_diff, sorted_vals[i] - sorted_vals[i - 1])

    return min_diff


"""
Complexity:

1. Time complexity:
- DFS: O(n)
- find min_diff: O(n)

2. Space complexity: O(n + h)
- 'stack': O(h)
- 'sorted_vals': O(n)
"""


# === Optimize further ===
"""
- Find min_diff while performing DFS.
- Don't need to collect all node values.
  Just track the last visited value to calculate min_diff. 
"""


def get_minimum_difference(root: TreeNode | None) -> int:
    last_val: int | None = None
    min_diff = float("inf")

    def _in_order_dfs(node: TreeNode | None) -> None:
        nonlocal last_val
        nonlocal min_diff

        if not node:
            return
        _in_order_dfs(node.left)
        if last_val is not None:
            min_diff = min(min_diff, node.val - last_val)
        last_val = node.val
        _in_order_dfs(node.right)

    _in_order_dfs(root)

    return min_diff


"""
Complexity:

1. Time complexity:
- DFS + find min_diff : O(n)

2. Space complexity: O(h)
- recursion stack: O(h)
"""
