"""
https://leetcode.com/problems/intersection-of-multiple-arrays/

Given a 2D array 'nums' that contains n arrays of distinct integers,
return a sorted array containing all the numbers that appear in all n arrays.

For example, given nums = [[3,1,2,4,5],[1,2,3,4],[3,4,5,6]],
return [3, 4]. 3 and 4 are the only numbers that are in all arrays.
"""

"""
Analysis:
- each array contains distinct elements
  -> element appears in all arrays <-> element appears n times

Idea:
- iterate through all array to collect frequencies of all elements.
  (use a dict).
- iterate through frequency dict to collection elements appears n times.
- sort the result.
"""

from collections import defaultdict


def intersection(nums: list[list[int]]) -> list[int]:
    cnt: defaultdict[int, int] = defaultdict(int)
    for arr in nums:
        for x in arr:
            cnt[x] += 1

    result: list[int] = []
    n = len(nums)
    for key in cnt:
        if cnt[key] == n:
            result.append(key)

    result.sort()
    return result


"""
Complexity:
- Let n = number of arrays, m = number of elements in each array   

1. Time complexity:
- Build 'cnt': O(n*m)
- If all elements are unique:
  . iterate through 'cnt' takes O(n*m)
  . result is empty -> no sorting
- If m unique elements appear in n arrays
  . iterate through 'cnt' takes O(m)
  . sorting result: O(n*log(n))
=> Time complexity:
   . case 1: O(n*m) + O(n*m) = O(n*m)
   . case 2: O(n*m) + O(m) + O(n*log(n)) = O(n*(m + log(n)))

2. Space complexity: 
- If all elements are unique: O(n*m) for 'cnt'
- If m unique elements appear in n arrays: O(m + n)
  . O(m) for 'cnt'
  . O(n) for sorting (timsort)
"""
