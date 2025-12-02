"""
Key idea:
(divide and conquer)
- Pick a pivot element: first / last / median / random
- Partition the array:
  . x < pivot -> go left
  . x > pivot -> go right
- pivot is now at the correct position.
- Recursively sort the left and right sub-arrays.
"""

"""
Partitioning algorithms summary:

1. Naive partition:
- Create a temporary array.
- Copy x <= pivot, then pivot, then x > pivot.
- Copy back to original array.
-> Stable, O(n) extra space.

2. Lomuto partition:
- Maintain a pointer i for the end of (x <= pivot) region
- Scan left to right, swap x <= pivot into that region
- Place pivot after the (x <= pivot) region
-> Unstable, in-place.

3. Hoare partition:
- Use 2 pointers moving towards each other.
- Swap out-out-place elements (left >= pivot, right <= pivot).
- Stop when pointers cross.
-> Unstable, in-place.
"""


# ===== NAIVE PARTITION =====
# ===========================
def quick_sort(arr: list[int], low: int, high: int) -> None:
    if low < high:
        pivot_index = naive_partition(arr, low, high)
        quick_sort(arr, low, pivot_index - 1)
        quick_sort(arr, pivot_index + 1, high)


def naive_partition(arr: list[int], low: int, high: int) -> int:
    pivot = arr[high]  # pick last element as pivot
    temp = []  # create temp array

    # Copy x <= pivot (except pivot) to temp
    for i in range(low, high):
        if arr[i] <= pivot:
            temp.append(arr[i])

    # Add pivot to temp & save pivot index
    temp.append(pivot)
    pivot_index = low + (len(temp) - 1)  # index in arr

    # Copy x > pivot to temp
    for i in range(low, high):
        if arr[i] > pivot:
            temp.append(arr[i])

    # Copy elements from temp back to arr
    for i in range(len(temp)):
        arr[low + i] = temp[i]

    return pivot_index


"""
Complexity:

1. Time complexity:
- Recursion depth: 
  . Best/Average case: O(log(n)) (split evenly)
  . Worst case: O(n) (pivot is always min or max)
- Partitions at each level: O(n)
=> Overall: 
   . Best/Average case: O(n * log(n))
   . Worst case: O(n^2)

2. Space complexity:
- temp array: O(n)
- recursion stack: O(n) or O(log(n))
=> Overall: O(n)
"""

"""
Stability: stable
- Preserve order of duplicate elements.
"""


# ===== LOMUTO PARTITION =====
# ============================
def quick_sort(arr: list[int], low: int, high: int) -> None:
    if low < high:
        pivot_index = lomuto_partition(arr, low, high)
        quick_sort(arr, low, pivot_index - 1)
        quick_sort(arr, pivot_index + 1, high)


def lomuto_partition(arr: list[int], low: int, high: int) -> int:
    pivot = arr[high]  # pick last element as pivot

    # Mark the end of (x <= pivot, except pivot) region
    i = low - 1

    # Move x <= pivot to the left side
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    # Place pivot after (x <= pivot) region
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


"""
Complexity:

1. Time complexity:
- Recursion depth: 
  . Best/Average case: O(log(n)) (split evenly)
  . Worst case: O(n) (pivot is always min or max)
- Partitions at each level: O(n)
=> Overall: 
   . Best/Average case: O(n * log(n))
   . Worst case: O(n^2)

2. Space complexity:
- recursion stack: O(n) or O(log(n))
=> Overall:
   . Best/Average case: O(log(n))
   . Worst case: O(n)
"""

"""
Stability: unstable
- equal elements may cross each other due to swapping.
"""


# ===== HOARE PARTITION =====
# ============================


def quick_sort(arr: list[int], low: int, high: int) -> None:
    if low < high:
        p = hoare_partition(arr, low, high)
        quick_sort(arr, low, p)  # include p (check [!] in hoare_partition)
        quick_sort(arr, p + 1, high)


def hoare_partition(arr: list[int], low: int, high: int) -> int:
    # Pick middle element as pivot
    pivot = arr[(low + high) // 2]

    i = low - 1
    j = high + 1

    while True:
        # Find the next arr[i] >= pivot from the left
        i += 1
        while arr[i] < pivot:
            i += 1

        # Find the next arr[j] <= pivot from the right
        j -= 1
        while arr[j] > pivot:
            j -= 1

        # If pointers cross, partition is done
        if i >= j:
            return j

        # [!] At the end:
        # - All values in [low..j] are <= pivot.
        #   All values in [j+1..high] are >= pivot.
        #   But arr[j] itself may not be pivot.
        # - j is just partition boundary, not correct position of pivot
        #   (unlike naive_partition and lomuto_partition).
        #   -> include it in the recursive calls.

        # Swap out-of-place elements
        arr[i], arr[j] = arr[j], arr[i]


"""
Complexity:

1. Time complexity:
- Recursion depth: 
  . Best/Average case: O(log(n)) (split evenly)
  . Worst case: O(n) (pivot is always min or max)
- Partitions at each level: O(n)
=> Overall: 
   . Best/Average case: O(n * log(n))
   . Worst case: O(n^2)

2. Space complexity:
- recursion stack: O(n) or O(log(n))
=> Overall:
   . Best/Average case: O(log(n))
   . Worst case: O(n)
"""

"""
Stability: unstable
- equal elements may cross each other due to swapping.
"""


x = [5, 4, 5, 3, 5]
quick_sort(x, 0, len(x) - 1)
print(x)

y = [5, 6, 5, 3, 5]
quick_sort(y, 0, len(y) - 1)
print(y)
