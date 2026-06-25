"""
https://leetcode.com/problems/linked-list-cycle/

Given the head of a linked list, determine if the linked list has a cycle.

There is a cycle in a linked list if there is some node in the list
that can be reached again by continuously following the next pointer.
"""

"""
Idea: Use fast and slow pointers
- The 2 pointers are guaranteed to meet if there's a cycle.

Explain:
- When 'slow' enters the loop:
  . if 'fast' is at the same loop-entry node -> detected
  . if the distance from 'fast' to 'slow' is currently X (steps):
    . relative speed: v_fast - v_slow = 2 - 1 = 1.
    . after each iteration, the distance between them is reduced by 1.
    . the pointers will meet when the distance goes to 0.
"""


from __future__ import annotations


class ListNode:
    def __init__(self, val):
        self.val = val
        self.next: ListNode | None = None


def has_cycle(head: ListNode | None) -> bool:
    slow = head
    fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False


"""
Complexity:
1. Time complexity: O(n)
2. Space complexity: O(1)
"""


# === Other solution: hashing (less efficient) ===
def has_cycle_1(head: ListNode | None) -> bool:
    seen: set[ListNode] = set()
    dummy = head
    while dummy:
        if dummy in seen:
            return True
        seen.add(dummy)
        dummy = dummy.next
    return False


"""
Complexity:
1. Time complexity: O(n)
2. Space complexity: O(n) for 'seen'
"""
