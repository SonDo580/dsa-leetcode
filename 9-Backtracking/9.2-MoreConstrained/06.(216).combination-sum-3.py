"""
https://leetcode.com/problems/combination-sum-iii/

Find all valid combinations of k numbers that sum up to n
such that the following conditions are true:
- Only numbers 1 through 9 are used.
- Each number is used at most once.

Return a list of all possible valid combinations.
The list must not contain the same combination twice,
and the combinations may be returned in any order.

Related constraints:
. 2 <= k <= 9
"""

"""
Idea:
- Use backtracking to find all valid combinations. States needed:
  . current: the combination being built.
  . start: only add digits in range [start..9]. 
  . current_sum: the sum of all numbers in 'current'.
- We need 'start' to avoid duplicates, because order doesn't matter in a combination.
  -> only combine in 1 direction (forward)
- Only keep exploring a path if current_sum < n.
- When len(current) == k:
  . If current_sum == n, add 'current' to result.
  . Otherwise, go back and try other options.
"""


def combinations_with_target_sum_3(k: int, n: int) -> list[list[int]]:
    answer: list[list[int]] = []

    def backtrack(current: list[int], start: int, current_sum: int):
        if len(current) == k and current_sum == n:
            # Clone since we mutate 'current' across 'backtrack' calls
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


"""
Complexity:

1. Time complexity: O(k * 9Ck)
- . Clone 'current' for each valid combinations: O(k)
  . Number of valid combinations <= Number of combinations = 9Ck
  -> work: O(k * 9Ck) 
- Number of tree nodes:
  . level 0: 1 root node
  . level 1: single digit -> 9C1 = 9 nodes
  . level 2: 2 digits (increasing order) -> 9C2 nodes
  . ...
  . level k: valid combination -> 9Ck nodes 
  -> loop work: O(sum(9Ci for i in [0..k])) = O(9Ck)
     . O(k * 9Ck) if being lax, but that doesn't change complexity
=> Total work: O(k * 9Ck + 9Ck) = O(k * 9Ck)

2. Space complexity: O(k)
- recursion stack: O(k)
- current: O(k)
"""


# === Extra: Why sum(nCi for i in [0..k]) = O(nCk) ===
# (See notes in '(77).combinations')
