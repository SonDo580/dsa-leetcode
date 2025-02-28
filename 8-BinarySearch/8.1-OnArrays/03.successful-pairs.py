# You are given two positive integer arrays spells and potions,
# where spells[i] represents the strength of the ith spell
# and potions[j] represents the strength of the jth potion.
# You are also given an integer 'success'.
# A spell and potion pair is considered successful
# if the product of their strengths is at least 'success'.
# For each spell, find how many potions it can pair with to be successful.
# Return an integer array where the ith element
# is the answer for the ith spell.

# ===== Analyze =====
# Let n = spells.length and m = potions.length
#
# 1. Brute-force approach
# - Iterate over all pairs and check which ones have a product greater than success
# -> O(m*n)
#
# 2. Use binary search
# - If a spell has strength x, it will form a successful pair with any potion
#   that has strength 'success / x'
# - If potions is sorted, we can perform a binary search to find the insertion point
# - All the potions from that point can form a successful pair with the current spell
#   -> count = m - i

def successful_pairs(spells: list[int], potions: list[int], success: int) -> list[int]:
    def find_insertion_point(arr, target):
        left = 0
        right = len(arr) - 1

        while left <= right:
            mid = (left + right) // 2

            if arr[mid] == target:
                return mid

            if arr[mid] > target:
                right = mid - 1
            else:
                left = mid + 1

        return left

    potions.sort()
    answers = []
    m = len(potions)

    for spell in spells:
        i = find_insertion_point(potions, success / spell)
        answers.append(m - i)

    return answers


# ===== Complexity =====
#
# Time complexity:
# - Sort potions: O(m*log(m))
# - Iterate through spells: O(n*log(m))
#   (In each iteration, perform a binary search through sorted potions)
# => Overall: O((m + n) * log(m))
#
# Space complexity:
# - Answer list: O(n)
# - Sorting (depends on the algorithm): O(1) or O(m)
# => Overall: O(m + n)
