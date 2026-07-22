"""
https://leetcode.com/problems/brightest-position-on-street/

A perfectly straight street is represented by a number line.
The street has street lamp(s) on it and is represented by a 2D integer array 'lights'.
Each lights[i] = [positioni, rangei] indicates that there is a street lamp at position positioni
that lights up the area from [positioni - rangei, positioni + rangei] (inclusive).

The brightness of a position p is defined as the number of street lamp that light up the position p.

Given 'lights', return the brightest position on the street.
If there are multiple brightest positions, return the smallest one.
"""

# === Approach 1: Hashmap + Sorting ===
"""
- Iterate through 'lights' to record change in brightness at transition points
  (boundaries of light range) in a dictionary:
  . enter light range at (position-radius) -> increase brightness by 1.
  . leave light range at (position+radius + 1) -> decrease brightness by 1.
    (position+radius is included -> decrease brightness at next point)
- Iterate through sorted transition points and accumulate brightness.
  . Update max brightness and answer if brightness > current max 
    (prioritize smaller point, encountered before).
  . Brightness is applied to a range, not just 1 point.
    The smallest point is the transition point.
"""

from collections import defaultdict


class Solution:
    def brightestPosition(self, lights: list[list[int]]) -> int:
        # record brightness change at light range boundaries
        change: defaultdict[int, int] = defaultdict(int)
        for position, radius in lights:
            change[position - radius] += 1  # enter light range
            change[position + radius + 1] -= 1  # leave light range

        brightness = max_brightness = 0
        brightest_pos = None

        for point in sorted(change.keys()):
            brightness += change[point]
            if brightness > max_brightness:
                max_brightness = brightness
                brightest_pos = point

        assert brightest_pos is not None
        return brightest_pos


"""
Complexity:
- Let n = len(lights)

1. Time complexity: O(n*log(n))
- build 'change' dict: O(n)
- sort positions: O(n*log(n))
- find answer: O(n)

2. Space complexity: O(n)
- 'change' dict: O(n)
- sorted positions: O(n)
"""


# === Approach 2: Array + Sorting ===
class Solution:
    def brightestPosition(self, lights: list[list[int]]) -> int:
        # record brightness change at light range boundaries
        changes: list[tuple[int, int]] = []
        for position, radius in lights:
            changes.append((position - radius, 1))
            changes.append((position + radius + 1, -1))

        changes.sort()

        brightness = max_brightness = 0
        brightest_pos = None

        for point, change in changes:
            brightness += change
            if brightness > max_brightness:
                max_brightness = brightness
                brightest_pos = point

        assert brightest_pos is not None
        return brightest_pos


"""
Complexity:
- Let n = len(lights)

1. Time complexity: O(n*log(n))
- build 'changes' array: O(n)
- sort 'changes' array: O(n*log(n))
- find answer: O(n)

2. Space complexity: O(n) for 'changes' array
"""
