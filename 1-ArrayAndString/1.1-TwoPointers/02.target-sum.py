"""
Given a sorted array of unique integers and a target integer,
return true if there exists a pair of numbers that sum to target,
false otherwise.
For example, given nums = [1, 2, 4, 6, 8, 9, 14, 15] and target = 13,
return true because 4 + 9 = 13.
"""

"""
Some approaches:
1. Brute-force: 
- Iterate through 'nums'. For each item, 
  iterate through the remaining items to check if sum == target
-> Time complexity: O(n^2).

2. Hash table:
- Iterate through 'nums' and add items to a set.
  For each item 'num', if 'target - num' has been encountered, return True.
-> Time complexity: O(n)
   Space complexity: O(n)

3. 2 pointers (used):
- Use 2 pointers starting from both ends and move towards each other.
  Let sum = nums[left] + nums[right]
- Since 'nums' is sorted, right-- will decrease 'sum', left++ will increase 'sum'
  -> Adjust 'sum' towards 'target' by moving pointers.
"""


def target_sum(nums: list[int], target: int) -> bool:
    left = 0
    right = len(nums) - 1

    while left < right:
        sum = nums[left] + nums[right]
        if sum == target:
            return True
        elif sum > target:
            right -= 1
        else:
            left += 1

    return False


"""
Complexity:
1. Time complexity: O(n)
2. Space complexity: O(1)
"""
