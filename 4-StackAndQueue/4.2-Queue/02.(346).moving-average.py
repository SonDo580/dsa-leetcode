"""
https://leetcode.com/problems/moving-average-from-data-stream/

Given a stream of integers and a window size,
calculate the moving average of all integers in the sliding window.

Implement the MovingAverage class:
. MovingAverage(int size) Initializes the object with the size of the window size.
. double next(int val) Returns the moving average of the last size values of the stream.
"""

"""
Idea:
- Use a queue to store items in a window.
  . current size < max size -> append right.
  . current size == max size -> append right and pop left.
- Maintain the sum of the current window and update when adding/removing items.
"""

from collections import deque


class MovingAverage:
    def __init__(self, size: int):
        self.size = size  # max size
        self.queue = deque()  # current window
        self.current_sum = 0  # sum of current window

    def next(self, val: int) -> float:
        # Enqueue the new item
        self.queue.append(val)

        # Add new value to current sum
        self.current_sum += val

        # Dequeue if current size becomes greater than max size
        if len(self.queue) > self.size:
            removed_val = self.queue.popleft()

            # Subtract removed value from current sum
            self.current_sum -= removed_val

        # Return the current average
        return self.current_sum / len(self.queue)


"""
Complexity:

1. Time complexity:
- 'next': O(1)

2. Space complexity: O(n) for the queue.
"""
