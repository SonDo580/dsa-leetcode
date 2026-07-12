"""
https://leetcode.com/problems/course-schedule-ii/

... Similar to (207).course-schedule. But:

Return the ordering of courses you should take to finish all courses.
If there are many valid answers, return any of them.
If it is impossible to finish all courses, return an empty array.
"""

# ===== BFS approach (Kahn's Algorithm) =====
# ===========================================
from collections import defaultdict, deque


def find_order(num_courses: int, prerequisites: list[tuple[int, int]]) -> list[int]:
    in_degree: list[int] = [0] * num_courses
    graph: defaultdict[int, list[int]] = defaultdict(list)
    for a, b in prerequisites:
        graph[b].append(a)  # directed edge b->a
        in_degree[a] += 1

    queue: deque[int] = deque()
    for i in range(num_courses):
        if in_degree[i] == 0:
            queue.append(i)

    study_plan: list[int] = []
    while queue:
        i = queue.popleft()
        study_plan.append(i)

        for j in graph[i]:
            in_degree[j] -= 1
            if in_degree[j] == 0:
                queue.append(j)

    return study_plan if len(study_plan) == num_courses else []


"""
Complexity:
- Let V = num_courses         (number of vertices)
      E = len(prerequisites)  (number of edges)

1. Time complexity: O(V + E)
- Init 'in-degree': O(V)
- Build 'graph' and fill 'in-degree': O(E)
- Find starters (in-degree 0): O(V)
- BFS: O(V + E) (visit each node/edge once)

2. Space complexity: O(V + E)
- 'in_degree': O(V)
- 'graph' (adjacency list): O(V + E)
- queue: O(V)
"""


# ===== DFS approach ======
# =========================
"""
- Perform DFS from each node:
  . Skip nodes that have been visited in previous traversals.
  . All reachable nodes in each pass can be put sequentially in schedule.
- If we append vertices to result array in forward order:
  . The next traversal may include ancestors to visited nodes,
    which must be put before visited nodes in result array
  . But prepending to array is inefficient.
  -> Record the vertices in reverse order.
     Reverse the list after processing all nodes.
  -> Use post-order DFS to process neighbors first.

- Cycle detection:
  . Each node can be in 1 of 3 states (colors):
    . unvisited (white)
    . pending (gray): encountered but hasn't been processed (explore neighbors first)
    . processed (black)
  . While performing DFS, if a gray node is encountered
    -> There's a cycle.
"""

from enum import Enum


class NodeState(Enum):
    UNVISITED = 0
    PENDING = 1
    PROCESSED = 2


def find_order(num_courses: int, prerequisites: list[tuple[int, int]]) -> list[int]:
    graph: defaultdict[int, list[int]] = defaultdict(list)
    for a, b in prerequisites:
        graph[b].append(a)

    reversed_study_plan: list[int] = []
    state: list[NodeState] = [NodeState.UNVISITED] * num_courses
    has_cycle: bool = False

    def dfs(i: int) -> None:
        nonlocal has_cycle
        if has_cycle:  # cycle detected somewhere
            return

        state[i] = NodeState.PENDING
        for j in graph[i]:
            if state[j] == NodeState.PENDING:
                has_cycle = True
                return
            if state[j] == NodeState.UNVISITED:
                dfs(j)

        reversed_study_plan.append(i)
        state[i] = NodeState.PROCESSED

    for k in range(num_courses):
        if state[k] == NodeState.UNVISITED:
            dfs(k)

    return [] if has_cycle else list(reversed(reversed_study_plan))


"""
Complexity:
- Let V = num_courses         (number of vertices)
      E = len(prerequisites)  (number of edges)
      D = O(V)                (max depth)

1. Time complexity: O(V + E)
- Build 'graph': O(E)
- Init 'state': O(V)
- DFS in total: O(V + E)
- Reverse the reversed study plan: O(V)

2. Space complexity: O(V + E + D) = O(V + E)
- 'graph' (adjacency list): O(V + E)
- DFS recursion stack: O(D)
"""
