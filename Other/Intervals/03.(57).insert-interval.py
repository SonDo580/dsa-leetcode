"""
https://leetcode.com/problems/insert-interval/

You are given an array of non-overlapping intervals 'intervals' 
where intervals[i] = [starti, endi] represent the start and the end 
of the ith interval and 'intervals' is sorted in ascending order by starti.
You are also given an interval newInterval = [start, end] that represents 
the start and end of another interval.

Insert newInterval into 'intervals' such that 'intervals' is 
still sorted in ascending order by starti and 'intervals' 
still does not have any overlapping intervals 
(merge overlapping intervals if necessary).

Return 'intervals' after the insertion.
Note that you don't need to modify intervals in-place.
You can make a new array and return it.
"""


"""
Idea:
- Use a separate array to store result.
- Add all intervals that end before new interval starts.
- Merge intervals that overlap with new interval and add to result.
- Add all remaining intervals.
"""

def insert_interval(
    intervals: list[list[int]], new_interval: list[int]
) -> list[list[int]]:
    n = len(intervals)
    inserted: list[list[int]] = []

    # Add all intervals that end before the new interval starts
    i = 0
    while i < n and intervals[i][1] < new_interval[0]:
        inserted.append(intervals[i])
        i += 1

    # Merge intervals that overlap with new interval
    # - After the previous loop, any remaining interval has end >= new_start
    #   -> Overlap if interval has start <= new_end
    while i < n and intervals[i][0] <= new_interval[1]:
        new_interval[0] = min(new_interval[0], intervals[i][0])
        new_interval[1] = max(new_interval[1], intervals[i][1])
        i += 1

    # Add (merged) new interval
    inserted.append(new_interval)

    # Add all remaining intervals
    while i < n:
        inserted.append(intervals[i])
        i += 1

    return inserted

"""
Complexity:
- Let n = len(intervals)
1. Time complexity: O(n)
2. Space complexity: O(n)
"""
