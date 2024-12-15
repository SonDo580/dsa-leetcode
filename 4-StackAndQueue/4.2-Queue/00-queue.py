# To implement an efficient queue:
# - Use a doubly linked list that maintains pointers to the head and tail (with sentinel nodes)
# - Use a double-ended queue (allow adding and deleting elements from both ends)

from collections import deque

queue = deque()

# Initialize with initial values
queue = deque([1,2,3])

# Enqueue
queue.append(4)
queue.append(5)

# Dequeue
queue.popleft() # 1
queue.popleft() # 2

# Check element at the front
queue[0] # 3

# Get size
len(queue) # 3



# ===== Other Implementation =====
# Use a singly linked list that maintains pointers to the head and tail

class Node:
    def __init__(self, val):
        self.val = val
        self.next = None

class Queue:
    def __init__(self):
        self.head = None # Front of the queue
        self.tail = None # Back of the queue
        self.size = 0
    
    def enqueue(self,val):
        new_node = Node(val)

        if self.tail:
            self.tail.next = new_node
        self.tail = new_node

        if not self.head:
            self.head = new_node
        
        self.size += 1
    
    def dequeue(self):
        if self.is_empty():
            raise IndexError("Dequeue from an empty queue")

        val = self.head.val
        
        self.head = self.head.next
        
        if not self.head:
            self.tail = None

        self.size -= 1

        return val

    def peek(self):
        if self.is_empty():
            raise IndexError("Peek from an empty queue")
        return self.head.val

    def is_empty(self):
        return self.size == 0

    def __len__(self):
        return self.size