# Given a 2D array nums that contains n arrays of distinct integers,
# return a sorted array containing all the numbers that appear in all n arrays.

# For example, given nums = [[3,1,2,4,5],[1,2,3,4],[3,4,5,6]],
# return [3, 4]. 3 and 4 are the only numbers that are in all arrays.

# => Analyze:
# - each array contains distinct elements
#   -> appears in all arrays <=> appears n times

from typing import List


def intersection(nums: List[List[int]]) -> List[int]:
    counts = {}

    for arr in nums:
        for x in arr:
            if x not in counts:
                counts[x] = 0
            counts[x] += 1

    result = []
    for key in counts:
        if counts[key] == len(nums):
            result.append(key)

    return sorted(result)

# Time complexity analysis:
# - n lists and each list has an average of m elements
# - O(n*m) to populate the hash map
#
# Case 1: all the elements are unique
# - O(n*m) to iterate over the hash map
# - but result will be empty -> no sorting
# 
# Case 2: m unique elements 
# - O(m) to iterate over the hash map
# - O(m*log(m)) for the sorting
#
# => Total: 
# - case 1: O(n*m)
# - case 2: O(n*m) + O(m) + O(m*log(m)) = O(m*(n + log(m))) 

# Space complexity: O(n*m) - all elements are unique