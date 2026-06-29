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


class Deque:
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
            raise IndexError("Pop an empty deque")

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
            raise IndexError("Pop an empty deque")

        val = self.head.val

        self.head = self.head.next
        if not self.head:
            self.tail = None
        else:
            self.head.prev = None

        self.size -= 1
        return val

    def peek_left(self) -> Any:
        if self.is_empty():
            raise IndexError("Peek an empty deque")
        return self.head.val

    def peek_right(self) -> Any:
        if self.is_empty():
            raise IndexError("Peek an empty deque")
        return self.tail.val

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


# ===== BLOCK LINKED LIST =====
# ==============================
"""
Use a doubly linked list of fixed-size arrays.
"""
BLOCK_SIZE = 64


class Block:
    def __init__(self):
        self.data: list[Any | None] = [None] * BLOCK_SIZE
        self.left: Block | None = None
        self.right: Block | None = None


class Deque:
    def __init__(self):
        # Init a single block
        new_block = Block()
        self.leftmost_block: Block = new_block
        self.rightmost_block: Block = new_block

        # Start from the middle of the block
        self.leftmost_index: int = BLOCK_SIZE // 2
        self.rightmost_index: int = BLOCK_SIZE // 2 - 1

        self.size: int = 0

    def append_right(self, val: Any) -> None:
        if self.rightmost_index < BLOCK_SIZE - 1:
            # Add to current right block
            self.rightmost_index += 1
        else:
            # Add a new block to the right
            new_block = Block()
            new_block.left = self.rightmost_block
            self.rightmost_block.right = new_block
            self.rightmost_block = new_block
            self.rightmost_index = 0

        self.rightmost_block.data[self.rightmost_index] = val
        self.size += 1

    def append_left(self, val: Any) -> None:
        if self.leftmost_index > 0:
            # Add to current left block
            self.leftmost_index -= 1
        else:
            # Add a new block to the left
            new_block = Block()
            new_block.right = self.leftmost_block
            self.leftmost_block.left = new_block
            self.leftmost_block = new_block
            self.leftmost_index = BLOCK_SIZE - 1

        self.leftmost_block.data[self.leftmost_index] = val
        self.size += 1

    def pop_right(self) -> Any:
        if self.size == 0:
            raise IndexError("Pop an empty deque")

        val = self.rightmost_block.data[self.rightmost_index]
        self.rightmost_block.data[self.rightmost_index] = None
        self.rightmost_index -= 1

        # Move to previous block if index under-flows
        if self.rightmost_index < 0 and self.rightmost_block.left:
            self.rightmost_block = self.rightmost_block.left
            self.rightmost_index = BLOCK_SIZE - 1

        # Note: current implementation doesn't remove free blocks

        self.size -= 1
        return val

    def pop_left(self) -> Any:
        if self.size == 0:
            raise IndexError("Pop an empty deque")

        val = self.leftmost_block.data[self.leftmost_index]
        self.leftmost_block.data[self.leftmost_index] = None
        self.leftmost_index += 1

        # Move to next block if index over-flows
        if self.leftmost_index >= BLOCK_SIZE and self.leftmost_block.right:
            self.leftmost_block = self.leftmost_block.right
            self.leftmost_index = 0

        # Note: current implementation doesn't remove free blocks

        self.size -= 1
        return val

    def peek_right(self) -> Any:
        if self.size == 0:
            raise IndexError("Peek an empty deque")
        return self.rightmost_block.data[self.rightmost_index]

    def peek_left(self) -> Any:
        if self.size == 0:
            raise IndexError("Peek an empty deque")
        return self.leftmost_block.data[self.leftmost_index]

    def is_empty(self) -> bool:
        return self.size == 0

    def __len__(self) -> int:
        return self.size
