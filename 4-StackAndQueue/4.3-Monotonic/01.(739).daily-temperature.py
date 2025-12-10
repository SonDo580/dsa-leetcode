"""
https://leetcode.com/problems/daily-temperatures/

Given an array of integers 'temperatures' that represents the daily temperatures,
return an array answer such that answer[i] is the number of days
you have to wait after the ith day to get a warmer temperature.
If there is no future day that is warmer, have answer[i] = 0 instead.
"""

"""
Brute-force approach: O(n^2)
- For each day, scan forward until we find a warmer day.

Improvement:
- Use a stack to store indices (days).
- For each day:
  + Keep popping days with lower temperature off the stack
    and record the time difference.
  + Push the current day to the stack.
- Stack properties:
  . only hold days whose warmer day haven't been found.
  . temperatures associated with the days are non-increasing.
"""


def daily_temperature(temperatures: list[int]) -> list[int]:
    # Use a stack to store indices (days)
    stack: list[int] = []

    # Initialize the answers:
    # answers[i] = 0 if there's no future warmer day
    n = len(temperatures)
    answers: list[int] = [0] * n

    for i in range(n):
        # Check if current day is warmer than the last day on the stack
        while len(stack) > 0 and temperatures[stack[-1]] < temperatures[i]:
            # Pop the day off the stack
            j = stack.pop()

            # Calculate the time difference
            answers[j] = i - j

        stack.append(i)

    return answers

"""
Complexity:
- Let n = len(temperatures)

1. Time complexity:
- Init 'answers': O(n)
- Iterate through 'temperatures': O(n)
  . although there's a nested 'while' loop, each item can only be removed at most once.
=> Overall: O(n)

2. Space complexity: O(n) for the stack
"""