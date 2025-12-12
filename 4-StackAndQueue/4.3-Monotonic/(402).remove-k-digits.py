"""
https://leetcode.com/problems/remove-k-digits/

Given string 'num' representing a non-negative integer, and an integer k,
return the smallest possible integer after removing k digits from 'num'.
"""

"""
Idea:
- To generate the minimum number by removing digits:
  If we encounter a digit b that is less than the digit a before it,
  then we should remove a (b is shifted left to the position of a).

=> Algorithm:
- Loop through the digits from left to right, and push them to a stack.
  Before pushing, pop any digits that are greater than current digit.
  Leading 0's is not allowed, so only push 0 if the stack is not empty. 
- Repeat until all digits are processed, or k digits have been removed.
- If k remains, pop the top remaining_k digits off the stack,
  which are the largest digits.
- Concatenate all digits on the stack to build the result. 
  If the stack is empty, return "0".  
- Note: the stack is monotonically non-decreasing.
  
- Implementation notes:
  + compare digit characters directly, don't need to convert to number
    (the character codes are already sorted).
"""


def remove_k_digits(num: str, k: int) -> str:
    stack: list[str] = []

    for digit in num:
        while stack and stack[-1] > digit and k > 0:
            stack.pop()
            k -= 1

        if digit == "0" and not stack:
            continue
        stack.append(digit)

    while k > 0 and stack:
        stack.pop()
        k -= 1

    return "".join(stack) if stack else "0"


"""
Complexity:
- Let n = len(num)

1. Time complexity:
- Stack pushes: O(n)
  Stack pops: O(k)
- Build result: O(n)
=> Overall: O(n + k)

2. Space Complexity: O(n) for the stack
"""
