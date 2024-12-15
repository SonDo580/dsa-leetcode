# Given the head of a linked list, swap every pair of nodes.
# For example, given a linked list 1 -> 2 -> 3 -> 4 -> 5 -> 6,
# return a linked list 2 -> 1 -> 4 -> 3 -> 6 -> 5.


class ListNode:
    def __init__(self, val) -> None:
        self.val = val
        self.next = None


def swap_pairs(head: ListNode) -> ListNode:
    # Edge case: linked list has 0 or 1 node
    if not head or not head.next:
        return head

    # the second node will become the head
    dummy = head.next

    # point to the first node in a pair
    prev = None

    # keep iterating if there's a full pair
    while head and head.next:
        if prev:
            # connect the previous pair to the rest of the list
            # - point the first node (previous pair) to the second node (current pair)
            # - this will overwrite this line from the previous iteration: `head.next = next_node`,
            #   which point the first node (previous pair) to the first node (current pair)
            prev.next = head.next

        # save a pointer to the first node (current pair)
        prev = head

        # save a pointer to the first node (next pair)
        next_node = head.next.next

        # (current pair) point the second node back to the first node
        head.next.next = head

        # point the first node (current pair) to the first node (next pair)
        # - this is needed because next_node can be the last node
        #   (so we won't have the next iteration)
        head.next = next_node

        # move to the next pair
        head = next_node

    # return the second node
    return dummy


# Time complexity: O(n)
# Space complexity: O(1)
