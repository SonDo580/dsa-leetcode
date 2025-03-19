from heapq import *

# heapq module:
# - does not provide a heap data structure.
# - provides methods on a normal list to perform heap operations.
# - implement a min heap

heap = []

# Add to heap
heappush(heap, 1)
heappush(heap, 2)
heappush(heap, 3)
print(len(heap)) # 3

# Find min item in O(1)
print(heap[0]) # 1

# Pop min item in O(log n)
heappop(heap)
print(len(heap)) # 2

# Convert a list to a heap in O(n)
heap = [67, 341, 234, -67, 12, -976]
heapify(heap)

heappush(heap, 7451)
heappush(heap, -5352)

# The numbers will be in sorted order
print(heap) # [-5352, -976, 67, -67, 12, 234, 7451, 341]
while heap:
    print(heappop(heap))