"""
https://leetcode.com/problems/meeting-rooms/

Given an array of meeting times 'intervals' where intervals[i] = [start, end]
indicates the ith meeting runs from [start, end),
determine if one person could attend all meetings.

For example, given intervals = [[0, 30], [5, 10], [15, 20]], return false.
If you attend the [0, 30] meeting, then you cannot attend the other two.
"""

# === Brute-force ===
"""
- Look at every pair of intervals to check overlap.
"""


class Solution:
    def canAttendMeetings(self, intervals: list[list[int]]) -> bool:
        n = len(intervals)
        for i in range(n - 1):
            start_i, end_i = intervals[i]
            for j in range(i + 1, n):
                start_j, end_j = intervals[j]
                # meeting ending at time t and meeting starting at time t do not overlap
                if start_j < end_i <= end_j or start_i < end_j <= end_i:
                    return False
        return True


"""
Complexity:
1. Time complexity: O(n^2)
2. Space complexity: O(1)
"""

# === Improvement ===
"""
- Sort the intervals by start time and check overlap 
  between adjacent meetings.
"""


class Solution:
    def canAttendMeetings(self, intervals: list[list[int]]) -> bool:
        intervals.sort()
        for i in range(1, len(intervals)):
            if intervals[i][0] < intervals[i - 1][1]:  # start_i < end_(i-1)
                return False
        return True


"""
Complexity:

1. Time complexity: O(n*log(n))
- sort 'intervals': O(n*log(n))
- iterate through 'intervals': O(n)

2. Space complexity: O(n) for sorting 'intervals' (timsort)
"""
