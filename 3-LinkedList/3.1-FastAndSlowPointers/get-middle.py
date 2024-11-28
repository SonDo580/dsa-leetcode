# Given the head of a linked list with an odd number of nodes,
# return the value of the node in the middle.
# 
# For example, given a linked list that represents 
# 1 -> 2 -> 3 -> 4 -> 5, return 3.


class ListNode:
    def __init__(self, val) -> None:
        self.val = val
        self.next = next

# Use slow and fast pointers
def get_middle(head: ListNode):
    slow = head 
    fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    return slow.val

# Space complexity: O(1) for the pointers
# Time complexity: O(n) for the traversal

# ==============================
# Other ways (less efficient)

# iterate through the linked list once to find the length,
# then iterate from the head again to find the middle       
def get_middle_1(head: ListNode):
    length = 0
    dummy = head

    while dummy:
        length += 1
        dummy = dummy.next

    for _ in range(length // 2):
        head = head.next

    return head.val

# convert the linked list into and array
def get_middle_2(head: ListNode):
    arr = []
    while head:
        arr.append(head.val)
        head = head.next

    return arr[len(arr) // 2]