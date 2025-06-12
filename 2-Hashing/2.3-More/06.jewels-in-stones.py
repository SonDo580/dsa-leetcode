# You're given strings jewels representing the types of stones that are jewels,
# and stones representing the stones you have.
# Each character in stones is a type of stone you have.
# You want to know how many of the stones you have are also jewels.

# Letters are case sensitive, so "a" is considered a different type of stone from "A".

# Example 1:
# Input: jewels = "aA", stones = "aAAbbbb"
# Output: 3

# Example 2:
# Input: jewels = "z", stones = "ZZ"
# Output: 0

# Constraints:
# 1 <= jewels.length, stones.length <= 50
# jewels and stones consist of only English letters.
# All the characters of jewels are unique.


# ===== Strategy =====
# - Use a set to store the jewels
# - Loop through stones and check if an item is in the set


def num_jewels_in_stones(jewels: str, stones: str) -> int:
    jewel_set = set(jewels)
    count = 0
    for stone in stones:
        if stone in jewel_set:
            count += 1
    return count


# ===== Complexity =====
# Let n = jewels.length, m = stones.length
#
# 1. Time complexity
# - Build jewel set: O(n)
# - Loop through stones: O(m)
# => Overall: O(n + m)
#
# 2. Space complexity: O(n) - for jewel set
