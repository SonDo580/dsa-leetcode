"""
https://leetcode.com/problems/combination-sum/

Given an array of distinct positive integers 'candidates' and a target integer 'target',
return a list of all unique combinations of candidates where the chosen numbers sum to 'target'.
The same number may be chosen from candidates an unlimited number of times.
Two combinations are unique if the frequency of at least one of the chosen numbers is different.
"""

"""
Idea:
- Use backtracking to find all valid combinations. States needed:
  . current: the combination being built.
  . start: only choose numbers in candidates[start:].
  . current_sum: the sum of all numbers in 'current'.
- We need 'start' to avoid duplicates, 
  because order doesn't matter in a combination
  (never look back at elements we've already passed).
- We are allowed to use the same number multiple times.
  -> Try using the same number in the next backtrack call.
- Stop a path if adding to 'current_sum' makes it exceed 'target'.
  When 'current_sum' reaches 'target', add 'current' to result.
"""


def combinations_with_target_sum(candidates: list[int], target: int) -> list[list[int]]:
    answer: list[list[int]] = []

    def backtrack(current: list[int], start: int, current_sum: int):
        """Pick numbers from candidates[start:] to current."""
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
                backtrack(current, i, next_sum)  # try using the same number
                current.pop()

    backtrack(current=[], start=0, current_sum=0)
    return answer


"""
Complexity:
- Let n = len(candidates)
      min = min(candidates)
- Each backtrack call is a node in the recursion tree.
      
1. Time complexity:
- Recursion depth: O(target/min)
- Branching factor for each node: O(n)
=> Total nodes: O(branch_factor^recursion_depth) = O(n^(target/min))

- Clone a valid combination: O(L) = O(target/min)
=> Across nodes: O((target/min) * n^(target/min))
   (Cloning does not happen in every node, being lax here)

2. Space complexity: O(target/min)
- recursion stack: O(target/min)
- 'current': O(target/min)
"""

# === Alternative ===
"""
- Instead of generating unique combinations directly,
  generate arrays representing frequency of each candidate.
  Build result from frequencies.
- Example: 
  . candidates = [1, 2, 3]
  . frequencies = [0, 1, 0] 
    -> use 2 once, don't use 1 and 3
- Valid result:
  . len(frequencies) == n AND current_sum == target
"""


def combinations_with_target_sum(candidates: list[int], target: int) -> list[list[int]]:
    ans: list[list[int]] = []
    n = len(candidates)

    def choose_freq(i: int, frequencies: list[int], curr_sum: int) -> None:
        """Choose frequency for candidates[i] in current combination."""
        if i == n:
            if curr_sum == target:
                # Generate combination from candidate frequencies
                curr: list[int] = []
                for j in range(n):
                    curr.extend([candidates[j]] * frequencies[j])
                ans.append(curr)
            return

        # Try using this number as long as curr_sum doesn't exceed target
        for freq in range((target - curr_sum) // candidates[i] + 1):
            frequencies.append(freq)
            curr_sum += freq * candidates[i]
            choose_freq(i + 1, frequencies, curr_sum)
            curr_sum -= freq * candidates[i]
            frequencies.pop()

    choose_freq(i=0, frequencies=[], curr_sum=0)
    return ans


"""
Complexity:

1. Time complexity:
- Recursion depth: O(n)
- Branching factor for each node: O(target/min)
=> Total nodes: O(branch_factor^recursion_depth) = O((target/min)^n)

- Generate a valid combination: O(target/min)
=> Across nodes: O((target/min) * (target/min)^n) = O((target/min)^n)
   (Cloning does not happen in every node, being lax here)

2. Space complexity: O(n)
- recursion stack: O(n)
- 'frequencies': O(n)
"""
