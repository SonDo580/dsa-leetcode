# Given the head of a sorted linked list,
# delete all duplicates such that each element appears only once.
# Return the linked list sorted as well.

# Example 1:
# Input: head = [1,1,2]
# Output: [1,2]

# Example 2:
# Input: head = [1,1,2,3,3]
# Output: [1,2,3]

# Constraints:
# The number of nodes in the list is in the range [0, 300].
# -100 <= Node.val <= 100
# The list is guaranteed to be sorted in ascending order.


class ListNode:
    def __init__(self, val) -> None:
        self.val = val
        self.next = None


def delete_duplicates(head: ListNode) -> ListNode:
    if head is None:
        return head

    slow = head
    fast = head.next

    while fast is not None:
        # skip duplicate values
        while fast is not None and fast.val == slow.val:
            fast = fast.next
        slow.next = fast

        # move slow to current position of fast
        slow = fast

    return head

# ====================
# Improve: use 1 pointer
def delete_duplicates_v1(head: ListNode) -> ListNode:
    if head is None:
        return head

    current = head
    while current and current.next:
        if current.val == current.next.val:
            # skip the duplicate node
            current.next = current.next.next
        else:
            # move to the next node
            current = current.next

    return head


# Time complexity: O(n)
# Space complexity: O(1) - for 'current' pointer
