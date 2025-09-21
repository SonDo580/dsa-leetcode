# Find all valid combinations of k numbers that sum up to n
# such that the following conditions are true:
# - Only numbers 1 through 9 are used.
# - Each number is used at most once.
#
# Return a list of all possible valid combinations.
# The list must not contain the same combination twice,
# and the combinations may be returned in any order.

# Example 1:
# Input: k = 3, n = 7
# Output: [[1,2,4]]
# Explanation:
# 1 + 2 + 4 = 7
# There are no other valid combinations.

# Example 2:
# Input: k = 3, n = 9
# Output: [[1,2,6],[1,3,5],[2,3,4]]
# Explanation:
# 1 + 2 + 6 = 9
# 1 + 3 + 5 = 9
# 2 + 3 + 4 = 9
# There are no other valid combinations.

# Example 3:
# Input: k = 4, n = 1
# Output: []
# Explanation: There are no valid combinations.
# Using 4 different numbers in the range [1,9],
# the smallest sum we can get is 1+2+3+4 = 10 and since 10 > 1,
# there are no valid combination.

# Constraints:
# 2 <= k <= 9
# 1 <= n <= 60


# ===== Strategy =====
# - Build each combination using a recursive function backtrack(current, start, current_sum),
#   . current: the combination being built.
#   . start: the index that represents where we should start iterating.
#   . current_sum: the sum of all numbers in 'current'.
# - We need start to avoid duplicates. Because order doesn't matter in a combination,
#   only combine current element and elements that come after it.
# - Only keep exploring if current_sum is less than target.
# - When current.length reaches k:
#   + If current_sum = target, add 'current' to result.
#   + Otherwise, go back and try other options.


def combinations_with_target_sum_3(k: int, n: int) -> list[list[int]]:
    answer: list[list[int]] = []

    def backtrack(current: list[int], start: int, current_sum: int):
        if len(current) == k and current_sum == n:
            # - We mutate 'current' across 'backtrack' calls,
            #   -> create a copy of 'current' when adding
            answer.append(current[:])
            return

        for num in range(start, 10):
            next_sum = current_sum + num
            if next_sum <= n:
                current.append(num)
                backtrack(current, num + 1, next_sum)
                current.pop()

    backtrack(current=[], start=1, current_sum=0)
    return answer
