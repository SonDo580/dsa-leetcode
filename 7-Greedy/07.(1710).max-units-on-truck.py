"""
https://leetcode.com/problems/maximum-units-on-a-truck/

You are assigned to put some amount of boxes onto one truck.
You are given a 2D array 'boxTypes', where boxTypes[i] = [numberOfBoxes_i, numberOfUnitsPerBox_i]:
- numberOfBoxes_i is the number of boxes of type i.
- numberOfUnitsPerBox_i is the number of units in each box of the type i.

You are also given an integer 'truckSize',
which is the maximum number of boxes that can be put on the truck.
You can choose any boxes to put on the truck as long as the number of boxes does not exceed truckSize.
Return the maximum total number of units that can be put on the truck.
"""

"""
Strategy:
- To maximize the number of units for the same amount of boxes,
  always choose the box type with the most number of units at any step.

Implementation:
- Sort boxTypes in decreasing order by number of units.
- Loop through sorted boxTypes, reduce the number of truck space
  by number of boxes (if num_boxes > remaining_space, reduce by remaining_space),
  and accumulate the units.
"""


def max_units_on_truck(box_types: list[list[int, int]], truck_size: int) -> int:
    box_types.sort(key=lambda b: b[1], reverse=True)  # by units-per-box
    max_units = 0
    remaining_space = truck_size

    for num_boxes, units_per_box in box_types:
        num_boxes_to_take = min(num_boxes, remaining_space)
        max_units += units_per_box * num_boxes_to_take
        remaining_space -= num_boxes_to_take
        if remaining_space == 0:
            break

    return max_units


"""
Complexity:
- Let n = len(boxTypes)

1. Time complexity:
- sort boxTypes: O(n*log(n))
- iterate through boxTypes: O(n)
=> Overall: O(n*log(n))

2. Space complexity: O(n) for sorting (timsort)
"""
