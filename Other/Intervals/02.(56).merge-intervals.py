"""
https://leetcode.com/problems/merge-intervals/description/

Given an array of intervals where intervals[i] = [start, end],
merge all overlapping intervals,
and return an array of the non-overlapping intervals that cover all the intervals in the input.

For example, given intervals = [[1, 3], [2, 6], [8, 10], [15, 18]],
return [[[1, 6], [8, 10], [15, 18]]].
The first two intervals merge to form [1, 6],
and then the next two intervals have no overlap.
"""

"""
Idea:
- Sort the intervals by start time
- Check overlap between adjacent intervals: start_i <= end_(i-1)
  (interval i-1 might be a merged interval)
- If overlap, merged interval = [start_(i-1), max(end_(i-1), end_i)]
  (start_(i-1) always <= start_i since 'intervals' is sorted)
"""


class Solution:
    def merge(self, intervals: list[list[int]]) -> list[list[int]]:
        intervals.sort()
        merged: list[list[int]] = []

        for start, end in intervals:
            if len(merged) > 0 and merged[-1][1] >= start:
                merged[-1][1] = max(merged[-1][1], end)
            else:
                merged.append([start, end])

        return merged


"""
Complexity:

1. Time complexity: O(n*log(n))
- sort 'intervals': O(n*log(n))
- iterate through 'intervals': O(n)

2. Space complexity: O(n) for sorting 'intervals' (timsort)
"""
