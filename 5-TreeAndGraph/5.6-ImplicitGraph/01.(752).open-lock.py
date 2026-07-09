"""
https://leetcode.com/problems/open-the-lock/

You have a lock with 4 circular wheels.
Each wheel has the digits 0 to 9.
The wheels rotate and wrap around - so 0 can turn to 9 and 9 can turn to 0.
Initially, the lock reads "0000".
One move consists of turning a wheel one slot.
You are given an array of blocked codes 'deadends' -
if the lock reads any of these codes, then it can no longer turn.
Return the minimum number of moves to make the lock read 'target'.
"""

"""
Idea:
- Consider each lock state as a node.
  The neighbors are nodes that differ by 1 position by a value of 1.
  -> Perform BFS from node "0000" until reaching 'target'.
- We cannot visit any node in 'deadends'
  -> Mark all states in 'deadends' as visited
- To find the neighbors of a node:
  . Loop over each of the 4 slots
  . Increment and decrement the slot by 1
  . Handle wrap-around (increment(9) = 0 and decrement(0) = 9):
    . increment(x) = (x + 1) % 10
    . decrement(x) = (x - 1) % 10
"""

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
    START = "0000"

    # Start node is a deadend -> cannot move
    if START in seen:
        return -1

    seen.add(START)
    queue: deque[tuple[str, int]] = deque([(START, 0)])  # (node, steps)

    while queue:
        node, steps = queue.popleft()
        if node == target:
            return steps

        for neighbor in get_neighbors(node):
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append((neighbor, steps + 1))

    return -1  # cannot reach target


"""
Complexity:
- Number of wheels: n = 4
  Number of options on each wheel: m = 10
  Number of states (nodes): S = m^n
  Number of dead-ends: d = len(deadends) < S

1. Time complexity: O(m^n * n^2 + d) = O(m^n * n^2)
- Convert 'deadends' to a set: O(d)
- BFS:
  . Compute neighbors for each node: O(n*2*n) = O(n^2)
    . Loop through n wheels.
      Increment/decrement value for each wheel.
      String concatenation to compute 1 neighbor: O(n)
  . Visit all edges of each node: O(n) 
    . Each node has 2*n possible neighbors
  -> For all nodes: O(S * (n^2 + n)) = O(m^n * n^2)

2. Space complexity: O(S + d) = O(S) = O(m^n)
- 'seen': O(S)
- 'deadends_set': O(d)
- queue: O(S') where S' < S (don't hold all states at once)
- neighbors: O(n) (each node has 2*n neighbors)
"""
