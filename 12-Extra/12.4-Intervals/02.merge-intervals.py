# Given an array of intervals where intervals[i] = [start, end],
# merge all overlapping intervals,
# and return an array of the non-overlapping intervals that cover all the intervals in the input.

# For example, given intervals = [[1, 3], [2, 6], [8, 10], [15, 18]],
# return [[[1, 6], [8, 10], [15, 18]]].
# The first two intervals merge to form [1, 6],
# and then the next two intervals have no overlap.

# ===== Implementation =====
# - Sort the meetings by their start time and check if there is overlap between any adjacent meetings.
#   (end time of meeting i >= start time of meeting i + 1)
# - Merge the overlapping intervals.
# - Or just push the current interval to result array.


def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    intervals.sort()
    merged = []

    for start, end in intervals:
        if len(merged) > 0 and merged[-1][1] >= start:
            merged[-1][1] = end
        else:
            merged.append([start, end])

    return merged

# ===== Complexity =====
# 
# 1. Time complexity:
# - sorting: O(n*log(n))
# - loop through: O(n)
# => Overall: O(n*log(n))
# 
# 2. Space complexity:
# - sorting: depends on the sorting algorithm (Python's timsort uses O(n) space)
# - 'merged' array: O(n)