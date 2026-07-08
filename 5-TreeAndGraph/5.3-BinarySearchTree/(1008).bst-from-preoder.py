"""
https://leetcode.com/problems/construct-binary-search-tree-from-preorder-traversal/

Given an array of integers 'preorder',
which represents the pre-order traversal of a BST,
construct the tree and return its root.
"""

"""
Idea:
- preorder[0] is the root
- If preorder[i] < preorder[i - 1]
  -> preorder[i] is left child of preorder[i - 1].
- If preorder[i] > preorder[i - 1]
  -> traverse up the ancestor chain of preorder[i - 1]
     to find the lowest ancestor whose value range
     still contains preorder[i],
  -> preorder[i] is right child of that ancestor.

Implement:
- Create node and push (node, subtree value range) to a stack.
- To traverse backward, pop items off the stack.
  (Don't need to revisit left branch once we've moved to right branch,
   since the nodes are visited in pre-order)
"""


from __future__ import annotations


class TreeNode:
    def __init__(
        self, val: int, left: TreeNode | None = None, right: TreeNode | None = None
    ):
        self.val = val
        self.left = left
        self.right = right


def bst_from_preorder_iter(preorder: list[int]) -> TreeNode | None:
    if not preorder:
        return None

    root = TreeNode(preorder[0])

    stack: list[tuple[TreeNode, int, int]] = [
        (root, float("-inf"), float("inf"))
    ]  # stack item: node + value range

    for i in range(1, len(preorder)):
        node = TreeNode(preorder[i])

        if preorder[i] < preorder[i - 1]:
            # - 'node' parent is current top of stack (preorder[i - 1])
            # - attach 'node' as left child of parent
            parent, low, _ = stack[-1]
            parent.left = node

            # add to stack to build 'node' subtree
            stack.append((node, low, parent.val))

        elif preorder[i] > preorder[i - 1]:
            # find lowest ancestor whose value range contains preorder[i]
            while stack:
                _, low, high = stack[-1]
                if preorder[i] > high:
                    stack.pop()
                else:
                    # - before popping:
                    #   . preorder[i] > preorder[i - 1] > low
                    # - as we pop items off the stack:
                    #   . low stays the same if popped item is left child,
                    #   . low decreases if popped item is right child
                    assert preorder[i] > low
                    break

            # - 'node' parent is current top of stack
            # - attach 'node' as right child of parent
            parent, _, high = stack[-1]
            parent.right = node

            # add to stack to build 'node' subtree
            stack.append((node, parent.val, high))

    return root


"""
Complexity:
- Let n = len(preorder) (number of nodes)
      h = tree height
  . worst case: skewed tree -> h = O(n)
  . best case: balanced tree -> h = O(log(n))

1. Time complexity: O(n)
- Each node is pushed once, and popped at most once.
  (The nodes on the right most path are not removed)

2. Space complexity: O(h) for the stack
"""
