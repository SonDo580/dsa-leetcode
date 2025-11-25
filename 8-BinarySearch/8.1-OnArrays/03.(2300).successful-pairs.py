"""
https://leetcode.com/problems/successful-pairs-of-spells-and-potions

You are given two positive integer arrays 'spells' and 'potions',
where spells[i] represents the strength of the ith spell
and potions[j] represents the strength of the jth potion.

You are also given an integer 'success'.

A spell and potion pair is considered successful
if the product of their strengths is at least 'success'.

For each spell, find how many potions it can pair with to be successful.

Return an integer array where the ith element is the answer for the ith spell.
"""

"""
Analysis:
- Let n = spells.length and m = potions.length

1. Brute-force approach
- Iterate over all pairs and check which ones have a product greater than 'success'
  -> Time complexity: O(m*n)

2. Use binary search
- If a spell has strength x, it will form a successful pair with any potion
  that has strength of at least 'success / x'
- If potions is sorted, we can perform a binary search to find the insertion point
- All the potions from that point can form a successful pair with the current spell
  -> count = m - i
"""


def successful_pairs(spells: list[int], potions: list[int], success: int) -> list[int]:
    def find_insertion_point(arr: list[int], target: int) -> int:
        """
        Find position to insert 'target' in ascending array 'arr'.
        Return the left most possible position.
        """
        left = 0
        right = len(arr) - 1

        while left <= right:
            mid = (left + right) // 2
            if arr[mid] >= target:
                right = mid - 1  # find "better" result on the left portion
            else:
                left = mid + 1  # find result on the right portion

        return left

    potions.sort()
    answers: list[int] = []
    m = len(potions)

    for spell in spells:
        i = find_insertion_point(potions, success / spell)
        answers.append(m - i)  # number of potions with strength >= success / spell

    return answers


"""
Complexity:

1. Time complexity:
- Sort 'potions': O(m * log(m))
- Iterate through 'spells': n iterations
  + Perform binary search on 'potions' in each iteration: O(log(m)) 
=> Overall: O((m + n) * log(m))

2. Space complexity:
- Sort 'potions' (depends on the algorithm): Python's timsort takes O(m)
=> Overall: O(m)
"""
