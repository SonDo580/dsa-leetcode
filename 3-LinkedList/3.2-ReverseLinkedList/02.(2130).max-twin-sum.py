"""
https://leetcode.com/problems/maximum-twin-sum-of-a-linked-list/

In a linked list of size n, where n is even,
the ith node (0-indexed) of the linked list is known as
the twin of the (n-1-i)th node, if 0 <= i <= (n / 2) - 1.

For example, if n = 4, then node 0 is the twin of node 3,
and node 1 is the twin of node 2.
These are the only nodes with twins for n = 4.

The twin sum is defined as the sum of a node and its twin.

Given the head of a linked list with even length,
return the maximum twin sum of the linked list.
"""


class ListNode:
    def __init__(self, val: int):
        self.val = val
        self.next: ListNode | None = None


# === 1) Convert to array then use 2 pointers ===


def max_twin_sum(head: ListNode | None) -> int:
    # Collect node values into an array
    node_vals: list[int] = []
    current = head
    while current:
        node_vals.append(current.val)
        current = current.next

    max_twin_sum = -1

    # Use 2 pointers from both ends to find max twin sum
    left = 0
    right = len(node_vals) - 1

    while left < right:
        twin_sum = node_vals[left] + node_vals[right]
        max_twin_sum = max(max_twin_sum, twin_sum)
        left += 1
        right -= 1

    return max_twin_sum


"""
Complexity:

1. Time complexity: O(n)
- collect node values: O(n)
- find max twin sum: O(n) 

2. Space complexity: O(n) for 'node_vals' array
"""


# === 2) Other approach - if we are allowed to modify the linked list in-place ===
"""
- Use fast and slow pointer to find the middle (and length n) of the list.
- Perform a reversal on 2nd half of the list.
- Use 2 pointers: 1 points to head, 1 points to tail.
  Iterate n/2 times to find every pair sum
  (after reversal, 2nd half will traverse from tail to middle).
"""


def max_twin_sum(head: ListNode | None) -> int:
    slow = head
    fast = head
    half_n = 0  # half the number of nodes

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        half_n += 1

    # the list is guaranteed to have an even number of nodes
    # -> slow is now the second middle node (start of the second half)

    # reverse the second half
    prev: ListNode | None = None
    current = slow
    while current:
        next_node = current.next  # save next node
        current.next = prev  # reverse pointer direction
        prev = current  # set current node as prev of next node
        current = next_node  # move on

    # prev now points to the original tail of the list

    # pointers to iterate from 2 ends
    from_tail = prev
    from_head = head

    # iterate n/2 times from both sides to find max twin sum
    max_twin_sum = -1
    for _ in range(half_n):
        max_twin_sum = max(max_twin_sum, from_head.val + from_tail.val)
        from_head = from_head.next
        from_tail = from_tail.next

    return max_twin_sum


"""
Complexity:

1. Time complexity: O(n)
- find start of 2nd half: O(n)
- reverse 2nd half: O(n)
- find max twin sum: O(n)

2. Space complexity: O(1)
"""
