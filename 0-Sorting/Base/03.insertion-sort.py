"""
Key idea:
- Take the next unsorted element and insert it into the correct position
  in the sorted portion by shifting elements to the right.
- The sorted portion (from the front) grows by 1 element after each pass.
"""


def insertion_sort(arr: list[int]) -> None:
    n = len(arr)

    for i in range(1, n):
        current = arr[i]  # current element to insert
        j = i - 1  # end of sorted portion

        # Shift element of the sorted portion to the right
        # until we find the correct position for current
        while j >= 0 and arr[j] > current:
            arr[j + 1] = arr[j]
            j -= 1

        # Insert current at the correct position in the sorted portion
        arr[j + 1] = current


"""
Complexity:

1. Time complexity:
- Best case: O(n)
  + Happens when the array is already sorted.
  + Perform n - 1 comparisons and no shifting.

- Worst case: O(n^2) - when the array is reverse sorted
  + Pass 1: 1 comparison & shift
  + Pass 2: 2 comparisons & shifts
  + ...
  + Pass n - 1: n - 1 comparisons & shifts
  -> Total: n * (n - 1)
  -> O(n^2)

2. Space complexity: O(1)
"""

"""
Stability: stable
- Equal elements remain in the same relative order.
- Because we only shift elements that are greater than 'current'.
"""
