"""
https://leetcode.com/problems/count-of-smaller-numbers-after-self/

Given an integer array 'nums',
return an integer array 'counts' where counts[i] is
the number of smaller elements to the right of nums[i].
"""

# === Approach 1: Brute-force (exceed time limit) ===
"""
- For each nums[i], iterate through nums[i+1:] to find smaller elements.
"""


def count_smaller(nums: list[int]) -> list[int]:
    n = len(nums)
    count: list[int] = [0] * n
    for i in range(n - 1):
        for j in range(i + 1, n):
            if nums[j] < nums[i]:
                count[i] += 1
    return count


"""
Complexity:
1. Time complexity: O(n^2)
2. Space complexity: O(1)
"""


# === Approach 2: Merge Sort ===
"""
- When merging 2 arrays 'left' and 'right'.
  . All items in 'right' are to the right of all items in 'left'.
  . If left[i] > right[j]:
    . If sort in ascending order:
      -> all items in left[i:] > right[j]
      -> increment count for all items in left[i:]
         (inefficient)
    . If sort in descending order:
      -> left[i] > all items in right[j:]
      -> count for left[i] increases by len(right)-j
  -> Sort in descending order.
- We need to track original index i to update count[i] 
  -> group index and value before sorting.
"""


def count_smaller(nums: list[int]) -> list[int]:
    n = len(nums)
    count: list[int] = [0] * n
    nums_with_indices = [(num, i) for i, num in enumerate(nums)]
    _merge_sort(nums_with_indices, 0, n - 1, count)
    return count


def _merge_sort(
    nums_with_indices: list[tuple[int, int]], left: int, right: int, count: list[int]
) -> None:
    """
    Sort nums_with_indices in descending order.
    Record number of smaller items to the right of each item.
    """
    if left == right:
        return

    mid = (left + right) // 2
    _merge_sort(nums_with_indices, left, mid, count)
    _merge_sort(nums_with_indices, mid + 1, right, count)
    _merge(nums_with_indices, left, mid, right, count)


def _merge(
    nums_with_indices: list[tuple[int, int]],
    left: int,
    mid: int,
    right: int,
    count: list[int],
) -> None:
    """
    Merge 2 arrays sorted in descending order.
    Record number of smaller items to the right of each item.
    """
    sorted_arr: list[tuple[int, int]] = []
    i = left
    j = mid + 1

    while i <= mid and j <= right:
        left_val, left_idx = nums_with_indices[i]
        right_val, _ = nums_with_indices[j]
        if left_val > right_val:
            count[left_idx] += right - j + 1
            sorted_arr.append(nums_with_indices[i])
            i += 1
        else:  # unstable sort is acceptable
            sorted_arr.append(nums_with_indices[j])
            j += 1

    while i <= mid:
        sorted_arr.append(nums_with_indices[i])
        i += 1
    while j <= right:
        sorted_arr.append(nums_with_indices[j])
        j += 1

    nums_with_indices[left : right + 1] = sorted_arr


"""
Complexity:
- Let n = len(nums)

1. Time complexity: O(n*log(n))
- Init count: O(n)
- Group values with indices: O(n)
- Merge sort: O(n*log(n))
  . Sub-array size at each level:
    . n, n / 2, n / 4, ..., n / 2^k
    . n / 2^k = 1 (base case) -> k = log2(n)
    -> Number of levels (recursion depth): O(log(n))
  . Total merge work at each level: O(n)
  -> Work across levels: O(n*log(n))

2. Space complexity: O(n)
- 'num_with_indices': O(n)
- Merge sort: O(n)
  . recursion stack: O(log(n))
  . temporary array for merging: O(n)
"""


# === Approach 3: Segment Tree ===
"""
Idea:
- Find number of smaller items of each item when the array is sorted
  (produce array of ranks):
  . Produce sorted array (ascending order).
  . For each nums[i] in original array, find smallest j in sorted array 
    such that sorted_arr[j] >= nums[i] (bisect left / lower bound).
    (equal items have the same rank)
  . j = number of (all) items smaller than nums[i]
      = rank of nums[i]
- Use a segment tree to manage the whole range of ranks.
  . node's value is number of items with rank in node's managed range
    -> node's value = left_child's value + right_child's value. 
- Process original array in reverse order:
  . At nums[i], query how many items have been inserted into the range [0, rank-1].
    That's number of smaller items than nums[i] on the right in original array
    (since we process the original array in reverse order).
  . Update segment tree to reflect that nums[i] has been encounter
    (increase number of items for nums[i]'s rank)
"""


