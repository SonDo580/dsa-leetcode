# Note: children of node i have indices 2i + 1 and 2i + 2


class MinHeap:
    def __init__(self, lst: list[int] = []):
        self._heap: list[int] = lst[:]  # avoid mutating the original list
        self.__heapify()

    def __heapify(self) -> None:
        """Convert the cloned list to a heap in O(n)"""
        for i in range(len(self._heap) // 2 - 1, -1, -1):
            self.__move_down(i)
    
        # Explain:
        # - Why moving backwards:
        #   + to heapify lower level subtrees first
        #   + so when we move down a higher level node, it interacts with already heapified subtree
        # - Why start from n // 2 - 1:
        #   + in binary heap, nodes at indices n // 2 and beyond are all leaf nodes.
        #   + we only need to move down the internal nodes

    def __move_up(self, index: int) -> None:
        """Move a newly added item up the tree to its correct position"""
        parent: int = (index - 1) // 2
        while index > 0 and self._heap[parent] > self._heap[index]:
            self._heap[parent], self._heap[index] = (
                self._heap[index],
                self._heap[parent],
            )
            index = parent
            parent = (index - 1) // 2

    def __move_down(self, index: int) -> None:
        """Move an item down the tree to its correct position"""
        n: int = len(self._heap)
        current: int = index
        left: int = 2 * index + 1  # left child index
        right: int = 2 * index + 2  # right child index

        if left < n and self._heap[left] < self._heap[current]:
            current = left
        if right < n and self._heap[right] < self._heap[current]:
            current = right

        if current != index:
            self._heap[index], self._heap[current] = (
                self._heap[current],
                self._heap[index],
            )
            self.__move_down(current)

    def heappush(self, item: int) -> None:
        """Add an item to the heap in O(log n)"""
        self._heap.append(item)
        self.__move_up(len(self._heap) - 1)

        # Explain:
        # - Appending new item keeps the tree complete in O(1)
        #   (now new item is the rightmost leaf at the last level)
        # - Moving up fixes the heap property in O(log n)
        #   (find correct position for the new item)

    def heappop(self) -> int:
        """Remove and return the min item in O(log n)"""
        min_item: int = self.peek()
        last_item: int = self._heap.pop()  # this is min_item if length is 1

        if len(self._heap) > 0:
            self._heap[0] = last_item
            self.__move_down(0)

            # Explain:
            # - Placing the last item at the root keeps the tree complete in O(1).
            #   (last item is the rightmost leaf at the last level)
            # - Moving down fixes the heap property in O(log n).
            #   (swap temporary root with the smallest item & find correct position for the temporary root)

        return min_item

    def peek(self) -> int:
        """Return the min item in O(1)"""
        if not self._heap:
            raise IndexError("Heap is empty")
        return self._heap[0]

    def __len__(self) -> int:
        """Return the number of items in the heap"""
        return len(self._heap)

    def __str__(self) -> str:
        """String representation of the heap"""
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
    print(f"heap: {heap}") # [3, 4]

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
