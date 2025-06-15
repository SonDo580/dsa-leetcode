# You are given an integer array arr.
# You can choose a set of integers and remove all the occurrences of these integers in the array.
# Return the minimum size of the set so that at least half of the integers of the array are removed.

# Example 1:
# Input: arr = [3,3,3,3,5,5,5,2,2,7]
# Output: 2
# Explanation: Choosing {3,7} will make the new array [5,5,5,2,2] which has size 5 (i.e equal to half of the size of the old array).
# Possible sets of size 2 are {3,5},{3,2},{5,2}.
# Choosing set {2,7} is not possible as it will make the new array [3,3,3,3,5,5,5] which has a size greater than half of the size of the old array.

# Example 2:
# Input: arr = [7,7,7,7,7,7]
# Output: 1
# Explanation: The only possible set you can choose is {7}. This will make the new array empty.

# Constraints:
# 2 <= arr.length <= 10^5
# arr.length is even.
# 1 <= arr[i] <= 10^5


# ===== Analyze =====
# - The goal is to remove as much integers as possible each time.
# -> Just remove the most frequent integer at any step.

# ===== Implementation =====
# - Build a hash map to store frequency of each integer
# - Sort the entries by frequency in descending order
# - Loop through the entries and keep decreasing count by frequency
# - Stop when count <= n / 2 (n is guaranteed to be even)


def min_set_size(arr: list[int]) -> int:
    frequency_dict: dict[int, int] = {}
    for num in arr:
        if num not in frequency_dict:
            frequency_dict[num] = 0
        frequency_dict[num] += 1

    frequencies = sorted(frequency_dict.values(), reverse=True)

    removed = 0
    half = len(arr) / 2
    set_size = 0

    for frequency in frequencies:
        removed += frequency
        set_size += 1
        if removed >= half:
            break

    return set_size


# ===== Complexity =====
# (worst case when all integers are unique)
# 
# 1. Time complexity:
# - build frequency dict: O(n)
# - gather frequencies from dict: O(n)
# - sort the frequencies: O(n*log(n))
# - iterate through frequencies: O(n)
# => Overall: O(n*log(n))
#
# 2. Space complexity:
# - space for frequency_dict: O(n)  
# - space for frequencies list: O(n)
