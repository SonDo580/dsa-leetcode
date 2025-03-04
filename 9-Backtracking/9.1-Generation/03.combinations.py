# Given two integers n and k,
# return all possible combinations of k numbers chosen from the range [1, n].
# You may return the answer in any order.

# Example 1:
# Input: n = 4, k = 2
# Output: [[1,2],[1,3],[1,4],[2,3],[2,4],[3,4]]
# Explanation: There are 4 choose 2 = 6 total combinations.
# Note that combinations are unordered, i.e., [1,2] and [2,1] are considered to be the same combination.

# Example 2:
# Input: n = 1, k = 1
# Output: [[1]]
# Explanation: There is 1 choose 1 = 1 total combination.

# Constraints:
# 1 <= n <= 20
# 1 <= k <= n


# ===== Analyze =====
# - Let n = nums.length
# - Number of combinations: nCk = n! / k!(n - k)!
# - Base case:
#   + nCn = 1 (1 item - the list with all numbers in range)
#   + nC1 = n (each item is a list containing 1 number in the range)
# - When building combination, we have:
#   + n options for the first slot
#   + n - 1 options for the second slot
#   + ...
#   + n - k + 1 options for the last slot


# ===== Recursive divide-and-conquer =====
# (*) Note:
# - When performing the recursive call, only includes the ones that come after current number.
# - Allowing numbers before current number will generate duplicated combinations.
#   (because order doesn't matter in combination)
def combine(n: int, k: int) -> list[list[int]]:
    def recur(start: int, end: int, k: int) -> list[list[int]]:
        """Return all combinations of k numbers chosen from [start, end]"""
        full_range = range(start, end + 1)

        # k == end -> return full range
        if k == end:
            return [list(full_range)]

        # k == 1 -> return single-element lists
        if k == 1:
            return [[i] for i in full_range]

        result: list[list[int]] = []
        for i in full_range:
            # Find all combinations of k - 1 numbers from remaining numbers
            remaining_combinations = recur(i + 1, end, k - 1)

            # Combine current number with each combination
            for combination in remaining_combinations:
                result.append([i] + combination)

        return result

    return recur(1, n, k)
