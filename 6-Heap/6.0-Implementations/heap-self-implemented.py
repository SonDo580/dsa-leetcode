"""
Implement a min heap (max heap is similar).

Properties:
- a node at i has left child at 2i + 1 and right child at 2i + 2.
- a node at i has parent at (i - 1) // 2
- all nodes from n // 2 to n - 1 are leaves.
- in min heap:
  . the min item is at index 0 (root)
  . parent <= its children.
"""


class MinHeap:
    def __init__(self, lst: list[int] = []):
        self._heap: list[int] = lst[:]  # avoid mutating the original list
        self.__heapify()

    def __heapify(self) -> None:
        """Convert the cloned list to a heap in O(n)."""
        # - Move backwards to heapify lower subtrees first,
        #   so when we sift down a higher node,
        #   it interacts with already heapified subtree.
        # - We only need to sift down the internal nodes.
        #   Exclude the leaves.
        for i in range(len(self._heap) // 2 - 1, -1, -1):
            self.__sift_down(i)

    def __sift_up(self, i: int) -> None:
        """
        Move an item up the tree to its correct position.
        Time complexity: 0(log(n)) (~ tree height)
        """
        parent: int = (i - 1) // 2
        while i > 0 and self._heap[parent] > self._heap[i]:
            self._heap[parent], self._heap[i] = (
                self._heap[i],
                self._heap[parent],
            )
            i = parent
            parent = (i - 1) // 2

    def __sift_down(self, i: int) -> None:
        """
        Move an item down the tree to its correct position.
        Time complexity: 0(log(n)) (~ tree height)
        """
        n: int = len(self._heap)
        current: int = i
        left_child: int = 2 * i + 1
        right_child: int = 2 * i + 2

        if left_child < n and self._heap[left_child] < self._heap[current]:
            current = left_child
        if right_child < n and self._heap[right_child] < self._heap[current]:
            current = right_child

        if current != i:
            self._heap[i], self._heap[current] = (
                self._heap[current],
                self._heap[i],
            )
            self.__sift_down(current)

    def heappush(self, item: int) -> None:
        """Add an item to the heap in O(log n)."""
        self._heap.append(item)
        self.__sift_up(len(self._heap) - 1)

        # - Appending new item keeps the tree complete in O(1)
        #   (now new item is the rightmost leaf at the last level)
        # - Sift up to fix the heap property in O(log n).

    def heappop(self) -> int:
        """Remove and return the min item in O(log n)."""
        min_item: int = self.peek()
        last_item: int = self._heap.pop()  # this is min_item if length is 1

        if len(self._heap) > 0:
            self._heap[0] = last_item
            self.__sift_down(0)

            # - Placing the last item at the root keeps the tree complete in O(1).
            #   (last item is the rightmost leaf at the last level)
            # - Sift down to fix the heap property in O(log n).

        return min_item

    def peek(self) -> int:
        """Return the min item in O(1)."""
        if not self._heap:
            raise IndexError("Heap is empty")
        return self._heap[0]

    def __len__(self) -> int:
        """Return the number of items in the heap."""
        return len(self._heap)

    def __str__(self) -> str:
        """String representation of the heap."""
        return str(self._heap)


# ===== Example usage =====
def main():
    heap = MinHeap()

    # Add to heap
    heap.heappush(1)
    heap.heappush(4)
    heap.heappush(3)
    print(f"length: {len(heap)}")  # 3

    # Find min item in O(1)
    print(f"min: {heap.peek()}")  # 1

    # Pop min item in O(log n)
    print(f"popped: {heap.heappop()}")  # 1

    # The min heap property is kept
    print(f"heap: {heap}")  # [3, 4]

    # Convert a list to a heap in O(n)
    heap2 = MinHeap([67, 341, 234, -67, 12, -976])

    heap2.heappush(7451)
    heap2.heappush(-5352)

    print(f"heap2: {heap2}")  # [-5352, -976, 67, -67, 12, 234, 7451, 341]

    # The numbers will be in sorted order
    while len(heap2) > 0:
        print(heap2.heappop(), end=" ")  # -5352, -976, -67, 12, 67, 234, 341, 7451
    print()


if __name__ == "__main__":
    main()


"""
Time complexity of 'heapify' in detailed:

- At height = 0 (leaves):
  . max cost of heapify: 0 
  . max number of nodes: max n / 2
- At height = 1:
  . max cost of heapify: 1
  . max number of nodes: n / 4
- ...
- At height = log2(n) (root):
  . max cost of heapify: log2(n)
  . max number of nodes: 1

=> Total build cost: T = (n/2)*0 + (n/4)*1 + (n/8)*2 + ... + 1*log2(n)
T <= n * ((1/4 + 2/8) + 3/16 + 4/32 + 5/64 + 6/128 + ...)
   = n * (1/2 + 3/16 + 1/8 + 5/64 + 1/32 + ...)
  <= n * (1/2 + 1/4 + 1/8 + 1/16 + ...)
   = n * 1      (geometric series sum)
   = n

=> Time complexity: O(n)
"""
