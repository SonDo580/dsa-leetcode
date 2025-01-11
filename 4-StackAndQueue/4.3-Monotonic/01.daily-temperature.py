# Given an array of integers temperatures that represents the daily temperatures,
# return an array answer such that answer[i] is the number of days
# you have to wait after the ith day to get a warmer temperature.
# If there is no future day that is warmer, have answer[i] = 0 instead.

# ===== Analyze =====
# Brute-force approach: O(n^2)
# - iterate over the input.
# - for each temperature, iterate through the rest of the array
#   until we find a warmer temperature.

# ===== Improvement =====
# - Push the indices (day) onto a stack
# - The temperatures associated with the days on the stack must always be decreasing
# - When encountering a day with warmer temperature than the last day on the stack:
#   + pop that day off the stack and calculate the time difference
#   + repeat with the remaining days on the stack

# Note: the stack is monotonically non-increasing

from typing import List


def daily_temperature(temperatures: List[int]) -> List[int]:
    # Use a stack to store the day indices
    stack: List[int] = []

    # Initialize the answers:
    # answers[i] = 0 if there's no future that is warmer
    answers = [0] * len(temperatures)

    for i in range(len(temperatures)):
        # Check if encounter a day with warmer temperature than the last day on the stack
        while len(stack) > 0 and temperatures[stack[-1]] < temperatures[i]:
            # Pop the day off the stack
            j = stack.pop()

            # Calculate the time difference
            answers[j] = i - j

        stack.append(i)

    return answers
