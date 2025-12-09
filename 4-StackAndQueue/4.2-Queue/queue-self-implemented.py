# ===== SINGLY LINKED LIST =====
# ==============================
"""
Use a singly linked list that maintains pointers to the head and tail.
"""

from __future__ import annotations
from typing import Any


class Node:
    def __init__(self, val: Any, next: Node | None = None):
        self.val = val
        self.next = next


class Queue:
    def __init__(self):
        self.head: Node | None = None  # Front of the queue
        self.tail: Node | None = None  # Back of the queue
        self.size: int = 0

    def enqueue(self, val: Any) -> None:
        new_node = Node(val)

        if self.tail:
            self.tail.next = new_node
        self.tail = new_node

        if not self.head:
            self.head = new_node

        self.size += 1

    def dequeue(self) -> Any:
        if self.is_empty():
            raise IndexError("Dequeue from an empty queue")

        val = self.head.val

        self.head = self.head.next

        if not self.head:
            self.tail = None

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
- Enqueue: O(1)
- Dequeue: O(1)
- Peek: O(1)
"""


# ========== 2-STACK ==========
# =============================
"""
Use 2 stacks (2 dynamic arrays, 1 for enqueuing and 1 for dequeuing).
"""


class Queue:
    def __init__(self):
        self.enqueue_stack: list[Any] = []
        self.dequeue_stack: list[Any] = []

    def enqueue(self, val: Any) -> None:
        self.enqueue_stack.append(val)

    def dequeue(self) -> Any:
        if len(self.dequeue_stack) == 0:
            # move elements from enqueue_stack to dequeue_stack
            while len(self.enqueue_stack) > 0:
                self.dequeue_stack.append(self.enqueue_stack.pop())

        if len(self.dequeue_stack) == 0:
            raise IndexError("Dequeue from an empty queue")

        return self.dequeue_stack.pop()

    def peek(self) -> Any:
        if len(self.dequeue_stack) == 0:
            # move elements from enqueue_stack to dequeue_stack
            while len(self.enqueue_stack) > 0:
                self.dequeue_stack.append(self.enqueue_stack.pop())

        if len(self.dequeue_stack) == 0:
            raise IndexError("Peek from an empty queue")

        return self.dequeue_stack[-1]

    def is_empty(self) -> bool:
        return self.__len__() == 0

    def __len__(self) -> int:
        return len(self.enqueue_stack) + len(self.dequeue_stack)


"""
Time complexity:
- Enqueue: amortized O(1) (dynamic array push)
- Dequeue: amortized O(1) (elements are transferred only when dequeue_stack becomes empty)
- Peek: amortized O(1) (same as dequeue)
"""
