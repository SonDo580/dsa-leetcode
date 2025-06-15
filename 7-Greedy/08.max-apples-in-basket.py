# You have some apples and a basket that can carry up to 5000 units of weight.
# Given an integer array weight where weight[i] is the weight of the ith apple,
# return the maximum number of apples you can put in the basket.

# Example 1:
# Input: weight = [100,200,150,1000]
# Output: 4
# Explanation: All 4 apples can be carried by the basket since their sum of weights is 1450.

# Example 2:
# Input: weight = [900,950,800,1000,700,800]
# Output: 5
# Explanation: The sum of weights of the 6 apples exceeds 5000 so we choose any 5 of them.

# Constraints:
# 1 <= weight.length <= 10^3
# 1 <= weight[i] <= 10^3


# ===== Analyze =====
# - To maximize the number of apples, we should choose the lightest one at each step.

# ===== Implementation =====
# - Sort weights in increasing order.
# - Loop through sorted weights and add apples to the basket
# - Stop when the total weight exceed capacity (5000 units)


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


# ===== Complexity =====
#
# Time complexity:
# - sort the array: O(n*log(n))
# - iterate through the array: O(n)
# => Overall: O(n*log(n))
#
# Space complexity: depends on the sort function
# - built-in sort method of Python (timsort): O(n)
