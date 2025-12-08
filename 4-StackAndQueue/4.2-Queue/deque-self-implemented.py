# ===== DOUBLY LINKED LIST =====
# ==============================
"""
Use a doubly linked list that maintains pointers to the head and tail.
"""

from __future__ import annotations
from typing import Any


class Node:
    def __init__(self, val: Any, prev: Node | None = None, next: Node | None = None):
        self.val = val
        self.next = next
        self.prev = prev


class Queue:
    def __init__(self):
        self.head: Node | None = None  # Front of the queue
        self.tail: Node | None = None  # Back of the queue
        self.size: int = 0

    def append_right(self, val: Any) -> None:
        new_node = Node(val)

        if self.tail:
            self.tail.next = new_node
            new_node.prev = self.tail
        self.tail = new_node

        if not self.head:
            self.head = new_node

        self.size += 1

    def pop_right(self) -> Any:
        if self.is_empty():
            raise IndexError("Dequeue from an empty queue")

        val = self.tail.val

        self.tail = self.tail.prev
        if not self.tail:
            self.head = None
        else:
            self.tail.next = None

        self.size -= 1
        return val

    def append_left(self, val: Any) -> None:
        new_node = Node(val)

        if self.head:
            new_node.next = self.head
            self.head.prev = new_node
        self.head = new_node

        if not self.tail:
            self.tail = new_node

        self.size += 1

    def pop_left(self) -> Any:
        if self.is_empty():
            raise IndexError("Dequeue from an empty queue")

        val = self.head.val

        self.head = self.head.next
        if not self.head:
            self.tail = None
        else:
            self.head.prev = None

        self.size -= 1
        return val

    def peek(self) -> Any:
        if self.is_empty():
            raise IndexError("Peek from an empty queue")
        return self.head.val

    def is_empty(self) -> bool:
        return self.size == 0

    def __len__(self) -> int:
        return self.size


"""
Time complexity:
- append_left: O(1)
- append_right: O(1)
- pop_left: O(1)
- pop_right: O(1)
- peek: O(1)
"""
