# Given an array of integers arr and an integer k.
# Find the least number of unique integers after removing exactly k elements.

# Example 1:
# Input: arr = [5,5,4], k = 1
# Output: 1
# Explanation: Remove the single 4, only 5 is left.

# Example 2:
# Input: arr = [4,3,1,1,3,3,2], k = 3
# Output: 2
# Explanation: Remove 4, 2 and either one of the two 1s or three 3s. 1 and 3 will be left.

# Constraints:
# 1 <= arr.length <= 10^5
# 1 <= arr[i] <= 10^9
# 0 <= k <= arr.length


# ===== Analyze =====
# - The number of unique integers is reduced only if we remove all of an element
# => We should greedily remove the element with lowest frequency at each step

# ===== Implementation =====
# - Use a hashmap to track frequency of each element.
# - Sort the keys according to their frequencies.
# - Iterate through the keys starting from the least frequent element.
# - At each key, if the frequency f is less than or equal to k,
#   decrease k by f (effectively remove f elements) .
# - Stop when running out of removals. Count the number of keys remaining.


def least_unique_nums(arr: list[int], k: int) -> int:
    frequency_dict: dict[int, int] = {}
    for num in arr:
        if num not in frequency_dict:
            frequency_dict[num] = 0
        frequency_dict[num] += 1

    sorted_frequencies = sorted(frequency_dict.values(), reverse=True)

    while k > 0:
        min_frequency = sorted_frequencies[-1]
        if min_frequency > k:
            break
        k -= min_frequency
        sorted_frequencies.pop()

    return len(sorted_frequencies)


# ===== Complexity =====
# 1. Time complexity:
# - Build frequency_dict: O(n)
# - Sort the frequencies: O(n*log(n)) (worst case when all elements are unique)
# - The while loop can run at most n times: O(n)
# => Overall: O(n*log(n))
#
# 2. Space complexity:
# (worst case when all elements are unique)
# - O(n) for the hash map
# - O(n) for the frequencies array
# => Overall: O(n)
