"""
https://leetcode.com/problems/letter-combinations-of-a-phone-number/

Given a string containing digits from 2-9 inclusive,
return all possible letter combinations that the number could represent.
Return the answer in any order.

A mapping of digits to letters (just like on the telephone buttons) is given below.
Note that 1 does not map to any letters.
------------------------------
| 1()     | 2(abc) | 3(def)  |
| 4(ghi)  | 5(jkl) | 6(mno)  |
| 7(pqrs) | 8(tuv) | 9(wxyz) |
------------------------------
"""

"""
Idea:
- Use backtracking to find all letter combinations. States needed:
  . curr: the string being built.
  . i: the ith digit in 'digits' to check next.
    i = len(curr) -> don't need explicit variable.
- For each digit, explore all possible letters that it represents.
- A valid solution is found when we consume all 'digits'.
- To quickly check letters that a number can represent: 
  . Create a mapping from digits to letters it represents
    (use an array / hashmap)
- Python strings are immutable so doing 'curr + letter'
  creates a brand new strings every time.
  -> Use array of characters for 'curr'
"""


def letter_combinations(digits: str) -> list[str]:
    if len(digits) == 0:
        return []

    digit_to_letters: list[str] = [
        "",  # 0
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

    ans: list[str] = []

    def build(curr: list[str]) -> None:
        """Choose the letter the digits[i] represents, where i = len(curr)."""
        if len(curr) == len(digits):
            ans.append("".join(curr))
            return

        next_digit = digits[len(curr)]
        for letter in digit_to_letters[int(next_digit)]:
            curr.append(letter)
            build(curr)
            curr.pop()

    build(curr=[])
    return ans


"""
Complexity:
- Let n = len(digits)

1. Time complexity: O(n * 4^n)
- Clone 'curr' at the end of each path: O(n)
- Number of valid paths: O(4^n)
  . max number of characters a digit can represents: 4
=> Total work: O(n * 4^n)

2. Space complexity: O(n)
- recursion stack: O(n)
- 'curr': O(n)
- 'digit_to_letters': O(10) = O(1)
"""
