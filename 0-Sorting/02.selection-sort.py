# ===== Key idea =====
# - Repeatedly select the smallest element from the unsorted portion,
#   and swap it with the first unsorted element.
# - After each pass, the sorted portion grows by 1 element (from the front).


def selection_sort(arr: list[int]) -> list[int]:
    n = len(arr)

    for i in range(n - 1):
        # Note: The first i elements are already in place

        # Initialize the first unsorted element as the minimum
        index_of_min = i

        # Find the minimum element in the unsorted portion
        for j in range(i + 1, n):
            if arr[j] < arr[index_of_min]:
                index_of_min = j

        # Swap the minimum element with the first unsorted element
        arr[i], arr[index_of_min] = arr[index_of_min], arr[i]

    return arr


# ===== Complexity =====
# 1. Time complexity: O(n^2)
# - Scan through the unsorted portion in each pass
#   + Pass 1: n - 1 comparisons
#   + Pass 2: n - 2 comparisons
#   + ...
#   + Pass n - 1: 1 comparison
#   -> Total: n * (n - 1) / 2
#   -> O(n^2)
#
# 2. Space complexity: O(1)

# ===== Stability =====
# - Unstable:
#   + Equal elements may be reordered.
#   + Example: [4, 4, 3]
#     -> the first 4 is swapped with 3, moving it behind the second 4.
