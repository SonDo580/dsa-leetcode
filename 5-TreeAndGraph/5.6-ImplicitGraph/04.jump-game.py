# Given an array of non-negative integers arr,
# you are initially positioned at start index of the array.
# When you are at index i, you can jump to i + arr[i] or i - arr[i],
# check if you can reach any index with value 0.
#
# Notice that you can not jump outside of the array at any time.

# Example 1:
# Input: arr = [4,2,3,0,3,1,2], start = 5
# Output: true
# Explanation:
# All possible ways to reach at index 3 with value 0 are:
# index 5 -> index 4 -> index 1 -> index 3
# index 5 -> index 6 -> index 4 -> index 1 -> index 3

# Example 2:
# Input: arr = [4,2,3,0,3,1,2], start = 0
# Output: true
# Explanation:
# One possible way to reach at index 3 with value 0 is:
# index 0 -> index 4 -> index 1 -> index 3

# Example 3:
# Input: arr = [3,0,2,1,2], start = 2
# Output: false
# Explanation: There is no way to reach at index 1 with value 0.


# ===== Strategy =====
# - Treat the whole array as a graph.
# - Neighbors of node i are i - arr[i] and i + arr[i]
#   if they are in range [0, arr.length - 1]
# - Perform a traversal (DFS or BFS) from 'start' node.
#   Return True if we can reach a node with value 0. Otherwise return False.


def can_reach(arr: list[int], start: int) -> bool:
    seen: set[int] = {start}  # track visited nodes by index
    stack: list[int] = [start]

    while stack:
        i = stack.pop()

        if arr[i] == 0:
            return True

        for next_i in [i - arr[i], i + arr[i]]:
            if next_i not in seen and 0 <= next_i < len(arr):
                seen.add(next_i)
                stack.append(next_i)

    return False
