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


def find_order(num_courses: int, prerequisites: list[tuple[int, int]]) -> bool:
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
- Build 'graph' and 'in-degree': O(E)
- Find starters (in-degree 0): O(V)
- BFS: O(V + E)

2. Space complexity: O(V + E)
- 'in_degree': O(V)
- 'graph': O(E)
- queue: O(V)
"""


# ===== DFS iterative =====
# =========================
"""
- Perform DFS from each node.
  We cannot add in desired order since the starting node may have prerequisites.
  -> Add the vertices in reverse order
  -> Use post-order DFS to process neighbors first.
- Use 4 states for node to implement post-order DFS
  . unvisited: initial state
  . visited: set on the first encounter
  . pending: set when adding node back to stack (explore neighbors first)
  . processed: set after processing done
- Reverse the list after processing all nodes.
- Cycle detection:
  . If encounter a pending node when checking neighbors 
    -> there's a cycle.

The above approach has a problem:
. If a has neighbors = [c, b], and b has neighbors = [c],
  we only add c to the stack once when exploring a's neighbors.
. When exploring b's neighbors, we see that c is already visited,
  so we don't add it to the stack again.
. Then b is processed and added to the reversed result list before c.
. But because of the edge (b -> c), c should be added before b.
=> 
. We should allow re-adding a visited node to the stack,
  in case another node on the path also points to it.
. Now there may be multiple instances of a visited node on the stack.
  But each node should only be processed once, so if we pop a node that
  has been processed (in another path), just ignore it.
. The visited state is "useless" now, since we can add visited node back.
  Just use 3 states: unvisited, pending, processed. 
"""

from enum import Enum


class NodeState(Enum):
    UNVISITED = 0
    PENDING = 1
    PROCESSED = 2


def find_order(num_courses: int, prerequisites: list[tuple[int, int]]) -> bool:
    graph: defaultdict[int, list[int]] = defaultdict(list)
    for a, b in prerequisites:
        graph[b].append(a)

    reversed_study_plan: list[int] = []
    stack: list[int] = []
    state: list[NodeState] = [NodeState.UNVISITED] * num_courses

    for k in range(num_courses):
        if state[k] == NodeState.UNVISITED:
            stack.append(k)

        while stack:
            i = stack.pop()
            if state[i] == NodeState.PENDING:
                reversed_study_plan.append(i)
                state[i] = NodeState.PROCESSED
                continue

            if state[i] == NodeState.PROCESSED:
                # already processed in another path
                continue

            # add back to process after neighbors
            stack.append(i)
            state[i] = NodeState.PENDING

            for j in graph[i]:
                if state[j] == NodeState.PENDING:
                    # already encounter in current path -> cycle
                    return []
                if state[j] == NodeState.UNVISITED:
                    stack.append(j)

    return list(reversed(reversed_study_plan))


"""
Complexity:

1. Time complexity: O(V + E)
- Build 'graph': O(E)
- Init 'state': O(V)
- DFS: O(V + E) 

2. Space complexity: O(D + E)
- 'graph': O(E)
- stack: O(D) where D is the maximum depth
"""


# ===== DFS recursive =====
# =========================
"""
Same idea as iterative approach. But:
- Leverage recursion to handle ordering.
- Don't need to explicitly check if a node has been processed by another path,
  since we explore full path before moving to the next neighbor.
- Cannot break early when detect cycle -> use a flag.
"""


def find_order(num_courses: int, prerequisites: list[tuple[int, int]]) -> bool:
    graph: defaultdict[int, list[int]] = defaultdict(list)
    for a, b in prerequisites:
        graph[b].append(a)

    reversed_study_plan: list[int] = []
    state: list[NodeState] = [NodeState.UNVISITED] * num_courses
    has_cycle: bool = False

    def dfs(i: int):
        nonlocal has_cycle
        if has_cycle:
            # cycle detected somewhere
            return

        state[i] = NodeState.PENDING
        for j in graph[i]:
            if state[j] == NodeState.PENDING:
                # already encounter in current path -> cycle
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

1. Time complexity: O(V + E)
- Build 'graph': O(E)
- Init 'state': O(V)
- DFS: O(V + E)

2. Space complexity: O(V + E)
- 'graph': O(E)
- stack: O(D) -> O(V)
"""
