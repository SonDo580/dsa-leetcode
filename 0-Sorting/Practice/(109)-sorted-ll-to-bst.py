"""
https://leetcode.com/problems/convert-sorted-list-to-binary-search-tree/

Given the head of a singly linked list where elements are sorted in ascending order,
convert it to a height-balanced binary search tree.
"""

"""
Idea:
- We can collect the nodes of the linked list into an array.
- Build the BST recursively:
  . Pick the middle element as the root (for height-balanced BST).
  . The middle of the left portion is the left child.
  . The middle of the right portion is the right child.
- To avoid stack overflow, build the BST iteratively.
  . Use a queue/stack to do it in breadth-first/depth-first manner
  . Each queue item should store the range, the parent, the side (left or right).
  . In each iteration, find the current root and attach it to parent.
    Then add 2 queue/stack items for 2 sub ranges.
"""

from __future__ import annotations
from collections import deque


class ListNode:
    def __init__(self, val: int = 0, next: ListNode | None = None):
        self.val = val
        self.next = next


class TreeNode:
    def __init__(
        self, val: int = 0, left: TreeNode | None = None, right: TreeNode | None = None
    ):
        self.val = val
        self.left = left
        self.right = right


def sorted_list_to_bst(head: ListNode | None) -> TreeNode | None:
    if not head:
        return None

    nodes: list[int] = []
    current = head
    while current:
        nodes.append(current.val)
        current = current.next

    # Recursive approach can cause stack overflow
    # return _get_root_recur(nodes, 0, len(nodes) - 1)

    return _get_root_iter(nodes)


def _get_root_recur(nodes: list[int], start: int, end: int) -> TreeNode | None:
    """
    Select the middle element as the BST root.
    Recursively do the same for the left and right subtree.
    """
    if start > end:
        return None
    mid = (start + end) // 2
    return TreeNode(
        val=nodes[mid],
        left=_get_root_recur(nodes, start, mid - 1),
        right=_get_root_recur(nodes, mid + 1, end),
    )


def _get_root_iter(nodes: list[int]) -> TreeNode | None:
    """
    Select the middle element as the BST root.
    Iteratively do the same for the left and right subtree.
    Use a queue to expand the tree in breadth-first manner.
    """
    root: TreeNode | None = None

    # Queue item: (start, end, parent, is_left)
    queue: deque[tuple[int, int, TreeNode | None, bool | None]] = deque(
        [(0, len(nodes) - 1, None, None)]
    )

    while queue:
        start, end, parent, is_left = queue.popleft()
        if start > end:
            continue

        mid = (start + end) // 2
        current = TreeNode(val=nodes[mid])

        if parent is None:
            root = current  # Record the root
        elif is_left:
            parent.left = current
        else:
            parent.right = current

        queue.append((start, mid - 1, current, True))
        queue.append((mid + 1, end, current, False))

    return root


"""
Complexity:

1. Time complexity: O(n)
- Collect nodes from linked list: O(n)
- Build BST: O(n)

2. Space Complexity: O(n)
- 'nodes': O(n)
- queue: O(n)
"""
