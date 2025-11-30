"""
https://leetcode.com/problems/random-pick-with-weight

You are given a 0-indexed array of positive integers w
where w[i] describes the weight of the ith index.

You need to implement the function pickIndex(),
which randomly picks an index in the range [0, w.length - 1] (inclusive) and returns it.
The probability of picking an index i is w[i] / sum(w).

For example, if w = [1, 3], the probability of picking index 0 is 1 / (1 + 3) = 0.25 (i.e., 25%),
and the probability of picking index 1 is 3 / (1 + 3) = 0.75 (i.e., 75%).
"""

"""
Idea:
- 1 solution is to create a separate list that duplicates items
  based on their weights, then pick randomly from that list.
  -> exceed memory limit if the weights are very big.
- Imagine there are sticks with lengths of weights.
  If we put the sticks sequentially in a straight line,
  then randomly pick 1 point on that line,
  the probability that we land on stick i is
  length_i / total_length = weight_i / total_weight
- To decide whether we land on stick i, check if the random value
  is between total_length_upto_i and (total_length_upto_i + length_i)
  -> use prefix sum array
- The weights are positive.
  -> prefix sum array is strictly increasing
  -> use binary search to find the segment
- To avoid overlapping, pick i if random_value is in [prefix[i-1]; prefix[i])
  -> use bisect right / upper bound operation to find prefix[i]
"""

import random
import bisect


class Solution:

    def __init__(self, w: list[int]):
        self.weights = w
        self.prefix_sum = self.__build_prefix_sum()

    def __build_prefix_sum(self) -> list[int]:
        prefix_sum: list[int] = []
        current_sum = 0
        for weight in self.weights:
            current_sum += weight
            prefix_sum.append(current_sum)
        return prefix_sum

    def __get_random_value(self) -> int:
        """
        Pick a random integer in [0, prefix_sum[-1]).
        Exclude prefix_sum[-1] so the max upper bound is prefix_sum[-1]
        """
        return random.randrange(0, self.prefix_sum[-1])

    def pickIndex(self) -> int:
        value = self.__get_random_value()
        return bisect.bisect_right(self.prefix_sum, value)


"""
Complexity:

1. Time complexity:
- __init__: O(n) to build prefix_sum
- pickIndex: O(log(n)) for bisect right

2. Space Complexity: O(n) for prefix_sum
"""
