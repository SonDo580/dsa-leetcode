# You are given an integer array matches where matches[i] = [winneri, loseri] 
# indicates that the player winneri defeated player loseri in a match.
# 
# Return a list answer of size 2 where:
# answer[0] is a list of all players that have not lost any matches.
# answer[1] is a list of all players that have lost exactly one match.
# 
# The values in the two lists should be returned in increasing order.
# Note:
# You should only consider the players that have played at least one match.
# The testcases will be generated such that no two matches will have the same outcome.
 
# Example 1:
# Input: matches = [[1,3],[2,3],[3,6],[5,6],[5,7],[4,5],[4,8],[4,9],[10,4],[10,9]]
# Output: [[1,2,10],[4,5,7,8]]
# Explanation:
# Players 1, 2, and 10 have not lost any matches.
# Players 4, 5, 7, and 8 each have lost one match.
# Players 3, 6, and 9 each have lost two matches.
# Thus, answer[0] = [1,2,10] and answer[1] = [4,5,7,8].

# Example 2:
# Input: matches = [[2,3],[1,3],[5,4],[6,4]]
# Output: [[1,2,5,6],[]]
# Explanation:
# Players 1, 2, 5, and 6 have not lost any matches.
# Players 3 and 4 each have lost two matches.
# Thus, answer[0] = [1,2,5,6] and answer[1] = [].

# Constraints:
# 1 <= matches.length <= 10^5
# matches[i].length == 2
# 1 <= winner_i, loser_i <= 10^5
# winner_i != loser_i
# All matches[i] are unique.

def find_winners(matches: list[list[int]]) -> list[list[int]]:
    lost_count: dict[int, int] = {}

    for winner, loser in matches:
        if winner not in lost_count:
            lost_count[winner] = 0
        
        if loser not in lost_count:
            lost_count[loser] = 0
        lost_count[loser] += 1


    no_lost: list[int] = []
    one_lost: list[int] = []
    for player, lost in lost_count.items():
        if lost == 0:
            no_lost.append(player)
        elif lost == 1:
            one_lost.append(player)

    return [sorted(no_lost), sorted(one_lost)]

# ===== Complexity =====
# 1. Time complexity
# - Iterate over matches: O(n)
# - Iterate over lost_count: O(n)
# - Sorting the 2 result arrays: O(n*log(n))
# => Overall: O(n*log(n))
# 
# 2. Space complexity
# - hashmap: O(n)
# - 2 result arrays: O(n)
# => Overall: O(n)