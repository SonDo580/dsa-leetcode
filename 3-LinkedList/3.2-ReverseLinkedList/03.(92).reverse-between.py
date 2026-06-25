"""
https://leetcode.com/problems/reverse-linked-list-ii/

Given the head of a singly linked list and 2 integers 'left' and 'right'
where left <= right, reverse the nodes of the list
from position 'left' to position 'right', and return the reversed list.

Constraints:
1 <= n <= 500
1 <= left <= right <= n
...

Follow up: Could you do it in one pass?
"""


class ListNode:
    def __init__(self, val):
        self.val = val
        self.next: ListNode | None = None


def reverse_between(head: ListNode | None, left: int, right: int) -> ListNode | None:
    if left == right:  # nothing to reverse
        return head

    first_section_last_node = None  # last node before reversed section
    reversed_section_last_node = None  # last node of reversed section

    # move to 'left' node
    i = 1  # 1-based index
    current = head
    while i < left:
        first_section_last_node = current
        current = current.next
        i += 1

    # 'left' node will become last node of reversed section
    reversed_section_last_node = current

    # reverse the list from 'left' up to 'right'
    prev: ListNode | None = None
    while i <= right:
        next_node = current.next  # save next node
        current.next = prev  # reverse pointer direction
        prev = current  # set current node as prev of next node
        current = next_node  # move to next node
        i += 1

    # 'prev' is now 1st node of reversed section
    # 'current' is now 1st node after reversed section (can be None)

    assert prev is not None

    # point last node of the reversed section to 'current'
    reversed_section_last_node.next = current

    if left == 1:
        # there's no nodes before the reversed section
        # -> 1st node of reversed section becomes the new head
        return prev

    # point last node of 1st section to 1st node of reversed section
    first_section_last_node.next = prev

    # return the original head
    return head


"""
Complexity:
1. Time complexity: O(n)
2. Space complexity: O(1)
"""
