"""
Use Python double-ended queue
"""

from collections import deque

queue = deque()

# Initialize with initial values
queue = deque([1, 2, 3])

# Enqueue
queue.append(4)
queue.append(5)

# Dequeue
queue.popleft()  # 1
queue.popleft()  # 2

# Peek (Check element at the front)
queue[0]  # 3

# Get size
len(queue)  # 3
