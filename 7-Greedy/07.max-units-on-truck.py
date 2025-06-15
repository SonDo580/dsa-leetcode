# You are assigned to put some amount of boxes onto one truck.
# You are given a 2D array boxTypes, where boxTypes[i] = [numberOfBoxes_i, numberOfUnitsPerBox_i]:
# - numberOfBoxes_i is the number of boxes of type i.
# - numberOfUnitsPerBox_i is the number of units in each box of the type i.
#
# You are also given an integer truckSize,
# which is the maximum number of boxes that can be put on the truck.
# You can choose any boxes to put on the truck as long as the number of boxes does not exceed truckSize.
# Return the maximum total number of units that can be put on the truck.

# Example 1:
# Input: boxTypes = [[1,3],[2,2],[3,1]], truckSize = 4
# Output: 8
# Explanation: There are:
# - 1 box of the first type that contains 3 units.
# - 2 boxes of the second type that contain 2 units each.
# - 3 boxes of the third type that contain 1 unit each.
# You can take all the boxes of the first and second types, and one box of the third type.
# The total number of units will be = (1 * 3) + (2 * 2) + (1 * 1) = 8.

# Example 2:
# Input: boxTypes = [[5,10],[2,5],[4,7],[3,9]], truckSize = 10
# Output: 91

# Constraints:
# 1 <= boxTypes.length <= 1000
# 1 <= numberOfBoxesi, numberOfUnitsPerBoxi <= 1000
# 1 <= truckSize <= 10^6


# ===== Analyze =====
# - To maximize the number of units for the same amount of boxes,
#   we should choose the box with the most number of units at any step.

# ===== Implementation =====
# - Sort boxTypes in decreasing order by number of units.
# - Loop through sorted boxTypes, reduce the number of truck space
#   by number of boxes (if num_boxes > remaining_space, reduce by remaining_space),
#   and accumulate the units.


def max_units_on_truck(box_types: list[list[int, int]], truck_size: int) -> int:
    box_types.sort(key=lambda b: b[1], reverse=True)
    max_units = 0
    remaining_space = truck_size

    for num_boxes, units_per_box in box_types:
        num_boxes_to_take = (
            num_boxes if num_boxes <= remaining_space else remaining_space
        )
        max_units += units_per_box * num_boxes_to_take
        remaining_space -= num_boxes_to_take

    return max_units

# ===== Complexity =====
# 
# Time complexity:
# - sort the array: O(n*log(n))
# - iterate through the array: O(n)
# => Overall: O(n*log(n))
#
# Space complexity: depends on the sort function
# - built-in sort method of Python (timsort): O(n)
