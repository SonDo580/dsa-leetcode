# Given a string containing digits from 2-9 inclusive,
# return all possible letter combinations that the number could represent.
# Return the answer in any order.

# A mapping of digits to letters (just like on the telephone buttons) is given below.
# Note that 1 does not map to any letters.
# ------------------------------
# | 1()     | 2(abc) | 3(def)  |
# | 4(ghi)  | 5(jkl) | 6(mno)  |
# | 7(pqrs) | 8(tuv) | 9(wxyz) |
# ------------------------------

# Example 1:
# Input: digits = "23"
# Output: ["ad","ae","af","bd","be","bf","cd","ce","cf"]

# Example 2:
# Input: digits = ""
# Output: []

# Example 3:
# Input: digits = "2"
# Output: ["a","b","c"]

# Constraints:
# 0 <= digits.length <= 4
# digits[i] is a digit in the range ['2', '9'].


# ===== Strategy =====
# - Use backtracking to generate all possible letter combinations
# - For each digit, explore all possible letters that it represents.
#   For each of those, explore all possible letters that the next digit represents.
#   And so on.
# -> Use a function backtrack(current) to build each letter combination:
#    . current is the string being built.
#    . i = len(current) represents the ith digit in 'digits' that we should check next.
# - A valid solution is found when we "consume" all 'digits'.
# - Implementation note: create a mapping from digits to letters it represents
#   (use an array or hashmap)


def letter_combinations(digits: str) -> list[str]:
    if len(digits) == 0:
        return []

    digit_to_letters: list[str] = [
        "",
        "",
        "abc",
        "def",
        "ghi",
        "jkl",
        "mno",
        "pqrs",
        "tuv",
        "wxyz",
    ]

    combinations: list[str] = []

    def backtrack(current: str):
        if len(current) == len(digits):
            combinations.append(current)
            return

        next_digit = digits[len(current)]
        for letter in digit_to_letters[int(next_digit)]:
            backtrack(current + letter)

    backtrack("")
    return combinations
