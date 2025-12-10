"""
https://leetcode.com/problems/merge-k-sorted-lists/

You are given an array of k linked-lists lists,
each linked-list is sorted in ascending order.

Merge all the linked-lists into one sorted linked-list and return it.
"""

"""
Idea:
- Recursively split the array of linked lists in half.
  Merge each portion separately and merge 2 sorted linked lists back.
- Base case:
  . empty array -> return null
  . 1-element array -> return the single element
- Merge 2 sorted linked-lists:
  . If 1 item is null -> return the other
  . Otherwise, create a result linked-list.
    Use 2 pointers on 2 input linked-lists.
    Select the smaller value for the next node of result linked-list.
- We can modify the 'next' pointers of list nodes directly.
"""

from __future__ import annotations


class ListNode:
    def __init__(self, val: int = 0, next: ListNode | None = None):
        self.val = val
        self.next = next


def merge_k_lists(lists: list[ListNode | None]) -> ListNode | None:
    return merge(lists, start=0, end=len(lists) - 1)


def merge(lists: list[ListNode | None], start: int, end: int) -> ListNode | None:
    # empty array
    if start > end:
        return None

    # 1-linked-list array
    if start == end:
        return lists[start]

    # Recursively merge the left and right portions
    mid = (start + end) // 2
    left_ll = merge(lists, start=start, end=mid)
    right_ll = merge(lists, start=mid + 1, end=end)

    # If one is null, return the other
    if not left_ll:
        return right_ll
    if not right_ll:
        return left_ll

    # Merge 2 sorted linked-lists
    curr_left: ListNode | None = left_ll
    curr_right: ListNode | None = right_ll

    merged_ll: ListNode | None = None
    curr_merged: ListNode | None = None

    while curr_left and curr_right:
        if curr_left.val <= curr_right.val:
            next_merged = curr_left
            curr_left = curr_left.next
        else:
            next_merged = curr_right
            curr_right = curr_right.next

        if not curr_merged:
            # Record the head
            merged_ll = next_merged
            curr_merged = next_merged
        else:
            curr_merged.next = next_merged
            curr_merged = curr_merged.next

    # Handle remaining nodes from left or right linked-list
    while curr_left:
        curr_merged.next = curr_left
        curr_left = curr_left.next
        curr_merged = curr_merged.next
    while curr_right:
        curr_merged.next = curr_right
        curr_right = curr_right.next
        curr_merged = curr_merged.next

    return merged_ll


"""
Complexity:

1. Time complexity: O(n * log(n))
- Recursion depth: O(log(n))
- Merging at each level: O(n)

2. Space Complexity: O(log(n)) for recursion stack
"""
