"""
https://www.geeksforgeeks.org/problems/inversion-of-array-1587115620/1

Given an array of integers arr[]. You have to find the Inversion Count of the array.
Note: Inversion count is the number of pairs of elements (i, j) such that i < j and arr[i] > arr[j].

Input: arr[] = [2, 4, 1, 3, 5]
Output: 3
Explanation: The sequence 2, 4, 1, 3, 5 has three inversions (2, 1), (4, 1), (4, 3).

Input: arr[] = [2, 3, 4, 5, 6]
Output: 0
Explanation: As the sequence is already sorted so there is no inversion count.

Input: arr[] = [10, 10, 10]
Output: 0
Explanation: As all the elements of array are same, so there is no inversion count.

Constraints:
1 <= arr.size() <= 10^5
1 <= arr[i] <= 10^4
"""


# ========== BRUTE-FORCE ==========
# =================================
def count_inversions(arr: list[int]) -> int:
    n = len(arr)
    count = 0
    for i in range(n - 1):
        for j in range(i + 1, n):
            if arr[i] > arr[j]:
                count += 1
    return count


"""
Complexity:
1. Time complexity: O(n^2)
2. Space complexity: O(1)
"""

# ========== DIVIDE & CONQUER ==========
# ======================================
"""
Idea:
- Recursively divide the arr in half.
  Count number of inversions in 'left'.
  Count number of inversions in 'right'.  
  Count number of inversions (left[i], right[j]).
  Combine to get the total number of inversions. 
- Base case: subarray has only 1 element -> no inversions.

- When merging, if the 2 subarrays have random order,
  counting inversions will be inefficient.
  -> Sort the subarrays before merging
  -> Use merge sort.

- With both subarrays in ascending order, if left[i] > right[j],
  all items in left[i..n1] are also > right[j]
  -> count (n1 - i) inversions in O(1).

- Optional: Avoid mutating 'arr' if needed
  + shallow copy: arr[:]
  + deep copy: copy.deepcopy(arr)
"""


def count_inversions(arr: list[int]) -> int:
    return merge_sort_and_count_inversions(arr, left=0, right=len(arr) - 1)


def merge_sort_and_count_inversions(arr: list[int], left: int, right: int) -> int:
    """Use merge sort on 'arr' to count inversions."""
    # 1-element subarray -> no inversions
    if left == right:
        return 0

    mid = (left + right) // 2
    count_left = merge_sort_and_count_inversions(arr, left=left, right=mid)
    count_right = merge_sort_and_count_inversions(arr, left=mid + 1, right=right)
    count_merged = merge_and_count_inversions(arr, left, mid, right)
    return count_left + count_right + count_merged


def merge_and_count_inversions(arr: list[int], left: int, mid: int, right: int) -> int:
    """Merge 2 sorted subarrays and count inversions."""
    count = 0  # number of inversions

    left_arr = arr[left : mid + 1]
    right_arr = arr[mid + 1 : right + 1]
    n1 = mid - left + 1
    n2 = right - mid

    i = j = 0
    k = left

    while i < n1 and j < n2:
        if left_arr[i] <= right_arr[j]:
            arr[k] = left_arr[i]
            i += 1
        else:
            # left_arr[i] > right-arr[j]
            # -> all items in left_arr[i:n1] can form inversion with right_arr[j]
            count += n1 - i

            arr[k] = right_arr[j]
            j += 1
        k += 1

    while i < n1:
        arr[k] = left_arr[i]
        i += 1
        k += 1
    while j < n2:
        arr[k] = right_arr[j]
        j += 1
        k += 1

    return count


"""
Complexity:
- Same as complexity of merge sort since counting takes O(1)

1. Time complexity: O(n * log(n))
2. Space complexity: O(n)
"""
