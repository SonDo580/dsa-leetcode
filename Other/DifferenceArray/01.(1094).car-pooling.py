"""
https://leetcode.com/problems/car-pooling/

There is a car with 'capacity' empty seats.
The vehicle only drives east (i.e., it cannot turn around and drive west).

You are given the integer 'capacity' and an array 'trips'
where trips[i] = [numPassengers_i, from_i, to_i] indicates that
the ith trip has numPassengers_i passengers and the locations
to pick them up and drop them off are from_i and to_i respectively.

The locations are given as the number of kilometers due east
from the car's initial location.

Return true if it is possible to pick up and drop off all passengers
for all the given trips, or false otherwise.
"""

# === Approach 1: Hashmap + Sorting ===
"""
- Iterate through 'trips' and record number of passengers
  pick-up/drop-off at each point.
  . Use a dictionary, value is change in number of passengers.
  . pick-up <-> change > 0 
    drop-off -> change < 0
- Sort pick-up/drop-off points in ascending order.
- Process the points in ascending order.
  . Initial number of passengers = 0.
  . Update number of passengers at each pick-up/drop-off point.
- Return False if number of passengers > capacity at any point.
"""

from collections import defaultdict


class Solution:
    def carPooling(self, trips: list[list[int]], capacity: int) -> bool:
        # change in passengers at each point
        change: defaultdict[int, int] = defaultdict(int)

        for num_passengers, from_point, to_point in trips:
            # 'num' passengers enter at 'from' and leave at 'to'
            change[from_point] += num_passengers
            change[to_point] -= num_passengers

        num_passengers_on_car = 0
        sorted_points = sorted(change.keys())
        for point in sorted_points:
            num_passengers_on_car += change[point]
            if num_passengers_on_car > capacity:
                return False

        return True


"""
Complexity:
- Let n = len(trips)
  -> Number of unique points: O(2*n) = O(n)

1. Time complexity: O(n*log(n))
- Iterate through 'trips': O(n)
- Sort the points: O(n*log(n))
- Iterate through sorted points: O(n)

2. Space complexity: O(n)
- 'change': O(n)
- 'sorted_points': O(n)
"""


# === Approach 2: Difference array ===
"""
- Find range of points = [0..max(to_point)].
- Init array 'changes' of size max(to_point)+1 to record
  changes in number of passengers at all points
  . Init all values to 0 (no changes).
  . Cons: need a large array when the range of points is large.
- Iterate through 'trips' and update change in number of passengers.
  . changes[from_i] += num_passengers (pick up)
  . changes[to_i] -= num_passengers (drop off)
- Iterate though 'changes' and update number of passengers on car
  . Initial number of passengers = 0.
- Return False if number of passengers > capacity at any point.
"""


class Solution:
    def carPooling(self, trips: list[list[int]], capacity: int) -> bool:
        furthest_point = max(trip[2] for trip in trips)  # max(to_i)

        # change in passengers at each point
        changes = [0] * (furthest_point + 1)

        for num_passengers, from_point, to_point in trips:
            # 'num' passengers enter at 'from' and leave at 'to'
            changes[from_point] += num_passengers
            changes[to_point] -= num_passengers

        num_passengers_on_car: int = 0
        for change in changes:
            num_passengers_on_car += change
            if num_passengers_on_car > capacity:
                return False

        return True


"""
Complexity
Let n = len(trips)
    m = furthest_point

1. Time complexity: O(n + m)
- Find furthest_point: O(n)
- Record change at enter/leave points: O(n)
- Iterate through 'changes': O(m)

2. Space complexity: O(m) for num_passengers_changes
"""
