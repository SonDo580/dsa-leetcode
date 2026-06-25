"""
https://leetcode.com/problems/middle-of-the-linked-list/

Given the head of a singly linked list,
return the middle node of the linked list.

If there are two middle nodes,
return the second middle node.
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
- middle is at n // 2 (0-based):
  . n is odd -> (n - 1) / 2
  . n is even -> n / 2 (the 2nd middle)
- when 'slow' reaches middle, 'fast' is at :
  . n is odd: 
    0 + 2 * slow_steps = 0 + 2 * ((n - 1) / 2 - 0) = n - 1
    -> at last node
  . n is even:
    0 + 2 * slow_steps = 0 + 2 * (n / 2 - 0) = n
    -> get past last node
"""


def middle_node(head: ListNode | None) -> ListNode | None:
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow


"""
Complexity:
1. Time complexity: O(n)
2. Space complexity: O(1)
"""
