"""
Key idea:
- Have an array with indices represents value range in sorted order.
  Count the frequency of each value.
- Convert counts to prefix sums to know the last index
  of each value in the sorted array.
- Iterate through the original array.
  Place each value at the last index of its block in the sorted array.
  Decrease counter for that block to move the last index to the left.
"""

"""
Explanation:
- For each value x, its block in the sorted array has size count[x]
- Block ranges for each value in sorted array:
  . 0's indices: 0 -> c[0] - 1
  . 1's indices: c[0] -> c[0] + c[1] - 1
  . 2's indices: c[0] + c[1] -> c[0] + c[1] + c[2] - 1
  . ...
  . x's indices: c[0] + ... + c[x - 1] -> c[0] + ... + c[x - 1] + c[x] - 1
=> If we compute prefix_sum[x] = c[0] + c[1] + ... + c[x],
   it gives the (end_index + 1) for x in the sorted array.
"""


def counting_sort(arr: list[int]) -> None:
    if not arr:
        return

    # Find the maximum value
    max_val = max(arr)

    # Count frequency of each element
    count = [0] * (max_val + 1)
    for num in arr:
        count[num] += 1

    # Compute prefix sum (cumulative count)
    for i in range(1, max_val + 1):
        count[i] += count[i - 1]

    # Build output array (iterate in reverse order to keep it stable)
    n = len(arr)
    ans = [0] * n
    for num in reversed(arr):
        ans[count[num] - 1] = num
        count[num] -= 1

    # Copy sorted array back to original array
    for i in range(n):
        arr[i] = ans[i]


"""
Complexity:
- Let n = len(arr)
      k = max(arr)

1. Time complexity:
- Find maximum value: O(n)
- Build 'count': O(n)
- Compute prefix sum on 'count': O(k)
- Initialize and fill 'ans': O(n)
- Copy 'ans' back to 'arr': O(n)
=> Overall: O(n + k)

2. Space complexity: O(n + k)
- 'count': O(k)
- 'sorted_arr': O(n)
"""

"""
Stability: stable
- We scan the input from right to left and place each value at 
  the last available position in its block.
"""

"""
Features:
- non-comparison-based sorting algorithm.
- efficient when k is small compared to n.
- doesn't work with decimal values -> can use bucket sort.
- if k >> n -> use comparison-based sorting algorithm (merge sort, quick sort).
"""


# ========== EXTRA ==========
# ===========================
"""
- If stability is not important, simply count occurrences of all elements 
  then output them one by one.
- With this approach we can also modify array in-place.
"""


def counting_sort_v2(arr: list[int]) -> None:
    if not arr:
        return

    # Find the maximum value
    max_val = max(arr)

    # Count frequency of each element
    count = [0] * (max_val + 1)
    for num in arr:
        count[num] += 1

    # Place numbers into original array in order
    k = 0
    for i in range(len(count)):
        for _ in range(count[i]):
            arr[k] = i
            k += 1


"""
Complexity:

1. Time complexity: O(n)
- Find maximum value: O(n)
- Build 'count': O(n)
- Place number into original array: O(n)

2. Space complexity: O(k) for 'count'
"""
