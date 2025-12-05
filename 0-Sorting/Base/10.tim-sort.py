"""
Key idea:
- Identify sorted runs (small segments). Reverse the order if needed.
- Sort unsorted runs using Insertion Sort (fast for small or nearly sorted data).
- Merge the runs efficiently, similar to Merge Sort.

[!] This is the default sorting algorithm in Python
"""

"""
Minimum RUN size:
. too small -> too many merges -> slow.
. too larger -> insertions sort becomes slow.
-> range [32, 64] gives best practical performance.

- The min run size is selected such that the number of runs is equal to, 
  or slightly less than, a power of two. 
  -> keep merging balanced and efficient.

- If array length < 64, set min run size to array size (reduce to insertion sort).
"""


def calc_min_run(n: int) -> int:
    """
    Find minimum run size such that number of runs N / min_run
    is equal to or slightly less than a power of 2.
    """
    # Keep halving n until it becomes smaller than 32.
    # Detect any odd intermediate result by checking if the LSB is 1.
    r = 0
    while n >= 32:
        r |= n & 1
        n >>= 1

    # At this point:
    # . min_run = current n = floor(N / 2^k)
    # . r = 1 if N / 2^k if has a fractional part.
    #   r = 0 if N / 2^k was an exact integer.

    # Round up min_run to ceil(N / 2^k) so that N / min_run <= 2^k
    # -> min_run = min_run + 1 if r = 1 OR min_run + 0 if r = 0
    #            = min_run + r
    return n + r


def insertion_sort(arr: list[int], left: int, right: int) -> None:
    """Insertion sort for small ranges."""
    for i in range(left + 1, right + 1):
        current = arr[i]  # current element to insert
        j = i - 1  # end of sorted portion

        # Shift element of the sorted portion to the right
        # until we find the correct position for current
        while j >= left and arr[j] > current:
            arr[j + 1] = arr[j]
            j -= 1

        # Insert current at the correct position in the sorted portion
        arr[j + 1] = current


def merge(arr: list[int], left: int, mid: int, right: int) -> None:
    """Merge 2 sorted subarrays [left..mid] and[mid+1..right]."""
    # Copy data to temp arrays
    n1 = mid - left + 1
    n2 = right - mid
    left_arr = [arr[left + i] for i in range(n1)]
    right_arr = [arr[mid + 1 + j] for j in range(n2)]

    # Merge the temp arrays back into arr[left..right]
    # (If there's a tie, pick the element from left_arr to ensure stability)
    i = j = 0
    k = left
    while i < n1 and j < n2:
        if left_arr[i] <= right_arr[j]:
            arr[k] = left_arr[i]
            i += 1
        else:
            arr[k] = right_arr[j]
            j += 1
        k += 1

    # Copy remaining items from left_arr/right_arr
    while i < n1:
        arr[k] = left_arr[i]
        i += 1
        k += 1
    while j < n2:
        arr[k] = right_arr[j]
        j += 1
        k += 1


def find_run(arr: list[int], start: int) -> int:
    """
    Detect ascending/descending run starting from 'start'.
    Reverse descending run. Return the end index (exclusive).
    """
    n = len(arr)
    end = start + 1
    if end == n:
        return end

    if arr[end] < arr[start]:
        # Descending run
        while end < n and arr[end] < arr[end - 1]:
            end += 1
        arr[start:end] = reversed(arr[start:end])
    else:
        # Ascending run
        while end < n and arr[end] >= arr[end - 1]:
            end += 1

    return end


def tim_sort(arr: list[int]) -> None:
    n = len(arr)
    min_run = calc_min_run(n)

    # Each run (start, end) represents a sorted subarray
    runs: list[tuple[int, int]] = []

    i = 0
    while i < n:
        # Detect a natural increasing or decreasing run
        # (The decreasing run is reversed)
        run_end = find_run(arr, i)
        run_len = run_end - i

        # If the detected run is short than min_run,
        # extend it to min_run then apply insertion sort.
        if run_len < min_run:
            run_end = min(i + min_run, n)
            insertion_sort(arr, i, run_end - 1)

        # Record current sorted run
        runs.append((i, run_end))

        # Mark the start of the next run
        i = run_end

        # Keep merging if the second latest run is shorter than the latest run
        # to avoid too many unbalanced merges later.
        while len(runs) > 1:
            start_1, end_1 = runs[-2]
            start_2, end_2 = runs[-1]
            len_1, len_2 = end_1 - start_1, end_2 - start_2

            if len_1 <= len_2:
                merge(arr, left=start_1, mid=end_1 - 1, right=end_2 - 1)
                runs.pop()
                runs[-1] = (start_1, end_2)
            else:
                break

    # Keep merging after all runs are collected
    while len(runs) > 1:
        start_1, end_1 = runs[-2]
        start_2, end_2 = runs[-1]

        merge(arr, left=start_1, mid=end_1 - 1, right=end_2 - 1)
        runs.pop()
        runs[-1] = (start_1, end_2)


"""
Complexity:
- Let n = len(arr)
      k = average run size (small constant)

1. Time complexity:
- Detecting runs: O(n)
- Sort runs:
  . Sort each run using insertion sort: O(k^2).
  . There are about n / k runs.
  -> Total sorting cost: O(n * k) ~ O(n)
- Merge runs:
  . Each merge level costs O(n)
  . Number of merge levels: O(log2(n / k))
  -> Total merging cost: O(n * log(n / k)) ~ O(n * log(n))
=> Overall:
   - Worst/Average case: O(n * log(n))
   - Best case: O(n) when the array is already sorted / reverse-sorted.

2. Space complexity: O(n) for merging runs.
"""
