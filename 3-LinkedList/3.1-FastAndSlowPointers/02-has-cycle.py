# Given the head of a linked list, determine if the linked list has a cycle.
# 
# There is a cycle in a linked list if there is some node in the list 
# that can be reached again by continuously following the next pointer.

# Solution: Use fast and slow pointers

# Explain:
# - The 2 pointers are guaranteed to meet if there is a cycle
# - When the slow pointer enters the loop:
# + if the fast pointer is at the same node as the slow pointer -> detected
# + if the distance between the 2 pointers is X (steps):
#   . the relative speed between them is 1
#   . after each iteration, the distance between them is reduced by 1 
#   . the pointers will meet when the distance goes to 0

class ListNode:
    def __init__(self, val) -> None:
        self.val = val
        self.next = None

def has_cycle(head: ListNode) -> bool: 
    slow = head
    fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False

# Time complexity: O(n)
# Space complexity: O(1)

# ==============================
# Other solution (less efficient) - use hashing:

def has_cycle_1(head: ListNode) -> bool:
    seen = set()
    dummy = head
    while dummy:
        if dummy in seen:
            return True
        seen.add(dummy)
        dummy = dummy.next
    return False

# Time complexity: O(n)
# Space complexity: O(n)