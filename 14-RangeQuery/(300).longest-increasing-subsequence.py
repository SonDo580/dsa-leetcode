"""
https://leetcode.com/problems/longest-increasing-subsequence/

Given an integer array 'nums',
return the length of the longest strictly increasing subsequence.
"""

# === Approach 1: DP ===
"""
- Let dp(i) be the length of the LIS that ends at nums[i].
  -> dp(i) = max(1 + dp(j) for j in [0..i-1] if nums[j] < nums[i])
- Each nums[i] is a subsequence of length 1.
- Result: max(dp(i) for i in [0..n-1])
"""


def length_of_LIS(nums: list[int]) -> int:
    n = len(nums)
    dp: list[int] = [1] * n  # each nums[i] is a 1-item subsequence
    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)


"""
Complexity:
- Let n = len(nums)
- Number of DP states: O(n)

1. Time complexity: O(n^2)
- Init 'dp': O(n)
- Fill 'dp': O(n^2)
  . total number of inner loop iterations:
    0 + 1 + ... + n - 1 = n * (n - 1) / 2
- Find max(dp): O(n)

2. Space complexity: O(n) for 'dp'
   (can not be improved since recurrence relation is not static)
"""

# === Approach 2: Binary search ===
"""
- Use an array 'tails' to store tails for LISs of different lengths.
- A subsequence of length L-1 can be extended to length L
  if current item > smallest tail of LIS with length L-1
  -> tails[L] should track current smallest tail of LIS with length L-1.
- Since we only extends the LIS if current item > max tail,
  'tails' is strictly increasing.
- We also replace tails[L] with current item if current item < tails[L]
  (so the LIS of length L-1 has more chance to be extended later),
  which keeps the increasing order.
  -> Use binary search to find tails[L] since 'tails' is sorted.
- The final length of 'tails' is the length of the LIS.
"""


def _bisect_left(arr: list[int], num: int) -> int:
    """Return the smallest i where arr[i] >= num ('arr' is increasing)."""
    left = 0
    right = len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] >= num:
            right = mid - 1  # find smaller i that is still valid
        else:
            left = mid + 1  # find valid i
    return left


def length_of_LIS(nums: list[int]) -> int:
    tails: list[int] = []
    for num in nums:
        if not tails or num > tails[-1]:
            tails.append(num)
        else:
            idx = _bisect_left(tails, num)
            tails[idx] = num
    return len(tails)


"""
Complexity:

1. Time complexity: O(n*log(n))
- Iterate through 'nums': n iterations
  . binary search in 'tails': O(log(n))

2. Space complexity: O(n) for 'tails'
"""


# === Approach 3: Segment tree ===
# (optimize approach 1 - DP)
"""
DP approach:
- At each nums[i], we need iterate through dp[0..i-1]
  to find the max dp[j] such that nums[j] < nums[i]

Reduce query time: 
- Find rank of each number:
  . sort 'nums' and use bisect left to find number of smaller items for each item.
  . equal numbers will have the same rank.
- Use a segment tree where the root manages the whole range of ranks
  . node's value = length of LIS ends at a node with rank in node's managed range
    -> node's value = max(left_child's value, right_child's value)
- Iterate through 'nums' in forward order. At each nums[i]:
  . Query for length of LIS in range [0..rank-1]
    (max length among LISs ending at an processed nums[j] where nums[j] < nums[i])
  . Update tree: insert length of LIS ending at nums[i]
"""


def _produce_ranks(nums: list[int]) -> tuple[list[int], int]:
    """
    Return rank of each item and max rank.
    (rank = number of smaller items)
    """
    sorted_nums = sorted(nums)
    ranks: list[int] = []
    max_rank = -1

    for num in nums:
        idx = _bisect_left(sorted_nums, num)
        max_rank = max(max_rank, idx)
        ranks.append(idx)

    return ranks, max_rank


class SegmentTree:
    def __init__(self, max_rank: int):
        # node's value = length of LIS ending at at item of rank 'rank'
        #                where 'rank' is in node's managed range
        self.tree = [0] * 4 * (max_rank + 1)  # rank is 0-indexed

    def update(self, rank: int, LIS_len: int, left: int, right: int, i: int) -> None:
        """Insert length of LIS (so far) ending at an item of rank 'rank'."""
        if left == right:  # reached leaf node
            self.tree[i] = LIS_len
            return

        mid = (left + right) // 2
        lci = 2 * i + 1
        rci = 2 * i + 2
        if rank <= mid:  # target is in left subtree
            self.update(rank, LIS_len, left, mid, lci)
        else:  # target is in right subtree
            self.update(rank, LIS_len, mid + 1, right, rci)

        # aggregate result after updating children
        self.tree[i] = max(self.tree[lci], self.tree[rci])

    def query_range(
        self, qleft: int, qright: int, left: int, right: int, i: int
    ) -> int:
        """Return length of LIS ending at a node with rank in range [qleft..qright]."""
        if qleft > qright:
            # rank == 0 (smallest value)
            # -> can only extend empty subsequence
            #    (due to strictly increasing requirement)
            return 0

        # node's range is outside query range
        if qright < left or right < qleft:
            # constructing result in parent: max(x, -1) = x
            # (the sibling of node i should have range overlapping
            #  with query range, so x >= 0)
            return -1

        # node's range is fully contained in query range
        # -> return precomputed value
        if qleft <= left and right <= qright:
            return self.tree[i]

        # partial overlap -> query both halves then aggregate result
        mid = (left + right) // 2
        left_res = self.query_range(qleft, qright, left, mid, 2 * i + 1)
        right_res = self.query_range(qleft, qright, mid + 1, right, 2 * i + 2)
        return max(left_res, right_res)


class Solution:
    def lengthOfLIS(self, nums: list[int]) -> int:
        ranks, max_rank = _produce_ranks(nums)
        st = SegmentTree(max_rank)
        for i in range(len(nums)):
            # find length of LIS ends at nums[i],
            # then insert that length to segment tree
            rank = ranks[i]
            lis_len = 1 + st.query_range(
                qleft=0, qright=rank - 1, left=0, right=max_rank, i=0
            )
            st.update(rank, lis_len, left=0, right=max_rank, i=0)

        # segment tree root holds the length of the LIS
        # after processing all numbers
        return st.tree[0]

"""
Complexity:
- Let n = len(nums)
  -> max_rank = O(n)
- Segment tree is full and balanced
  -> . number of nodes: O(4*n) = O(n)
     . height: h = O(log(4*n)) = O(n)

1. Time complexity: O(n*log(n))
- Produce 'ranks': O(n*log(n))
  . sort 'nums': O(n*log(n))
  . binary search on sorted 'nums' for n numbers: O(n*log(n))
- Init 'st': O(4*n) = O(n)
- query_range/update for n numbers: O(n*log(n))

2. Space complexity: O(n)
- sorted 'nums': O(n)
- 'ranks': O(n)
- 'st': O(4*n) = O(n)
- recursion stack: O(h) = O(log(n))
"""