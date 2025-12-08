"""
https://leetcode.com/problems/remove-all-adjacent-duplicates-in-string/

You are given a string s. Continuously remove duplicates
(two of the same character beside each other) until you can't anymore.
Return the final string after this.

For example, given s = "abbaca", you can first remove the "bb" to get "aaca".
Next, you can remove the "aa" to get "ca". This is the final answer.
"""

"""
Analysis:
- If the current character is the same as the previous character,
  they can be deleted.
- Some adjacent duplicates are available after the deletions of in-between characters.

=> Idea:
- Keep adding characters to a stack.
- If current character is the same as the top of the stack,
  pop the top of the stack.
- Join the remaining characters in the end. 
"""


def remove_adjacent_duplicates(s: str) -> str:
    stack: list[str] = []

    for c in s:
        if len(stack) > 0 and stack[-1] == c:
            stack.pop()
        else:
            stack.append(c)

    return "".join(stack)


"""
Complexity:

1. Time complexity:
- iterate through s: n iterations
- stack push/pop: O(1) (amortized)
- join remaining characters: O(n)
=> Overall: O(n)

2. Space complexity: O(n) for the stack
"""
