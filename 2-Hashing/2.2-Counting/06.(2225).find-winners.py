"""
https://leetcode.com/problems/find-players-with-zero-or-one-losses/

You are given an integer array 'matches' where matches[i] = [winneri, loseri]
indicates that the player winneri defeated player loseri in a match.

Return a list answer of size 2 where:
answer[0] is a list of all players that have not lost any matches.
answer[1] is a list of all players that have lost exactly one match.

The values in the two lists should be returned in increasing order.

Note:
- You should only consider the players that have played at least one match.
- The testcases will be generated such that no two matches will have the same outcome.
"""

"""
Idea:
- Use a dict to count number of lost matches of each player.
- Iterate through all matches:
  . winner not in dict -> lost_count = 0
  . loser -> increment lost_count
- Iterate through lost_count dict to collection players with 0/1 lost.
- Sort the results.
"""


def find_winners(matches: list[list[int]]) -> list[list[int]]:
    lost_count: dict[int, int] = {}

    for winner, loser in matches:
        if winner not in lost_count:
            lost_count[winner] = 0

        if loser not in lost_count:
            lost_count[loser] = 0
        lost_count[loser] += 1

    ans: list[list[int]] = [[], []]
    for player, lost in lost_count.items():
        if lost == 0:
            ans[0].append(player)
        elif lost == 1:
            ans[1].append(player)

    ans[0].sort()
    ans[1].sort()
    return ans


"""
Complexity:
- Let n = len(matches)

1. Time complexity:
- iterate over 'matches': O(n)
- iterate over 'lost_count': O(n)
- sort result arrays: O(n*log(n))
=> Overall: O(n*log(n))

2. Space complexity:
- O(n) for 'lost_count' dict
- sort result arrays: O(n) (timsort)
=> Overall: O(n)
"""
