class ListNode:
    def __init__(self, val) -> None:
        self.val = val
        self.next = None

def reverse_list(head: ListNode) -> ListNode:
    prev = None
    current = head
    
    while current:
        next_node = current.next # save the next node
        current.next = prev # reverse the direction of the pointer
        prev = current # set the current node as prev to the next node
        current = next_node # move on
    
    return prev

# Time complexity: O(n)
# Space complexity: O(1)
