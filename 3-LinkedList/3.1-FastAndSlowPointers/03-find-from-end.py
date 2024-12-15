# Given the head of a linked list and an integer k,
# return the kth node from the end.
#
# For example, given the linked list that represents 1 -> 2 -> 3 -> 4 -> 5
# and k = 2, return the node with value 4, as it is the 2nd node from the end.

# => Solution:
# Use 2 pointers with the gap of k, then move them at the same speed.
# When the ahead pointer reaches the end, the behind pointer is at the desired node.


class ListNode:
    def __init__(self, val) -> None:
        self.val = val
        self.next = None


def find_node(head: ListNode, k: int) -> ListNode | None:
    behind = head
    ahead = head

    # Create a gap of k between ahead and behind pointers
    for _ in range(k):
        # ahead becomes None -> k is greater than the number of nodes
        if not ahead:  
            return None
        ahead = ahead.next

    # Move both pointers at the same speed
    while ahead:
        ahead = ahead.next
        behind = behind.next

    return behind

# Time complexity: O(n)
# Space complexity: O(1)