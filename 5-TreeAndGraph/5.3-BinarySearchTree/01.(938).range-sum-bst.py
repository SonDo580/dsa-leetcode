"""
https://leetcode.com/problems/range-sum-of-bst/

Given the root node of a binary search tree
and two integers 'low' and 'high',
return the sum of values of all nodes with a value
in the inclusive range [low, high].
"""

"""
Trivial approach:
- Use BFS or DFS to visit every node, 
  add nodes whose values are between low and high.

Leverage BST property to prune invalid branches:
- If node.val <= low, skip node.left
  (all values in node.left will be < low)
- If node.val >= high, skip node.right
  (all values in node.right will be > high)
"""


from __future__ import annotations


class TreeNode:
    def __init__(
        self, val: int, left: TreeNode | None = None, right: TreeNode | None = None
    ):
        self.val = val
        self.left = left
        self.right = right


def range_sum_bst_recursive(root: TreeNode, low: int, high: int) -> int:
    if not root:
        return 0

    sum = 0

    if low <= root.val <= high:
        sum += root.val

    if root.val > low:
        sum += range_sum_bst_recursive(root.left, low, high)

    if root.val < high:
        sum += range_sum_bst_recursive(root.right, low, high)

    return sum


def range_sum_bst_iterative(root: TreeNode, low: int, high: int) -> int:
    if not root:
        return 0

    sum = 0
    stack: list[TreeNode] = [root]

    while len(stack) > 0:
        node = stack.pop()

        if low <= node.val <= high:
            sum += node.val

        if node.left and node.val > low:
            stack.append(node.left)

        if node.right and node.val < high:
            stack.append(node.right)

    return sum


"""
Complexity:
- Let n = number of nodes
      h = tree height
  . skewed tree -> h = O(n)
  . balanced tree -> h = O(log(n))

1. Time complexity: O(n)
- Worst case: all nodes are valid -> still visit all.
- Average case: prune many invalid branches.

2. Space complexity: O(h) for the stack (recursion / 'stack')
"""
