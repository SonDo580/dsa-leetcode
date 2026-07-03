"""
https://leetcode.com/problems/matchsticks-to-square/

You are given an integer array 'matchsticks'
where matchsticks[i] is the length of the ith matchstick.
You want to use all the matchsticks to make one square.
You should not break any stick, but you can link them up,
and each matchstick must be used exactly one time.

Return true if you can make this square and false otherwise.
"""

"""
Idea:
- Use backtracking: 
  . For each matchstick, try putting it to each side of the square.
  . At the end, return True if all 4 sides have equal length.
- If sum(matchsticks) % 4 != 0
  -> cannot split equally to 4 sides without breaking matchsticks. 
  -> return False.
- We can calculate side length in advance: 
  . side_length = sum(matchsticks) // 4   (if sum(matchsticks) % 4 == 0)
  -> Only put a matchstick to 1 side if new_side_length <= side_length
- If any matchstick is longer than side length
  -> return False.
  -> sort 'matchsticks' in descending order and check the longest one.
- Sorting also helps when putting stick to a side:
  . If current_length + shortest_matchstick > side_length
    (only check when current_length < side_length)
    -> cannot put current matchstick on that side
       since even the shortest matchstick doesn't fit.
"""


def make_square(matchsticks: list[int]) -> bool:
    n = len(matchsticks)
    total_len = sum(matchsticks)
    if total_len % 4 != 0:
        return False

    side_len = total_len // 4
    matchsticks.sort(key=lambda x: -x)  # descending
    if matchsticks[0] > side_len:
        return False

    current_lens = [0] * 4  # current length of each side
    ans: bool = False

    def choose_side(i: int) -> None:
        """Choose square side for the ith matchstick."""
        nonlocal ans
        if ans:  # already found 1 valid solution
            return

        if i == n:
            if all(x == side_len for x in current_lens):
                ans = True
            return

        for j in range(4):
            # current side full
            if current_lens[j] == side_len:
                continue

            # even the shortest matchstick doesn't fit remaining space
            if current_lens[j] + matchsticks[-1] > side_len:
                continue

            if current_lens[j] + matchsticks[i] <= side_len:
                current_lens[j] += matchsticks[i]
                choose_side(i + 1)
                current_lens[j] -= matchsticks[i]  # backtrack
                if ans:  # already found 1 valid solution
                    return

    choose_side(0)
    return ans


"""
Complexity:
- Let n = len(matchsticks)

1. Time complexity: O(4^n)
- recursion depth: O(n)
- each 'choose_side' call spans 4 more calls

2. Space complexity: O(n)
- sort 'matchsticks': O(n) (timsort)
- recursion stack: O(n) * O(1) = O(n)
"""
