"""
https://leetcode.com/problems/minimum-speed-to-arrive-on-time

You are given a floating-point number 'hour',
representing the amount of time you have to reach the office.
To commute to the office, you must take n trains in sequential order.
You are also given an integer array 'dist' of length n,
where dist[i] describes the distance (in kilometers) of the ith train ride.

Each train can only depart at an integer hour,
so you may need to wait in between each train ride.
For example, if the 1st train ride takes 1.5 hours,
you must wait for an additional 0.5 hours before
you can depart on the 2nd train ride at the 2 hour mark.

Return the minimum positive integer speed (in kilometers per hour)
that all the trains must travel at for you to reach the office on time,
or -1 if it is impossible to be on time.

Tests are generated such that the answer will not exceed 10^7
and hour will have at most two digits after the decimal point.
"""

"""
Analysis:
- Let k be the speed of all the trains.
  If a train has distance d then the time is d / k.
  The trains only depart at integer hour, so we need to round the time up.
  The last ride doesn't need rounding because we don't need to wait for another train.

- We can perform a binary search for the speed k.
  + lower bound: 1 (k must be a positive integer)
  + upper bound: 10^7 (in problem constraints)
- If a speed k is possible, try to find a smaller k. 
  Otherwise try a larger k.

- Since each train ride takes at least 1 hour, 
  if there are more trains than hours allowed,
  it is impossible to find an answer.
  The last train can take fractional time (no more waiting),
  so we should compare number of trains with hours rounded up.
"""

import math


def min_train_speed(dist: list[int], hour: float) -> int:
    if len(dist) > math.ceil(hour):
        return -1

    def _is_valid(speed: int) -> bool:
        """Check if we can be on time if all trains travel at 'speed'."""
        time = 0
        for distance in dist:
            time = math.ceil(time)
            time += distance / speed
            # the last time is not rounded up
        return time <= hour

    left = 1
    right = 10**7

    while left <= right:
        mid = (left + right) // 2
        if _is_valid(mid):
            right = mid - 1  # search left portion for smaller speed
        else:
            left = mid + 1  # search right portion for valid speed

    return left


"""
Complexity:
Let n = dist.length; k = max train speed (10^7 in this case)

1. Time complexity:
- check valid speed: O(n)
- binary search: O(log(k))
=> Overall: O(n * log(k))

2. Space complexity: O(1)
"""
