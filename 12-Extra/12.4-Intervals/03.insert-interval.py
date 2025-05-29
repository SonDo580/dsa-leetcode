# You are given an array of non-overlapping intervals intervals where intervals[i] = [starti, endi]
# represent the start and the end of the ith interval and intervals is sorted in ascending order by starti.
# You are also given an interval newInterval = [start, end] that represents the start and end of another interval.
#
# Insert newInterval into intervals such that intervals is still sorted in ascending order by starti
# and intervals still does not have any overlapping intervals (merge overlapping intervals if necessary).
#
# Return intervals after the insertion.
# Note that you don't need to modify intervals in-place.
# You can make a new array and return it.

# Example 1:
# Input: intervals = [[1,3],[6,9]], newInterval = [2,5]
# Output: [[1,5],[6,9]]

# Example 2:
# Input: intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]], newInterval = [4,8]
# Output: [[1,2],[3,10],[12,16]]
# Explanation: Because the new interval [4,8] overlaps with [3,5],[6,7],[8,10].

# Constraints:
# 0 <= intervals.length <= 10^4
# intervals[i].length == 2
# 0 <= starti <= endi <= 10^5
# intervals is sorted by starti in ascending order.
# newInterval.length == 2
# 0 <= start <= end <= 10^5

# ===== Implementation =====
# - Use a separate array to store result
# - Add all intervals before new interval (no overlap)
# - Merge intervals that overlap with new interval and add to result
# - Add all remaining intervals


def insert_interval(
    sorted_intervals: list[list[int]], new_interval: list[int]
) -> list[list[int]]:
    inserted = []
    n = len(sorted_intervals)

    # Add all intervals that end before the new interval starts
    i = 0
    while i < n and sorted_intervals[i][1] < new_interval[0]:
        inserted.append(sorted_intervals[i])
        i += 1

    # Merge intervals that overlap with new interval (if any)
    # - After the last loop, any remaining interval has end >= new_start
    # - We only need to check if the interval has start <= new_end
    while i < n and sorted_intervals[i][0] <= new_interval[1]:
        new_interval[0] = min(new_interval[0], sorted_intervals[i][0])
        new_interval[1] = max(new_interval[1], sorted_intervals[i][1])
        i += 1

    # Add (merged) new interval
    inserted.append(new_interval)

    # Add all remaining intervals
    while i < n:
        inserted.append(sorted_intervals[i])
        i += 1

    return inserted

# ===== Complexity =====
# Time complexity: O(n)
# Space complexity: O(n)