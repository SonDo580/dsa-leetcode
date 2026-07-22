"""
https://leetcode.com/problems/longest-increasing-subsequence-ii/

You are given an integer array 'nums' and an integer k.

Find the longest subsequence of 'nums' that meets the following requirements:
- The subsequence is strictly increasing and
- The difference between adjacent elements in the subsequence is at most k.

Return the length of the longest subsequence that meets the requirements.
"""

# === Approach 1: DP (exceed time limit) ===
"""
- Let dp(i) be the length of the LIS that ends at nums[i].
- A subsequence ending at j (0 <= j < i) can be extended with nums[i]
  if 0 < nums[i] - nums[j] <= k
"""


class Solution:
    def lengthOfLIS(self, nums: list[int], k: int) -> int:
        n = len(nums)
        dp = [1] * n  # each nums[i] is a 1-item subsequence
        for i in range(n):
            for j in range(i):
                if 0 < nums[i] - nums[j] <= k:
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


# === Approach 2: Segment tree ===
"""
Without "difference between adjacent elements is at most k" requirement
<-> '(300).longest-increasing-subsequence':

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

==========
Handle "difference between adjacent elements is at most k" requirement:

- For each nums[i] with rank ranks[i], 
  we need to find the smallest ranks[j] < ranks[i]
  such that nums[i] - nums[j] >= k
  -> . Group ranks with nums, sort in ascending order 
     . For each nums[i], binary search on sorted_ranks.
- Use query range [ranks[j]..ranks[i]-1] when finding
  length of LIS ending at nums[i].
  (only extend LIS ending at nums[j] where nums[i] - nums[j] <= k)
"""


def _bisect_left(asc_nums: list[int], num: int) -> int:
    """
    Return smallest i where asc_nums[i] >= num.
    (i = len(arr) if num > all items in array).
    """
    left = 0
    right = len(asc_nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if asc_nums[mid] >= num:
            right = mid - 1  # find smaller i that is still valid
        else:
            left = mid + 1  # find valid i
    return left


def _find_qleft(asc_ranks_with_nums: list[tuple[int, int]], num: int, k: int) -> int:
    """
    Return smallest rank[j] < ranks[i] such that 0 < nums[i] - nums[j] <= k.
    Return -1 if there's no valid items.
    """
    ans = -1

    left = 0
    right = len(asc_ranks_with_nums)
    while left <= right:
        mid = (left + right) // 2
        rank_mid, num_mid = asc_ranks_with_nums[mid]

        if num > num_mid:  # (rank also > rank_mid)
            if num - num_mid <= k:
                ans = rank_mid
                right = mid - 1  # try to find smaller rank that is still valid
            else:  # num - num_mid > k:
                # search upper half (increase num_mid to reduce the difference)
                left = mid + 1
        else:  # num <= num_mid
            right = mid - 1  # search lower half for valid rank

    return ans


def _find_ranks_and_qlefts_v0(
    nums: list[int], k: int
) -> tuple[list[int], int, list[int]]:
    """
    Return:
    - ranks: rank of each nums[i] (number of smaller items in sorted 'nums')
    - max rank.
    - qlefts: smallest rank[j] < ranks[i] such that 0 < nums[i] - nums[j] <= k.

    Note: order of 'ranks' and 'qlefts' is order of original 'nums'
    """
    n = len(nums)
    ranks: list[int] = []
    ranks_with_nums: list[tuple[int, int]] = []
    qlefts: list[int] = []
    max_rank = -1

    sorted_nums = sorted(nums)
    for num in nums:
        idx = _bisect_left(sorted_nums, num)
        assert 0 <= idx < n  # num is in sorted_nums -> must always found
        max_rank = max(max_rank, idx)
        ranks.append(idx)
        ranks_with_nums.append((idx, num))

    ranks_with_nums.sort()
    for num in nums:
        qleft = _find_qleft(ranks_with_nums, num, k)
        qlefts.append(qleft)

    return ranks, max_rank, qlefts


def _find_ranks_and_qlefts(nums: list[int], k: int) -> tuple[list[int], int, list[int]]:
    """
    Optimize v0: eliminate sorting step for ranks_with_nums.
    (similar idea to counting sort)
    - Init sorted_ranks_with_nums with length n.
    - 1st item of each rank goes to rank-th slot.
      2nd item of each rank goes to (rank+1)-th slot.
      ...
    -> Count number of items inserted for each rank.
    """
    n = len(nums)
    ranks: list[int] = []
    qlefts: list[int] = []
    max_rank = -1
    sorted_nums = sorted(nums)

    sorted_ranks_with_nums: list[tuple[int, int]] = [None] * n
    inserted_per_rank: dict[int, int] = {}

    for num in nums:
        rank = _bisect_left(sorted_nums, num)
        assert 0 <= rank < n  # num is in sorted_nums -> must always found
        max_rank = max(max_rank, rank)
        ranks.append(rank)

        if rank not in inserted_per_rank:
            inserted_per_rank[rank] = 0
        offset = inserted_per_rank[rank]
        sorted_ranks_with_nums[rank + offset] = (rank, num)
        inserted_per_rank[rank] += 1

    for num in nums:
        qleft = _find_qleft(sorted_ranks_with_nums, num, k)
        qlefts.append(qleft)

    return ranks, max_rank, qlefts


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
        """
        Return length of LIS ending at a node with rank in range [qleft..qright].
        """
        if qleft == -1:
            # no previous smaller nums[j] such that curr_num - nums[j] <= k
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
    def lengthOfLIS(self, nums: list[int], k: int) -> int:
        ranks, max_rank, qlefts = _find_ranks_and_qlefts(nums, k)
        st = SegmentTree(max_rank)

        for i in range(len(nums)):
            # find length of LIS ends at nums[i],
            # then insert that length into segment tree
            lis_len = 1 + st.query_range(
                qleft=qlefts[i], qright=ranks[i] - 1, left=0, right=max_rank, i=0
            )
            st.update(ranks[i], lis_len, left=0, right=max_rank, i=0)

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
- Produce 'ranks' and 'qlefts': O(n*log(n))
  . sort 'nums': O(n*log(n))
  . binary search on sorted_nums for n numbers: O(n*log(n))
  . binary search on sorted_ranks_with_nums for n numbers: O(n*log(n))
- Init 'st': O(4*n) = O(n)
- query_range/update for n numbers: O(n*log(n))

2. Space complexity: O(n)
- sorted_nums: O(n)
- ranks_with_nums: O(n)
- 'ranks': O(n)
- 'qleft': O(n)
- 'st': O(4*n) = O(n)
- recursion stack (query_range/update): O(h) = O(log(n))
"""
