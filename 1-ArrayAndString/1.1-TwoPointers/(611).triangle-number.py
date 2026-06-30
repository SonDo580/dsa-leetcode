"""
https://leetcode.com/problems/valid-triangle-number/

Given an integer array 'nums',
return the number of triplets chosen from the array that
can make triangles if we take them as side lengths of a triangle.
"""

"""
Idea:
- Triangle property: a + b > c where a, b, c are side lengths
  -> Find triplets that satisfy the above inequality.
  -> Similar to 3Sum problem.

Algorithm:
- Sort 'nums' in ascending order.
- Let c moves through 'nums' in reverse order
  (so it is always the largest value in the triplet (a <= b <= c))
- Apply 2 pointers to find a, b in the remaining items:
  . Start from both ends and move inward.
  . If a + b > c, it means x + b > c for all x > a
    -> the array is sorted so x = all numbers between b and a
    -> increase number of valid pairs by b - a, then decrease b
  . If a + b <= c -> increase a since b is already the largest
"""


def triangleNumber(nums: list[int]) -> int:
    n = len(nums)
    nums.sort()
    count = 0

    # k runs from n - 1 to 2
    for k in range(n - 1, 1, -1):
        j = k - 1
        i = 0

        while i < j:
            if nums[i] + nums[j] > nums[k]:
                count += j - i
                j -= 1
            else:
                i += 1

    return count


"""
Complexity:
- Let n = len(nums)

1. Time complexity: O(n^2)
- sorting: O(n*log(n))
- Outer for loop: n - 2 iterations
  . Inner while loop: k - 1 iterations (i and j move until overlap)
  -> Total: (n - 1 - 1) + (n - 2 - 1) + ... + (2 - 1)
          = (n - 2) + (n - 3) + ... + 1
          = (n - 1) * (n - 2) / 2 
=> Overall: O(n^2) + O(n*log(n)) = O(n^2)

2. Space Complexity: O(n) for sorting (timsort)
"""
