"""
Key idea:
- Find the maximum (or minimum) element and
  swap it with the last (or first) element (like selection sort).
- Use a binary heap for efficient access to the max (or min) element
  (O(log(n)) instead of O(n)).
- Repeat the process for remaining unsorted portion.
"""

"""
Algorithm:
- Convert the array into a max heap using heapify.
- Swap the heap root (max element) with the last element of unsorted portion.
  Decrease the heap size by 1 (ignore the last element as it's now sorted).
- Heapify the reduced heap to restore heap property.
- Repeat this process until the heap size becomes 1.
"""

"""
Heap properties:
- Treat the array as a complete binary tree:
  . the root is at index 0.
  . element at i has left child at 2i + 1, right child at 2i + 2.
  . all nodes from n // 2 to n - 1 are leaves.
- For max heap: parent >= its children.

[!] See Heap section for more in-depth info about heap
"""


def heapify(arr: list[int], n: int, i: int) -> None:
    """
    Ensure the subtree rooted at index i is a max heap.
    Only heapify elements in the unsorted portion [0, n).
    """
    largest = i  # Initialize largest as root
    left_child = 2 * i + 1
    right_child = 2 * i + 2

    # Left child is larger than root
    if left_child < n and arr[left_child] > arr[largest]:
        largest = left_child

    # Right child is larger than root
    if right_child < n and arr[right_child] > arr[largest]:
        largest = right_child

    # If largest is not root
    if largest != i:
        # Swap the larger child to root
        arr[i], arr[largest] = arr[largest], arr[i]

        # Recursively heapify the affected subtree
        heapify(arr, n, largest)


def heapify_iter(arr: list[int], n: int, i: int) -> None:
    """Iterative heapify."""
    while True:
        largest = i
        left_child = 2 * i + 1
        right_child = 2 * i + 2

        if left_child < n and arr[left_child] > arr[largest]:
            largest = left_child
        if right_child < n and arr[right_child] > arr[largest]:
            largest = right_child

        if largest == i:
            break  # heap property restored

        arr[i], arr[largest] = arr[largest], arr[i]
        i = largest  # continue with affected subtree


def heap_sort(arr: list[int]) -> None:
    n = len(arr)

    # Build a max heap
    # (start from the last non-leaf node up to the root)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    # Extract element from the heap one by one
    for i in range(n - 1, 0, -1):
        # Move current root (max element) to the end of the unsorted portion
        arr[0], arr[i] = arr[i], arr[0]

        # Heapify the reduced heap (exclude the max element just sorted)
        heapify(arr, i, 0)


"""
Complexity:
- Let n = len(arr)

1. Time complexity:
- Build initial heap: O(n)
- Perform n - 1 extraction. Each extraction does: 
  . swap: O(1)
  . heapify the reduced heap: O(log(n))
=> Overall: O(n * log(n))

2. Space complexity: 
- recursive approach: O(log(n)) for recursion stack of 'heapify'
- iterative approach: O(1)
"""

"""
Stability: unstable
- Equal elements may change their relative order because of swapping.
"""

"""
Features:
- guaranteed time complexity of O(n * log(n)) in all cases
  -> suitable for large datasets.
- minimal extra memory (no extra space if using iterative heapify)
- not very efficient because:
  . high constants in time complexity: more comparisons and swaps at each level.
  . random memory jumps causes frequent CPU cache misses.
"""
