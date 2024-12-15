# Implement the RecentCounter class.
# It should support ping(int t), which records a call at time t,
# and then returns an integer representing the number of calls
# that have happened in the range [t - 3000, t].
# Calls to ping will have increasing t.

from collections import deque


class RecentCounter:
    def __init__(self):
        # store timestamps in the range [t - 3000, t]
        self.queue = deque()

    def ping(self, t: int) -> int:
        # remove timestamps older than t - 3000
        while len(self.queue) > 0 and self.queue[0] < t - 3000:
            self.queue.popleft()

        # add current timestamp
        self.queue.append(t)

        # return the number of timestamps in the range [t - 3000, t]
        return len(self.queue)
