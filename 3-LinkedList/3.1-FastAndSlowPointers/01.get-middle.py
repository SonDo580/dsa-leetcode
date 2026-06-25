"""
Given the head of a linked list with an odd number of nodes,
return the value of the node in the middle.

For example, given a linked list that represents
1 -> 2 -> 3 -> 4 -> 5, return 3.
"""

from __future__ import annotations


class ListNode:
    def __init__(self, val):
        self.val = val
        self.next: ListNode | None = None


# === slow and fast pointers ===
"""
- Let:
  . 'slow' move 1 step at once.
  . 'fast' move 2 steps at once.
  . number of nodes = n
- the middle is at index n // 2 (0-based)
  n is odd -> middle is at (n - 1) / 2
- when 'slow' reaches middle, 'fast' is at:
  . 0 + 2 * slow_steps = 0 + 2 * ((n - 1) / 2 - 0) = n - 1
    (which is the last node, with next = None)
"""


def get_middle(head: ListNode):
    slow = head
    fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow.val


"""
Complexity:
1. Time complexity: O(n)
2. Space complexity: O(1)
"""


# === Other approaches (less efficient) ===


# - iterate through the linked list once to find the length.
# - iterate from the head again to find the middle.
def get_middle_1(head: ListNode):
    length = 0
    dummy = head
    while dummy:
        length += 1
        dummy = dummy.next

    for _ in range(length // 2):
        head = head.next
    return head.val


"""
Complexity:
1. Time complexity: still O(n) - but need 2 traversals.
2. Space complexity: O(1)
"""


# - convert the linked list into an array
# - get the middle element
def get_middle_2(head: ListNode):
    arr = []
    while head:
        arr.append(head.val)
        head = head.next

    return arr[len(arr) // 2]


"""
Complexity:
1. Time complexity: O(n).
2. Space complexity: O(n) for 'arr'.
"""
