# Given an array of distinct positive integers 'candidates' and a target integer target,
# return a list of all unique combinations of candidates where the chosen numbers sum to target.
# The same number may be chosen from candidates an unlimited number of times.
# Two combinations are unique if the frequency of at least one of the chosen numbers is different.


# ===== Strategy =====
# - Build each combination using a recursive function backtrack(current, start, current_sum),
#   . current: the combination being built.
#   . start: the index that represents where we should start iterating.
#   . current_sum: the sum of all numbers in 'current'.
# - We need start to avoid duplicates. Because order doesn't matter in a combination,
#   only combine current element and elements that come after it.
# - In this problem we are allowed to use the same number multiple times,
#   -> use the same number in the recursive backtrack call,
#      but increase the sum to indicate that we used it.
# - Only keep exploring if current_sum is less than target.
#   When 'current_sum' reaches 'target', add 'current' to result.


def combinations_with_target_sum(candidates: list[int], target: int) -> list[list[int]]:
    answer: list[list[int]] = []

    def backtrack(current: list[int], start: int, current_sum: int):
        if current_sum == target:
            # - We mutate 'current' across 'backtrack' calls,
            #   -> create a copy of 'current' when adding
            answer.append(current[:])
            return

        for i in range(start, len(candidates)):
            num = candidates[i]
            next_sum = current_sum + num
            if next_sum <= target:
                current.append(num)
                backtrack(current, i, next_sum)
                current.pop()

    backtrack(current=[], start=0, current_sum=0)
    return answer
