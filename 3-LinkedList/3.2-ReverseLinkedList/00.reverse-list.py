class ListNode:
    def __init__(self, val):
        self.val = val
        self.next: ListNode | None = None


def reverse_list(head: ListNode) -> ListNode:
    prev: ListNode | None = None
    current = head

    while current:
        next_node = current.next  # save next node
        current.next = prev  # reverse direction of pointer
        prev = current  # set current node as 'prev' of next node
        current = next_node  # move on

    return prev


"""
Complexity:
1. Time complexity: O(n)
2. Space complexity: O(1)
"""
