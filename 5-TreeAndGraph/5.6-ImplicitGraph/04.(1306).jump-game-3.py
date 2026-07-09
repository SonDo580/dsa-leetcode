"""
https://leetcode.com/problems/jump-game-iii/

Given an array of non-negative integers 'arr',
you are initially positioned at start index of the array.
When you are at index i, you can jump to i + arr[i] or i - arr[i],
check if you can reach any index with value 0.

Notice that you can not jump outside of the array at any time.
"""

"""
Strategy:
- Treat the whole array as a graph.
  Neighbors of node i are i - arr[i] and i + arr[i]
  (must be in range [0, arr.length - 1])
- Perform DFS/BFS from 'start' node.
  Return True if we can reach a node with value 0.
"""


def can_reach(arr: list[int], start: int) -> bool:
    n = len(arr)
    seen: set[int] = {start}  # track visited nodes by index
    stack: list[int] = [start]

    while stack:
        i = stack.pop()
        if arr[i] == 0:
            return True

        for next_i in [i - arr[i], i + arr[i]]:
            if 0 <= next_i < n and next_i not in seen:
                seen.add(next_i)
                stack.append(next_i)

    return False


"""
Complexity:
- Number of nodes: N = len(arr)
  Number of edges: E = O(2*N) = O(N)

1. Time complexity: O(N)
- DFS: O(N + E) = O(N)

2. Space complexity: O(N)
- 'seen': O(N)
- stack: O(N') where N' < N (don't hold all nodes at once)
"""