class SegmentTree:
    def __init__(self, max_rank: int):
        # node's value = number of items with rank in node's managed range
        self.tree = [0] * 4 * (max_rank + 1)  # rank is 0-indexed

    def update(self, rank: int, left: int, right: int, i: int) -> None:
        """Update when encountering an item with rank 'rank'."""
        if left == right:  # reached leaf node
            self.tree[i] += 1
            return

        mid = (left + right) // 2
        lci = 2 * i + 1
        rci = 2 * i + 2
        if rank <= mid:  # target is in left child
            self.update(rank, left, mid, lci)
        else:  # target is in right child
            self.update(rank, mid + 1, right, rci)

        # update node after updating children
        self.tree[i] = self.tree[lci] + self.tree[rci]

    def query_range(self, rank: int, left: int, right: int, i: int) -> int:
        """Return number of items with rank < 'rank'."""
        # rank 0 has no smaller items
        if rank == 0:
            return 0

        qleft, qright = 0, rank - 1

        # node's range is outside query range
        if qright < left or right < qleft:
            return 0

        # node's range is fully contained in query range
        # -> return precomputed result
        if qleft <= left and right <= qright:
            return self.tree[i]

        # partial overlap
        # -> query both halves and aggregate
        mid = (left + right) // 2
        left_res = self.query_range(rank, left, mid, 2 * i + 1)
        right_res = self.query_range(rank, mid + 1, right, 2 * i + 2)
        return left_res + right_res


def _bisect_left(arr: list[int], x: int) -> int:
    """Return smallest i such that arr[i] >= x (arr is ascending)."""
    left = 0
    right = len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] >= x:
            right = mid - 1  # search lower half for smaller answer
        else:
            left = mid + 1  # search upper half for valid answer
    return left


def _get_ranks(nums: list[int]) -> tuple[list[int], int]:
    """
    Return rank of each number in sorted nums and max rank.
    (rank = number of items smaller than current item)
    """
    sorted_nums = sorted(nums)
    ranks: list[int] = []
    max_rank = -1

    for num in nums:
        idx = _bisect_left(sorted_nums, num)
        max_rank = max(max_rank, idx)
        ranks.append(idx)

    return ranks, max_rank


class Solution:
    def countSmaller(self, nums: list[int]) -> list[int]:
        n = len(nums)
        ans: list[int] = [0] * n
        ranks, max_rank = _get_ranks(nums)
        st = SegmentTree(max_rank)

        for i in range(n - 1, -1, -1):
            rank = ranks[i]
            ans[i] = st.query_range(rank, left=0, right=max_rank, i=0)
            st.update(rank, left=0, right=max_rank, i=0)

        return ans


"""
Complexity:
- Let n = len(nums)
  -> max_rank = O(n) (worst case: all numbers are unique)
- The tree is full and balanced
  -> . number of nodes: O(4*n) = O(n) (last level contains empty slots)
     . height: h = O(log(4*n)) = O(log(n))

1. Time complexity:
- Init 'ans': O(n)
- Produce 'ranks': O(n*log(n))
  . sort array: O(n*log(n)) 
  . bisect left for n numbers: O(n*log(n))
- Init 'st': O(4*n) = O(n)
- Perform st.query and st.update for n numbers: O(n*log(n))
  . st.update: O(h) = O(log(n))
    . Each update follow exactly 1 path from root to a leaf
  . st.query: O(log(n))
    . At most 2 nodes per level can spawn extra calls, 2 calls per node
      (Only boundaries can overlap partially with query range)
      -> At most 4 nodes are processed at each level.
      -> Work across levels: O(4*h) = O(log(n)) 

2. Space complexity: O(n)
- sorted 'nums': O(n)
- 'ranks': O(n)
- 'st': O(4*n) for 'tree'
- recursion stack: O(h) = O(log(n))
"""
