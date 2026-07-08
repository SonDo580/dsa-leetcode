"""
https://leetcode.com/problems/kth-smallest-element-in-a-bst/

Given the root of a binary search tree, and an integer k, return the kth smallest value (1-indexed) of all the values of the nodes in the tree.

Follow up: If the BST is modified often (i.e., we can do insert and delete operations)
and you need to find the kth smallest frequently, how would you optimize?
"""

from __future__ import annotations


class TreeNode:
    def __init__(self, val: int, left: TreeNode | None, right: TreeNode | None):
        self.val = val
        self.left = left
        self.right = right


"""
Idea:
- Perform in-order traversal to process nodes in sorted order.
- Stop on the kth node and return its value.
"""


def kth_smallest_iter_v1(root: TreeNode, k: int) -> int:
    count = 0
    stack: list[tuple[TreeNode, bool]] = [(root, False)]

    while stack:
        node, should_process = stack.pop()
        if should_process:
            count += 1
            if count == k:
                return node.val
            continue

        if node.right:
            stack.append((node.right, False))
        stack.append((node, True))
        if node.left:
            stack.append((node.left, False))

    raise Exception("unreachable")  # constraint: k <= n


def kth_smallest_iter_v2(root: TreeNode, k: int) -> int:
    count = 0
    stack: list[TreeNode] = []
    current: TreeNode | None = root

    while stack or current:
        if current:
            # keep going left if possible

            # push 'current' onto stack to process later
            # (after all nodes in 'current.left' are processed)
            stack.append(current)

            current = current.left
        else:
            # get past a leaf -> backtrack

            # process the closest ancestor
            current = stack.pop()
            count += 1
            if count == k:
                return current.val

            # explore the right subtree
            current = current.right

    raise Exception("unreachable")  # constraint: k <= n


"""
Complexity (both approaches):
- Let n = number of nodes
      h = tree height
  . worst case: skewed tree -> h = O(n)
  . best case: balanced tree -> h = O(log(n))

1. Time complexity: O(k)
2. Space complexity: O(h) for 'stack'
"""


# === Follow-up: What if the BST is modified often ===
"""
- Record the number of nodes in the subtree at each subtree root.
  -> allow skipping entire subtrees while searching.
- After inserting/deleting, traverse up the ancestor chain to  
  update node_count recorded at each ancestor.
  . node.count = 1 + node.left.count + node.right.count

- Find kth smallest element: 
  Perform DFS. At each node:
  . If k == node.left.count + 1, node is target.
    -> return node.val
  . If k <= node.left.count, search for target in node.left:
    . keep k the same
  . If k > node.left.count + 1, search for target in node.right:
    . remaining_k = k - (node.left.count + 1)
"""


class ExtendedTreeNode:
    def __init__(self, val: int):
        self.val = val
        self.left: ExtendedTreeNode | None = None
        self.right: ExtendedTreeNode | None = None

        # === metadata ===
        self.count: int = 1  # number of nodes in subtree


def count(node: ExtendedTreeNode | None) -> int:
    """Return number of nodes in subtree."""
    return node.count if node else 0


def insert(root: ExtendedTreeNode | None, val: int) -> ExtendedTreeNode:
    """
    Return tree root after insert. Ignore if val already exists.
    Update metadata (count) for involved subtrees.
    """
    if not root:
        return ExtendedTreeNode(val=val)

    if root.val == val:
        return root

    if val < root.val:
        root.left = insert(root.left, val)
    else:
        root.right = insert(root.right, val)

    root.count = 1 + count(root.left) + count(root.right)
    return root


def delete(root: ExtendedTreeNode | None, val: int) -> ExtendedTreeNode:
    """
    Return tree root after delete. Ignore if val doesn't exist.
    Update metadata (count) for involved subtrees.
    """
    if not root:
        return root

    if val < root.val:
        root.left = delete(root.left, val)
    elif val > root.val:
        root.right = delete(root.right, val)
    else:  # root is target node
        # target node has no children or exactly 1 child
        if not root.left:
            return root.right
        if not root.right:
            return root.left

        # target node has 2 children
        # -> replace target node with its successor
        successor = _find_min(root.right)
        root.val = successor.val
        root.right = delete(root.right, successor.val)

    root.count = 1 + count(root.left) + count(root.right)
    return root


def _find_min(node: ExtendedTreeNode) -> ExtendedTreeNode:
    """Find the minimum node in a BST (the left-most one)"""
    current = node
    while current.left:
        current = current.left
    return current


def follow_up_kth_smallest(root: ExtendedTreeNode, k: int) -> int:
    # return follow_up_kth_smallest_recur(root, k)
    return follow_up_kth_smallest_iter(root, k)


def follow_up_kth_smallest_recur(root: ExtendedTreeNode, k: int) -> int:
    ans = None

    def _pre_order_dfs(node: ExtendedTreeNode, k: int) -> None:
        nonlocal ans
        if ans is not None:
            return

        left_count = count(node.left)
        if k == left_count + 1:
            ans = node.val
            return

        if k <= left_count:
            _pre_order_dfs(node.left, k)
        else:
            _pre_order_dfs(node.right, k - left_count - 1)

    assert 1 <= k <= root.count
    _pre_order_dfs(root, k)
    return ans


def follow_up_kth_smallest_iter(root: ExtendedTreeNode, k: int) -> int:
    assert 1 <= k <= root.count

    stack: list[tuple[ExtendedTreeNode, int]] = [(root, k)]
    while stack:
        node, remaining_k = stack.pop()
        left_count = count(node.left)
        if remaining_k == left_count + 1:
            return node.val

        if remaining_k <= left_count:
            assert node.left
            stack.append((node.left, remaining_k))
        else:
            assert node.right
            stack.append((node.right, remaining_k - left_count - 1))

    raise Exception("Unreachable")


"""
Complexity:

1. Time complexity: O(h)
- only explore 1 branch at each node.

2. Space complexity: O(h) for the stack (recursion / 'stack')
"""


# === Test follow-up implementation ===
import random

if __name__ == "__main__":
    N_VALS = 10
    vals = [i for i in range(N_VALS)]

    for _ in range(5):
        # shuffle to generate different tree structures
        random.shuffle(vals)

        root: ExtendedTreeNode | None = None

        # insert values
        for val in vals:
            root = insert(root, val)
        assert root.count == N_VALS

        # try inserting duplicates
        for val in range(3):
            root = insert(root, val)
        assert root.count == N_VALS

        # try deleting not-existed values
        for val in range(N_VALS, N_VALS + 3):
            root = delete(root, val)
        assert root.count == N_VALS

        # the kth smallest value should be the same for different tree structures
        for k in range(1, N_VALS + 1):
            assert follow_up_kth_smallest(root, k) == k - 1

        # delete some values
        for val in range(3, 7):
            root = delete(root, val)
        assert root.count == N_VALS - 4

        # the kth smallest value should be the same for different tree structures
        for k in range(1, 4):
            assert follow_up_kth_smallest(root, k) == k - 1
        for k in range(4, root.count + 1):
            assert follow_up_kth_smallest(root, k) == k - 1 + 4
