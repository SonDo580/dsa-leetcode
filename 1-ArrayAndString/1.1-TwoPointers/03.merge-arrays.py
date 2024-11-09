# Given two sorted integer arrays arr1 and arr2,
# return a new array that combines both of them and is also sorted

from typing import List


def merge(arr1: List[int], arr2: List[int]) -> list[int]:
    result = []
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

    while j < len(arr2):
        result.append(arr2[j])

    return result
