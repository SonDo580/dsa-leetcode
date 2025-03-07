# There is a car with 'capacity' empty seats.
# The vehicle only drives east (i.e., it cannot turn around and drive west).

# You are given the integer 'capacity' and an array 'trips'
# where trips[i] = [numPassengers_i, from_i, to_i] indicates that
# the ith trip has numPassengers_i passengers and the locations
# to pick them up and drop them off are from_i and to_i respectively.
#
# The locations are given as the number of kilometers due east
# from the car's initial location.
#
# Return true if it is possible to pick up and drop off all passengers
# for all the given trips, or false otherwise.

# Example 1:
# Input: trips = [[2,1,5],[3,3,7]], capacity = 4
# Output: false

# Example 2:
# Input: trips = [[2,1,5],[3,3,7]], capacity = 5
# Output: true

# Constraints:
# 1 <= trips.length <= 1000
# trips[i].length == 3
# 1 <= numPassengers_i <= 100
# 0 <= from_i < to_i <= 1000
# 1 <= capacity <= 10^5


def car_pooling(trips: list[list[int]], capacity: int) -> bool:
    # The furthest point is the maximum value of to_i
    furthest_point = max(trip[2] for trip in trips)

    # The array indicates the change in passengers at each location
    num_passengers_changes = [0] * (furthest_point + 1)

    # For each trip event, 'num_passengers' enter at 'from' and leave at 'to'
    for num_passengers, enter_point, leave_point in trips:
        num_passengers_changes[enter_point] += num_passengers
        num_passengers_changes[leave_point] -= num_passengers

    # Do a prefix sum to get number of passengers on the car at each point
    num_passengers_on_car: int = 0
    for change in num_passengers_changes:
        num_passengers_on_car += change

        # Check if at any point the sum exceeds capacity
        if num_passengers_on_car > capacity:
            return False

    return True

# ==== Complexity =====
# (n = trips.length; m = furthest_point)
# - Time complexity: O(n + m)
# - Space complexity: O(m)