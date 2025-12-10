"""
https://leetcode.com/problems/next-greater-element-i/

The next greater element of some element x in an array is
the first greater element that is to the right of x in the same array.

You are given two distinct 0-indexed integer arrays nums1 and nums2,
where nums1 is a subset of nums2.

For each 0 <= i < nums1.length, find the index j such that nums1[i] == nums2[j]
and determine the next greater element of nums2[j] in nums2.
If there is no next greater element, then the answer for this query is -1.

Return an array 'ans' of length nums1.length such that
ans[i] is the next greater element as described above.

Follow up: Could you find an O(nums1.length + nums2.length) solution?
"""

"""
Brute-force approach: O(m * n^2) (m = nums1.length, n = nums2.length)
- For each element nums1[i], find the equal element nums2[j],
  then scan forward in nums2 to find the first greater element.

=> Improvement:
- Iterate through nums2 and push elements to a stack.
  (the stack is monotonically non-increasing)
- Before pushing, keep popping elements off the stack if 
  they are less than current nums2[j'].
- For each popped-off nums2[j], check if that number exists in nums1.
  If yes, find the index i in nums1.
- Update answers[i] = nums2[j']. Don't update if it's already set, 
  since we only want the first greater element.
- We can build a dictionary that map value to index for nums1
  (enable fast checking).
"""


def next_greater_element(nums1: list[int], nums2: list[int]) -> list[int]:
    # Initialize answers
    answers: list[int] = [-1] * len(nums1)

    # Build a dictionary to lookup the index of a value in nums1
    val_to_idx_1: dict[int, int] = {}
    for i, num in enumerate(nums1):
        val_to_idx_1[num] = i

    stack: list[int] = []

    for current_num in nums2:
        # Keep popping element off the stack if they are less than current_num
        while len(stack) > 0 and stack[-1] < current_num:
            num = stack.pop()

            # Check if num exists in nums1
            if num in val_to_idx_1:
                # Retrieve the index of num in nums1
                i = val_to_idx_1[num]

                # Set the next greater element for nums1[i]
                answers[i] = current_num

        stack.append(current_num)

    return answers


"""
Complexity:
- Let m = nums1.length; n = nums2.length

1. Time complexity:
- Initialize answers: O(m)
- Build nums1's value-index dictionary: O(m)
- Loop through nums2: O(n)
  . Each iteration is amortized O(1), since the inner while loop can run at most n times
    (each element is pushed on the stack exactly once, and popped from the stack at most once)
=> Overall: O(m + n)
    
2. Space complexity:
- nums1's value-index dictionary: O(m)
- stack: O(n) 
=> Overall: O(m + n)
"""
