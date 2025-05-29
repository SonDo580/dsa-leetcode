# Given an array of meeting times intervals where intervals[i] = [start, end] 
# indicates the ith meeting runs from [start, end), 
# determine if one person could attend all meetings.

# For example, given intervals = [[0, 30], [5, 10], [15, 20]], return false. 
# If you attend the [0, 30] meeting, then you cannot attend the other two.

# ===== Analyze =====
# - Brute-force approach: look at every pair of intervals and check
#   if there is overlap 
#   -> Time complexity: O(n^2)
# - Improvement: sort the meetings by their start time and check if 
#   there is overlap between any adjacent meetings.

def can_attend_meetings(intervals: list[list[int]]) -> bool:
    intervals.sort()
    for i in range(1, len(intervals)):
        if intervals[i][0] < intervals[i - 1][1]:
            return False
    return True

# ===== Complexity =====
# 1. Time complexity: 
# - sorting: O(n*log(n))
# - loop through: O(n)
# => Overall: O(n*log(n))
# 
# 2. Space complexity:
# - Depends on the sorting algorithm
#   (Python's timsort uses O(n) space)