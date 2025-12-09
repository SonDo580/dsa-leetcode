"""
https://leetcode.com/problems/number-of-recent-calls/

Implement the RecentCounter class.
It should support ping(int t), which records a call at time t,
and then returns an integer representing the number of calls
that have happened in the range [t - 3000, t].
Calls to ping will have increasing t.
"""

"""
Analysis:
- The brute-force method would be to put all values in an array,
  and iterate over the array each time to count how many values are within 3000.
  -> inefficient since we have to scan outdated values.
- We should get rid of a value as soon as it is outdated.
  -> use a queue.
"""

from collections import deque


class RecentCounter:
    def __init__(self):
        # Store timestamps in the range [t - 3000, t]
        self.queue: deque[int] = deque()

    def ping(self, t: int) -> int:
        # Remove timestamps older than t - 3000
        while len(self.queue) > 0 and self.queue[0] < t - 3000:
            self.queue.popleft()

        # Add current timestamp
        self.queue.append(t)

        # Return the number of timestamps in the range [t - 3000, t]
        return len(self.queue)


"""
Complexity:
- Let n be the number of 'ping' calls.

1. Time complexity:
- 'ping' (arbitrary): O(n) if we have to remove all previous timestamps.
- 'ping' (on average): O(1) since each item is added/removed at most once.

2. Space complexity: O(n) for the queue. 
"""
