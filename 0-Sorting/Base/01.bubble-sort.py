"""
Key idea:
- Repeatedly swap adjacent elements if they're in the wrong order.
- After each pass, the largest element "bubbles up" to the end.
"""


def bubble_sort(arr: list[int]) -> None:
    n = len(arr)
    for i in range(len(arr)):
        swapped = False

        # The last i elements are already in correct positions
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True

        # Optimization: no swaps in this pass -> array is sorted
        if not swapped:
            break


"""
Complexity:

1. Time complexity:
- Best case: O(n)
  + If the array is already sorted, no swaps occur in the first pass
    -> only loop through the array once
    -> O(n)

- Average/Worst case: O(n^2)
  + Pass 1: n - 1 comparisons
  + Pass 2: n - 2 comparisons
  + ...
  + Pass n - 1: 1 comparison
  -> Total: 1 + 2 + ... + (n - 2) + (n - 1) = n * (n - 1) / 2
  -> O(n^2)

2. Space complexity: O(1)
"""

"""
Stability: stable
- doesn't reorder equal elements
"""
