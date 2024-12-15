# Given a stream of integers and a window size,
# calculate the moving average of all integers in the sliding window.
#
# Implement the MovingAverage class:
#
# MovingAverage(int size) Initializes the object with the size of the window size.
# double next(int val) Returns the moving average of the last size values of the stream.

# Example 1:
#
# Input
# ["MovingAverage", "next", "next", "next", "next"]
# [[3], [1], [10], [3], [5]]
# Output
# [null, 1.0, 5.5, 4.66667, 6.0]

# Explanation
# MovingAverage movingAverage = new MovingAverage(3);
# movingAverage.next(1); // return 1.0 = 1 / 1
# movingAverage.next(10); // return 5.5 = (1 + 10) / 2
# movingAverage.next(3); // return 4.66667 = (1 + 10 + 3) / 3
# movingAverage.next(5); // return 6.0 = (10 + 3 + 5) / 3

# Constraints:
# 1 <= size <= 1000
# -105 <= val <= 105
# At most 104 calls will be made to next.

from collections import deque


class MovingAverage:
    def __init__(self, size: int):
        self.size = size  # size of the window
        self.queue = deque()  # store the current window
        self.current_sum = 0  # sum of the current window

    def next(self, val: int) -> float:
        # enqueue the new item
        self.queue.append(val)

        # add new value to current sum
        self.current_sum += val

        # dequeue if the length of the queue becomes greater than window size
        if len(self.queue) > self.size:
            removed_val = self.queue.popleft()

            # subtract removed value from current sum
            self.current_sum -= removed_val

        # return the current average
        return self.current_sum / len(self.queue)
