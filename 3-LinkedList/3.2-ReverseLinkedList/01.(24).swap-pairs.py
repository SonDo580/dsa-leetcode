"""
https://leetcode.com/problems/swap-nodes-in-pairs/

Given the head of a linked list, swap every pair of nodes.
For example, given a linked list 1 -> 2 -> 3 -> 4 -> 5 -> 6,
return a linked list 2 -> 1 -> 4 -> 3 -> 6 -> 5.
"""


class ListNode:
    def __init__(self, val):
        self.val = val
        self.next: ListNode | None = None


def swap_pairs(head: ListNode | None) -> ListNode | None:
    # linked list is empty or has 1 node -> no pairs to swap
    if not head or not head.next:
        return head

    new_head = head.next  # save new head (the second node)
    prev: ListNode | None = None  # point to the first node in a pair

    # keep iterating if there's a full pair
    while head and head.next:
        if prev:
            # connect previous pair to the rest of the list:
            # - point 1st node of previous pair to 2nd node of current pair.
            # - overwrite `head.next = next_node` line from previous iteration.
            prev.next = head.next

        # save pointer to 1st node of current pair
        prev = head

        # save pointer to 1st node of next pair (can be None)
        next_node = head.next.next

        # (current pair) point 2nd node back to 1st node
        head.next.next = head

        # point 1st node of current pair to 1st node of next pair
        # - next_node can be the last node or None,
        #   so we won't have the next iteration
        head.next = next_node

        # move to the next pair
        head = next_node

    return new_head  # the original second node


"""
Complexity:
1. Time complexity: O(n)
2. Space complexity: O(1)
"""
