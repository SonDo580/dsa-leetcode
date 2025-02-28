# Given an integer array nums,
# find all the unique numbers x in nums that satisfy the following:
# x + 1 is not in nums, and x - 1 is not in nums.

def find_numbers(nums: list[int]) -> list[int]:
    result = []
    num_set = set(nums)

    for num in nums:
        if (num + 1 not in num_set) and (num - 1) not in num_set:
            result.append(num)

    return result


# Time complexity: O(n)
# Space complexity: O(n)
