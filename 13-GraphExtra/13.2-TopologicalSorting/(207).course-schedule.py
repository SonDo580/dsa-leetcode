"""
https://leetcode.com/problems/course-schedule/

There are a total of `numCourses` courses you have to take, labeled from 0 to numCourses - 1.
You are given an array `prerequisites` where prerequisites[i] = [ai, bi] indicates that
you must take course bi first if you want to take course ai.

For example, the pair [0, 1], indicates that to take course 0 you have to first take course 1.
Return true if you can finish all courses. Otherwise, return false.
"""

"""
Topological sorting:
- Provide a linear sorting based on the required ordering of vertices
  in a directed acyclic graph (DAG).
"""


# ===== BFS approach (Kahn's Algorithm) =====
# ===========================================
"""
Idea:
- Study a course with no prerequisites first.
- Remove it from prerequisites of other courses.
- Repeat until all courses are studied.

Implementation (BFS):
- BFS from vertices with in-degree 0.
- Dequeue and process each vertex.
  Decrement the in-degree of vertices that current vertex points to.
  Add vertices whose in-degree have reduced to 0 to the queue. 
  Repeat until all vertices are processed.
- Cycle detection:
  . There are vertices that haven't been processed, 
    but no ones with in-degree 0 -> cannot proceed.
- Notes:
  . Build adjacency list to look up neighbors quickly.
  . Use an array 'in_degree' to track in-degree of vertices.
"""

from collections import defaultdict, deque


def can_finish(num_courses: int, prerequisites: list[tuple[int, int]]) -> bool:
    in_degree: list[int] = [0] * num_courses
    graph: defaultdict[int, list[int]] = defaultdict(list)
    for a, b in prerequisites:
        graph[b].append(a)  # directed edge b->a
        in_degree[a] += 1

    queue: deque[int] = deque()
    for i in range(num_courses):
        if in_degree[i] == 0:
            queue.append(i)

    count: int = 0
    while queue:
        i = queue.popleft()
        count += 1

        for j in graph[i]:
            in_degree[j] -= 1
            if in_degree[j] == 0:
                queue.append(j)

    return count == num_courses


"""
Complexity:
- Let V = num_courses         (number of vertices)
      E = len(prerequisites)  (number of edges)

1. Time complexity: O(V + E)
- Init 'in-degree': O(V)
- Build 'graph' and fill 'in-degree': O(E)
- Find starters (in-degree 0): O(V)
- BFS: O(V + E) (visit each vertex/edge once)

2. Space complexity: O(V + E)
- 'graph' (adjacency list): O(V + E)
- 'in_degree': O(V)
- queue: O(V)
"""
