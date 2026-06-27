"""
https://leetcode.com/problems/how-many-apples-can-you-put-into-the-basket/

You have some apples and a basket that can carry up to 5000 units of weight.
Given an integer array 'weight' where weight[i] is the weight of the ith apple,
return the maximum number of apples you can put in the basket.
"""

"""
Strategy:
- To maximize the number of apples that we can put in the basket, 
  always choose the lightest one at each step.

Implementation:
- Sort weights in increasing order.
- Loop through sorted weights and add apples to the basket.
- Stop when the total weight exceed capacity (5000 units).
"""


def max_apples_in_basket(weights: list[int]) -> int:
    weights.sort()

    total_weight = 0
    num_apples = 0

    for weight in weights:
        if total_weight + weight > 5000:
            break
        total_weight += weight
        num_apples += 1

    return num_apples


"""
Complexity:
- Let n = len(weights)

1. Time complexity:
- sort 'weights': O(n*log(n))
- iterate through 'weights': O(n)
=> Overall: O(n*log(n))

2. Space complexity: O(n) for sorting (timsort)
"""
