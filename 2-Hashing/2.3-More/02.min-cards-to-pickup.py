# You are given an integer array cards where cards[i] represents the value of the ith card.
# A pair of cards are matching if the cards have the same value.

# Return the minimum number of consecutive cards you have to pick up
# to have a pair of matching cards among the picked cards.
# If it is impossible to have matching cards, return -1.

# Example 1:
# Input: cards = [3,4,2,3,4,7]
# Output: 4
# Explanation: We can pick up the cards [3,4,2,3] which contain a matching pair of cards with value 3. Note that picking up the cards [4,2,3,4] is also optimal.

# Example 2:
# Input: cards = [1,0,5,3]
# Output: -1
# Explanation: There is no way to pick up a set of consecutive cards that contain a pair of matching cards.

# Constraints:
# 1 <= cards.length <= 10^5
# 0 <= cards[i] <= 10^6

# ===== Analyze =====
# - The minimum number of consecutive cards to have a pair of matching cards.
# <=> The shortest distance between any of the same element (include both ends).

# ===== Strategy =====
# - Iterate over array and record the indices for every value
# - Iterate over those indices (values of the hash map) to find the shortest distance.

from collections import defaultdict


def min_cards_to_pickup(cards: list[int]) -> int:
    indices_dict: defaultdict[int, list[int]] = defaultdict(list)
    for i in range(len(cards)):
        indices_dict[cards[i]].append(i)

    min_distance = float("inf")
    for indices in indices_dict.values():
        for i in range(len(indices) - 1):
            min_distance = min(min_distance, indices[i + 1] - indices[i] + 1)

    return min_distance if min_distance < float("inf") else -1


# ===== Complexity =====
# 1. Time complexity:
# - Looping through cards to build indices_dict: O(n)
# - Looping through values of indices_dict: O(n)
# => Overall: O(n)
#
# 2. Space complexity: O(n) - for indices_dict


# ===== Improvement =====
# - Track the last seen index of each value.
# - When encounter a duplicate, calculate the window length.
# => - Just need 1 pass to find the min window length.
#    - Only store the last index instead of all indices for each value.


def min_cards_to_pickup(cards: list[int]) -> int:
    last_index_dict: dict[int, int] = {}
    min_distance = float("inf")

    for i in range(len(cards)):
        if cards[i] in last_index_dict:
            min_distance = min(min_distance, i - last_index_dict[cards[i]] + 1)
        last_index_dict[cards[i]] = i

    return min_distance if min_distance < float("inf") else -1


# ===== Complexity =====
# 1. Time complexity:
# - Still O(n). But only need 1 loop.
#
# 2. Space complexity:
# - Still O(n) (worst case when there's no duplicates). 
#   But better on average.