# You have a lock with 4 circular wheels.
# Each wheel has the digits 0 to 9.
# The wheels rotate and wrap around - so 0 can turn to 9 and 9 can turn to 0.
# Initially, the lock reads "0000".
# One move consists of turning a wheel one slot.
# You are given an array of blocked codes 'deadends' -
# if the lock reads any of these codes, then it can no longer turn.
# Return the minimum number of moves to make the lock read 'target'.


# ===== Analyze =====
# - We can consider each lock state as a node.
#   The neighbors are nodes that differ by 1 position by a value of 1.
# => We can perform a BFS from node "0000".
# - We cannot visit any node in 'deadends'
#   => Mark all states in 'deadends' as visited
# - To find the neighbors of a node:
#   + Loop over each of the 4 slots
#   + Increment and decrement the slot by 1
#   + To handle wrap-around (9 <-> 0), we can use modulo operator:
#   -> increment(x) = (x + 1) % 10
#      decrement(x) = (x - 1) % 10

from collections import deque


def open_lock(deadends: list[str], target: str) -> int:
    def get_neighbors(node: str) -> list[str]:
        neighbors: list[str] = []
        for i in range(4):
            num = int(node[i])
            for change in [-1, 1]:
                x = (num + change) % 10
                neighbors.append(f"{node[:i]}{x}{node[i + 1:]}")
        return neighbors

    seen: set[str] = set(deadends)  # track visited nodes

    # Start node is a deadend -> cannot move
    START = "0000"
    if START in seen:
        return -1

    seen.add(START)
    queue: deque[tuple[str, int]] = deque([(START, 0)])  # (node, moves)

    while queue:
        node, moves = queue.popleft()

        if node == target:
            return moves

        for neighbor in get_neighbors(node):
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append((neighbor, moves + 1))

    return -1  # cannot reach target

# ===== Complexity =====
# - Let: n be the number of wheels
#        m be the number of options on each wheel 
#        d be the number of dead-ends
#        -> number of states: m^n 
# 
# 1. Time complexity
# - Convert 'deadends' to a set: O(d)
# - Visit all nodes: O(m^n)
# - Compute neighbors for each node: O(n^2)
#   + Loop through n wheels: O(n)
#   + String concatenation to compute 1 neighbor: O(n) 
# - Explore all edges of each node: O(n) (each node has 2*n possible neighbors)
# => Overall: O(m^n * (n^2 + n) + d) = O(m^n * n^2 + d)
# 
# 2. Space complexity: O(m^n)
# - Space for 'seen' ~ number of states: O(m^n) 
# - Space for 'queue' will not exceed O(m^n), since we also do removal
# 
# * In this problem, n and m are both fixed (n = 4 and m = 10)
#   -> they do not affect complexity
#   -> both time and complexity are O(d)