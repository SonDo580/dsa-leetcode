# In a linked list of size n, where n is even,
# the ith node (0-indexed) of the linked list is known as
# the twin of the (n-1-i)th node, if 0 <= i <= (n / 2) - 1.
#
# For example, if n = 4, then node 0 is the twin of node 3,
# and node 1 is the twin of node 2.
# These are the only nodes with twins for n = 4.
#
# The twin sum is defined as the sum of a node and its twin.
#
# Given the head of a linked list with even length,
# return the maximum twin sum of the linked list.

# Example 1:
# Input: head = [5,4,2,1]
# Output: 6
# Explanation:
# Nodes 0 and 1 are the twins of nodes 3 and 2, respectively.
# All have twin sum = 6.
# There are no other nodes with twins in the linked list.
# Thus, the maximum twin sum of the linked list is 6.

# Example 2:
# Input: head = [4,2,2,3]
# Output: 7
# Explanation:
# The nodes with twins present in this linked list are:
# - Node 0 is the twin of node 3 having a twin sum of 4 + 3 = 7.
# - Node 1 is the twin of node 2 having a twin sum of 2 + 2 = 4.
# Thus, the maximum twin sum of the linked list is max(7, 4) = 7.

# Example 3:
# Input: head = [1,100000]
# Output: 100001
# Explanation:
# There is only one node with a twin in the linked list having twin sum of 1 + 100000 = 100001.

# Constraint:
# The number of nodes in the list is an even integer in the range [2, 10^5].
# 1 <= Node.val <= 10^5


class ListNode:
    def __init__(self, val) -> None:
        self.val = val
        self.next = None


def max_twin_sum_1(head: ListNode) -> int:
    # Store the node value in an array
    node_vals = []

    # Iterate through the linked list and save node values
    current = head
    while current:
        node_vals.append(current.val)
        current = current.next

    max_sum = -1

    # Use 2 pointers from both ends to find max sum
    left = 0
    right = len(node_vals) - 1

    while left < right:
        sum = node_vals[left] + node_vals[right]
        if sum > max_sum:
            max_sum = sum

        left += 1
        right -= 1

    return max_sum

# Another approach (if we are allow to modify the linked list in-place) 
# - Use fast and slow pointer to find the middle (and length n) of the list
# - Perform a reversal on the second half of the list
# - After reversing the second half, every node is spaced n/2 apart from its twin
# - Use 2 pointers: 1 point to head, 1 point to tail
# - Iterate n/2 times from head and tail to find every pair sum (and the max sum)

def max_twin_sum_2(head: ListNode) -> int:
    slow = head
    fast = head
    half_n = 0 # half the number of nodes

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        half_n += 1

    # the list is guaranteed to have an even number of nodes
    # -> slow is now the second middle node (start of the second half)

    # reverse the second half
    prev = None
    current = slow
    while current:
        next_node = current.next # save the next node
        current.next = prev # reverse the direction of the pointer
        prev = current # set the current node as prev to the next node
        current = next_node # move on

    # prev is now point to the (original) tail of the list 

    # add pointers to iterate from 2 ends
    # (I could have used the same pointers to save space,
    #  but the code will be hard to understand)
    from_tail = prev
    from_head = head

    # iterate n/2 times from both sides to find max sum
    max_sum = -1
    for _ in range(half_n):
        sum = from_head.val + from_tail.val
        if sum > max_sum:
            max_sum = sum

        from_head = from_head.next
        from_tail = from_tail.next

    return max_sum 