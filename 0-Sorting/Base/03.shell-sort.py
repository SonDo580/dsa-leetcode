"""
Insertion sort's weakness:
- Elements only move 1 position at a time.
- If a small element is at the very end of an array.
  -> takes O(n) steps just to "drag" that element to the front.

Shell sort's key idea:
- Compare and shift elements that are far apart first
"""

"""
Implementation:
- Break the array into several smaller sub-array using a gap.
  Elements in each sub-array are spaced 'gap' positions apart.
- Apply insertion sort to these sub-arrays.
- The gap is gradually reduced (usually halved) in each pass.
  The final pass always uses a gap of 1, which is standard insertion sort.
  If the array is "nearly sorted' by then, the final pass will run very fast.
"""


def shell_sort(arr: list[int]) -> None:
    n = len(arr)

    # start with a large gap
    gap = n // 2

    while gap > 0:
        # perform gapped insertion sort for each sub-array
        # - the 1st item of each sub-array is in range [0..gap-1]
        # - remaining items of all sub-arrays is in range [gap..n-1]
        for i in range(gap, n):
            current = arr[i]  # current element to insert
            j = i

            # shift element of the gapped sorted portion to the right
            # until we find the correct position for current
            while j >= gap and arr[j - gap] > current:
                arr[j] = arr[j - gap]
                j -= gap

            # insert current at its correct position
            arr[j] = current

        # reduce the gap
        gap //= 2


"""
Complexity:

1. Time complexity:
- Number of gap levels: O(log(n))
- Best case: O(n*log(n)) 
  . when: array has already sorted.
  . at each gap level, iterate through array from 'gap' to n.
  . in each iteration, the condition arr[j - gap] > current is check once
    and return False immediately, no shiftings happen.
- Worst case: O(n^2) 
  . when: elements in odd positions are very large and
    elements in even positions is very small, or vice versa.
  . the elements in odd positions and even positions
    are never compared and until the final pass where gap = 1.
    -> no useful "mixing" happened during the large-gap phases
    -> same O(n^2) behavior as standard insertion sort.

Fix worst case: 
- don't use n // 2 sequence for gaps.
- use gaps that are co-prime (don't share common factors).
- practical sequences: 
  . Knuth's sequence: (3^k - 1)/2
  . Sedgewick's sequence: 9*(4^k - 2^k) + 1 OR 4^k + 3*2^(k-1) + 1
    
2. Space complexity: O(1)
"""

"""
Stability: unstable
- elements are swapped across gap -> equal elements can change relative order.
"""
