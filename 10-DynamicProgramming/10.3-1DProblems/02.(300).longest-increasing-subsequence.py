"""
https://leetcode.com/problems/longest-increasing-subsequence

Given an integer array 'nums',
return the length of the longest strictly increasing subsequence.

Example 1:
Input: nums = [10,9,2,5,3,7,101,18]
Output: 4
Explanation: The longest increasing subsequence is [2,3,7,101], therefore the length is 4.

Example 2:
Input: nums = [0,1,0,3,2,3]
Output: 4

Example 3:
Input: nums = [7,7,7,7,7,7,7]
Output: 1

Constraints:
1 <= nums.length <= 2500
-10^4 <= nums[i] <= 10^4

Follow up: Can you come up with an algorithm that runs in O(n * log(n)) time complexity?
"""

# ===== Approach 1: DP =====
# ==========================
"""
Identify DP problem:
- ask for maximum subsequence length.
- taking an element affects elements we can take later.

Solution:
- Let dp[i] be the length of the LIS that ends with nums[i].
- We can add nums[i] to subsequences that end with nums[j] (0 <= j < i)
  if nums[j] < nums[i] (strictly increasing).
  -> dp[i] = max(dp[j] + 1) where j is in [0, i) and nums[j] < nums[i]
- Base case: every element is a subsequence with length 1.
- Find the length of the LIS that ends at each index,
  and take the maximum of those.
"""


# ----- Bottom-up -----
def length_of_LIS(nums: list[int]) -> int:
    n = len(nums)
    dp: list[int] = [1] * n

    for i in range(n):
        for j in range(i):
            if nums[i] > nums[j]:
                dp[i] = max(dp[i], dp[j] + 1)

    return max(dp)


"""
1. Time complexity: O(n^2)
- build 'dp': O(n^2)
- find max(dp): O(n)

2. Space complexity: O(n) for 'dp' array
- Space complexity cannot be improved since the recurrence relation is not static:
  + Static recurrence relation means the next state depends on
    a fixed number of previous states.
  + In this problem, each dp[i] depends on a variable number of
    previous states (dp[j] where j in [0, i) and nums[i] > nums[j]).
"""


# ----- Top-down -----
def length_of_LIS(nums: list[int]) -> int:
    memo: dict[int, int] = {}

    def dp(i: int) -> int:
        if i in memo:
            return memo[i]

        max_len = 1
        for j in range(i):
            if nums[i] > nums[j]:
                max_len = max(max_len, dp(j) + 1)

        memo[i] = max_len
        return max_len

    return max(dp(i) for i in range(len(nums)))


"""
1. Time complexity: O(n^2)
- Find dp(i): O(n) (because of caching)
  Repeat for n elements.

2. Space complexity: O(n)
- memo: O(n)
- recursion stack: O(1) (because of caching)
"""


# ===== Approach 2: Binary search =====
# (see BinarySearch section)


# ===== Extra: Find 1 specific LIS =====
# ======================================
"""
- We can modify the algorithm to reconstruct 1 LIS
- Let's use:
  + 'dp': dp[i] = the length of 1 LIS that ends with nums[i]
  + 'prev': prev[i] = index of the previous element in 1 LIS ending at nums[i].
                      (or -1 if nums[i] starts a subsequence)
- Update both 'dp' and 'prev' at each step.
- At the end, reconstruct 1 LIS:
  + Find the ending index of the LIS.
  + Walk 'prev' backwards.               
"""


def LIS(nums: list[int]) -> list[int]:
    n = len(nums)
    dp: list[int] = [1] * n
    prev: list[int] = [-1] * n

    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i] and dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
                prev[i] = j

    # Find the ending index of the LIS
    lis_len = max(dp)
    k = dp.index(lis_len)

    # Reconstruct the LIS
    reversed_lis: list[int] = []
    while k != -1:
        reversed_lis.append(nums[k])
        k = prev[k]  # trace backwards

    return list(reversed(reversed_lis))


"""
Complexity:

1. Time complexity:
- Build 'dp' and 'prev': O(n^2)
- Find ending index of LIS: O(n)
- Recover LIS (trace then reverse): O(n)
=> Overall: O(n^2)

2. Space complexity:
- 'dp': O(n)
- 'prev': O(n)
=> Overall: O(n)
"""


# ===== Extra: Find all LISs =====
# ================================
"""
- To recover all LISs, modify the find_one algorithm.
- Let prev[i] store the list of predecessor indices in all LISs ending at nums[i].
- After computing 'dp' and 'prev', find all indices where dp[i] = length of LIS.
  Each is a valid ending point.
- Perform DFS/backtracking from those points through 'prev' to enumerate all LISs.
"""


def all_LISs(nums: list[int]) -> list[list[int]]:
    n = len(nums)
    dp: list[int] = [1] * n
    prev: list[list[int]] = [[] for _ in range(n)]

    for i in range(n):
        for j in range(i):
            if nums[j] >= nums[i]:
                continue

            # found a longer subsequence
            if dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
                prev[i] = [j]  # reset predecessor list

            # found another subsequence with current max length
            elif dp[j] + 1 == dp[i]:
                prev[i].append(j)  # add another predecessor

    # Find the ending indices of all LISs
    lis_len = max(dp)
    end_indices = [i for i in range(n) if dp[i] == lis_len]

    # Collect and return all LISs
    return _collect_LISs_recur(nums, prev, end_indices)
    # return _collect_LISs_iter(nums, prev, end_indices)

"""
Complexity: TODO
"""


def _collect_LISs_recur(
    nums: list[int], prev: list[list[int]], end_indices: list[int]
) -> list[list[int]]:
    lis_list: list[list[int]] = []
    reversed_path: list[int] = []  # shared and mutable

    def dfs(i: int) -> None:
        reversed_path.append(nums[i])

        if len(prev[i]) == 0:
            # Found 1 complete LIS
            lis_list.append(list(reversed(reversed_path)))
        else:
            # Explore all predecessors
            for p in prev[i]:
                dfs(p)

        reversed_path.pop()  # backtrack

    # Start DFS from each LIS ending index
    for i in end_indices:
        dfs(i)

    return lis_list


def _collect_LISs_iter(nums: list[int], prev: list[list[int]], end_indices: list[int]):
    lis_list: list[list[int]] = []
    reversed_path: list[int] = []  # shared and mutable

    # Stack item: (i, j)
    # . i: index in 'nums'
    # . j: next predecessor to explore (index in prev[i])
    stack: list[tuple[int, int]] = [(i, 0) for i in end_indices]

    while len(stack) > 0:
        i, j = stack.pop()

        # First encounter of nums[i] (haven't explored predecessors)
        # -> add it to path
        if j == 0:
            reversed_path.append(nums[i])

        # Found 1 complete LIS -> record and backtrack
        if len(prev[i]) == 0:
            lis_list.append(list(reversed(reversed_path)))
            reversed_path.pop()  # pop nums[i]
            continue

        # All predecessors explored -> backtrack
        if j == len(prev[i]):
            reversed_path.pop()  # pop nums[i]
            continue

        # Push state to explore the next predecessor later
        stack.append((i, j + 1))

        # Push state to explore current predecessor in the next iteration
        p = prev[i][j]
        stack.append((p, 0))

    return lis_list
