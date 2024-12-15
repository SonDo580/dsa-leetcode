# Given the head of a singly linked list and two integers left and right
# where left <= right, reverse the nodes of the list
# from position left to position right, and return the reversed list.

# Example 1:
# Input: head = [1,2,3,4,5], left = 2, right = 4
# Output: [1,4,3,2,5]

# Example 2:
# Input: head = [5], left = 1, right = 1
# Output: [5]

# Constraints:
# The number of nodes in the list is n.
# 1 <= n <= 500
# -500 <= Node.val <= 500
# 1 <= left <= right <= n

# Follow up: Could you do it in one pass?


class ListNode:
    def __init__(self, val) -> None:
        self.val = val
        self.next = None


def reverse_between(head: ListNode, left: int, right: int) -> ListNode:
    # there's only 1 node to be reversed -> nothing to reverse
    if left == right:
        return head

    first_section_last_node = None  # the last node before the reversed section
    reversed_section_last_node = None  # the last node of the reversed section

    i = 1

    # move to the node at index left
    current = head
    while i < left:
        first_section_last_node = current
        current = current.next
        i += 1

    # the current node at left will be the last node after reversing
    reversed_section_last_node = current

    # reverse the list from left up to right
    prev = None
    while i <= right:
        next_node = current.next  # save the next node
        current.next = prev  # reverse the direction of the pointer
        prev = current  # set the current node as prev for the next node
        current = next_node  # move to the next node
        i += 1

    # 'prev' is now the fist node of the reversed section
    # 'current' is now the first node after the reversed section (can be None)

    # point the last node of the reversed section to 'current'
    reversed_section_last_node.next = current

    if left == 1:
        # there's no nodes before the reversed section
        # -> the fist node (reversed section) becomes the new head 
        return prev
    
    # point the last node (first section) to the first node (reversed section)
    first_section_last_node.next = prev

    # return the original head
    return head