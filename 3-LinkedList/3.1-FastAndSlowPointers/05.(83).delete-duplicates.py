"""
https://leetcode.com/problems/remove-duplicates-from-sorted-list/

Given the head of a sorted linked list (ascending order),
delete all duplicates such that each element appears only once.
Return the linked list sorted as well.
"""

from __future__ import annotations


class ListNode:
    def __init__(self, val):
        self.val = val
        self.next: ListNode | None = None


# === 1) fast and slow pointers ===
def delete_duplicates(head: ListNode | None) -> ListNode | None:
    if not head:
        return head

    slow = head # only traverse unique nodes  
    fast = head.next # traverse all nodes, to skip duplicates

    while fast:
        # move 'fast' to the next unique node
        while fast and fast.val == slow.val:
            fast = fast.next
        
        slow.next = fast # detach all duplicate nodes
        slow = fast

    return head


# === 2) Improvement: only use 1 pointer ===
def delete_duplicates(head: ListNode) -> ListNode:
    if not head:
        return head

    current = head
    while current and current.next:
        if current.val == current.next.val:
            # detach the duplicate node (current.next)
            current.next = current.next.next
        else:
            # move to the next unique node
            current = current.next

    return head


"""
Complexity (both approaches):
1. Time complexity: O(n)
2. Space complexity: O(1)
"""
