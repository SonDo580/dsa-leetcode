"""
https://leetcode.com/problems/course-schedule-iv/

There are a total of `numCourses` courses you have to take, labeled from 0 to numCourses - 1.
You are given an array `prerequisites` where prerequisites[i] = [ai, bi] indicates that
you must take course bi first if you want to take course ai.

Prerequisites can also be indirect.
If course a is a prerequisite of course b,
and course b is a prerequisite of course c,
then course a is a prerequisite of course c.

You are also given an array queries where queries[j] = [uj, vj].
For the jth query, you should answer whether course uj is a prerequisite of course vj or not.

Return a boolean array answer, where answer[j] is the answer to the jth query.
"""

# === Approach 1: DFS/BFS ===
"""
- Build adjacency list.
- Start DFS/BFS from each node and record reachable nodes for start node.
  . Track visited nodes in a single traversal to avoid revisiting nodes.
  . Record reachable nodes: use hashmap or 2D matrix
- On query (u, v), check if v is reachable from u.
"""

from collections import defaultdict


def check_if_prerequisite(
    num_courses: int, prerequisites: list[list[int]], queries: list[list[int]]
) -> list[bool]:
    # adjacency list
    graph: defaultdict[int, list[int]] = defaultdict(list)
    for a, b in prerequisites:  # a is prerequisite of b
        graph[a].append(b)

    # reachable[i][j] = True -> j is reachable from i
    reachable: list[list[bool]] = [[False] * num_courses for _ in range(num_courses)]

    # perform DFS from each node to populate 'reachable'
    stack: list[int] = []
    for start in range(num_courses):
        visited = [False] * num_courses
        stack.append(start)
        visited[start] = True

        while stack:
            node = stack.pop()
            reachable[start][node] = True
            for neighbor in graph[node]:
                if not visited[neighbor]:
                    stack.append(neighbor)
                    visited[neighbor] = True

    # answer queries
    ans: list[bool] = []
    for a, b in queries:
        ans.append(reachable[a][b])

    return ans


"""
Complexity:
- Number of nodes: V = num_courses
  Number of edges: E = len(prerequisites)
  Number of queries: q = len(queries)

1. Time complexity: O(E + V + V^2 + V*E + q) = O(V^2 + V*E + q)
- Build adjacency list: O(E)
- Init 'reachable': O(V^2)
- DFS from each node: O(V + E)
  -> For all nodes: O(V*(V + E)) = O(V^2 + V*E)
- Answer 'queries': O(q)

2. Space complexity: O(V^2 + V + E) = O(V^2)
- adjacency list: O(V + E)
- 'reachable': O(V^2)
- DFS stack: O(V)
- 'visited': O(V)
"""
