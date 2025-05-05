# You are given a 0-indexed integer array piles,
# where piles[i] represents the number of stones in the ith pile,
# and an integer k. You should apply the following operation exactly k times:
#
# Choose any piles[i] and remove floor(piles[i] / 2) stones from it.
# Notice that you can apply the operation on the same pile more than once.
#
# Return the minimum possible total number of stones remaining after applying the k operations.

# Example 1:
# Input: piles = [5,4,9], k = 2
# Output: 12
# Explanation: Steps of a possible scenario are:
# - Apply the operation on pile 2. The resulting piles are [5,4,5].
# - Apply the operation on pile 0. The resulting piles are [3,4,5].
# The total number of stones in [3,4,5] is 12.

# Example 2:
# Input: piles = [4,3,6,7], k = 3
# Output: 12
# Explanation: Steps of a possible scenario are:
# - Apply the operation on pile 2. The resulting piles are [4,3,3,7].
# - Apply the operation on pile 3. The resulting piles are [4,3,3,4].
# - Apply the operation on pile 0. The resulting piles are [2,3,3,4].
# The total number of stones in [2,3,3,4] is 12.

# Constraints:
# 1 <= piles.length <= 10^5
# 1 <= piles[i] <= 10^4
# 1 <= k <= 10^5


# ===== Analyze =====
# - To have the minimum number of stones remaining, we should remove as much stones
#   as possible at each step
# -> Select the pile with the most number of stones at each step
# -> Use a max heap

import heapq


def min_stones(piles: list[int], k: int) -> int:
    # Simulate a max heap by negating the values
    piles = [-pile for pile in piles]
    heapq.heapify(piles)

    # Iterate k times
    for _ in range(k):
        # Retrieve the pile with the most number of stones
        max_pile = -heapq.heappop(piles)

        # Remove half of the stones from that pile
        heapq.heappush(piles, -(max_pile - max_pile // 2))

    # Return the total number of stones left
    return -sum(piles)


# ===== Complexity =====
# Time complexity: O(n + k*log(n))
# - heapify piles: O(n)
# - k iterations:
#   + heap push: O(log(n))
#   + heap pop: O(log(n))
# - sum over remaining piles: O(n)
#
# Space complexity: O(n) for the heap
