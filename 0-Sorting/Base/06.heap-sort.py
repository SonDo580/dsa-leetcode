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


# not used
def _sift_down_recur(arr: list[int], n: int, i: int):
    """
    Fix the max heap represented by arr[0..n]:
    Move node i down the tree to its correct position.
    """
    current: int = i
    left_child: int = 2 * i + 1
    right_child: int = 2 * i + 2

    if left_child < n and arr[left_child] > arr[current]:
        current = left_child
    if right_child < n and arr[right_child] > arr[current]:
        current = right_child

    if current != i:
        arr[i], arr[current] = arr[current], arr[i]
        _sift_down_recur(current)


# used
def sift_down(arr: list[int], n: int, i: int):
    """
    Fix the max heap represented by arr[0..n]:
    Move node i down the tree to its correct position.
    """
    while True:
        current: int = i
        left_child: int = 2 * i + 1
        right_child: int = 2 * i + 2

        if left_child < n and arr[left_child] > arr[current]:
            current = left_child
        if right_child < n and arr[right_child] > arr[current]:
            current = right_child

        if current == i:
            return

        arr[i], arr[current] = arr[current], arr[i]
        i = current


def heapify(arr: list[int], n: int):
    """Convert arr[0..n] a max heap."""
    # - Move backwards to heapify lower subtrees first,
    #   so when we sift down a higher node,
    #   it interacts with already-heapified subtree.
    # - We only need to sift down internal nodes (exclude leaves).
    for i in range(n // 2 - 1, -1, -1):
        sift_down(arr, n, i)


def heap_sort(arr: list[int]) -> None:
    # Build a max heap
    n = len(arr)
    heapify(arr, n)

    # Extract element from the heap one by one
    for i in range(n - 1, 0, -1):
        # Move current root (max element) to the end of the unsorted portion
        arr[0], arr[i] = arr[i], arr[0]

        # Fix the reduced heap (exclude the max element just sorted)
        sift_down(arr, n=i, i=0)


# quick test
if __name__ == "__main__":
    arr = [67, 341, 234, -67, 12, -976, 7451, -5352]
    heap_sort(arr)
    assert arr == [-5352, -976, -67, 12, 67, 234, 341, 7451]


"""
Complexity:
- Let n = len(arr)

1. Time complexity:
- Build initial heap: O(n)
- Perform n - 1 extraction. Each extraction does: 
  . swap: O(1)
  . fix the reduced heap: O(log(n))
=> Overall: O(n * log(n))

2. Space complexity:
- iterative 'sift_down': O(1) (used)
- recursive 'sift_down': O(log(n))
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
