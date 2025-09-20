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


# ===== Analysis =====
# - Let n = nums.length
# - Number of combinations with k elements: nCk = n! / k!(n - k)!
# - Base case:
#   + nCn = 1 (1 item - the list with all numbers in range)
#   + nC1 = n (each item is a list containing 1 number in the range)
# - When building combination, we have:
#   + n options for the first slot
#   + n - 1 options for the second slot
#   + ...
#   + n - k + 1 options for the last slot


# ===== Strategy =====
# - Use a recursive function recur(start, end, k) to generate combination.
# - Base cases:
#   . k = n -> result contains a list of all numbers (nCn = 1)
#   . k = 1 -> result contains n single-element lists (nC1 = n)
# - For the general case, loop through each number:
#   + Find all combinations with k - 1 elements from the remaining numbers.
#     Only includes the ones that come after current number to avoid duplicates,
#     since order doesn't matter in combination.
#   + Prepend the current number of to each combination generated
#     from the remaining numbers, then add to result.
def get_combinations(n: int, k: int) -> list[list[int]]:
    def recur(start: int, end: int, k: int) -> list[list[int]]:
        """Return all combinations of k numbers chosen from [start, end]"""
        full_range = range(start, end + 1)

        if k == end:
            return [list(full_range)]

        if k == 1:
            return [[i] for i in full_range]

        all_combinations: list[list[int]] = []
        for i in full_range:
            remaining_combinations = recur(i + 1, end, k - 1)
            for combination in remaining_combinations:
                all_combinations.append([i] + combination)

        return all_combinations

    return recur(1, n, k)


# ===== Approach 2 =====
# - Build each combination using a recursive function backtrack(current, i),
#   where 'current' is the combination being built,
#   i is the index that represents where we should start iterating.
# - We need i to avoid duplicates. Because order doesn't matter in a combination,
#   only combine current element and elements that come after it.
# - When 'current' reaches length k, add it to result.


def get_combinations(n: int, k: int) -> list[list[int]]:
    all_combinations: list[list[int]] = []

    def backtrack(current: list[int], i: int):
        if len(current) == k:
            # - We mutate 'current' across 'backtrack' calls,
            #   -> create a copy of 'current' when adding
            all_combinations.append(current[:])
            return

        for num in range(i, n + 1):
            current.append(num)
            backtrack(current, num + 1)
            current.pop()

    backtrack([], 1)
    return all_combinations
