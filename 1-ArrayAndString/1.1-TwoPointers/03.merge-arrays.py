"""
Given two sorted integer arrays 'arr1' and 'arr2',
return a new array that combines both of them and is also sorted
"""


def merge(arr1: list[int], arr2: list[int]) -> list[int]:
    result: list[int] = []
    i = 0
    j = 0

    while i < len(arr1) and j < len(arr2):
        if arr1[i] < arr2[j]:
            result.append(arr1[i])
            i += 1
        else:
            result.append(arr2[j])
            j += 1

    while i < len(arr1):
        result.append(arr1[i])
        i += 1

    while j < len(arr2):
        result.append(arr2[j])
        j += 1

    return result


"""
Complexity:
- Let m = len(arr1), n = len(arr2)
1. Time complexity: O(m + n)
2. Space complexity: O(1)
"""
