"""
https://leetcode.com/problems/parallel-courses/

You are given an integer n,
which indicates that there are n courses labeled from 1 to n.
You are also given an array 'relations' where relations[i] = [prevCoursei, nextCoursei],
representing a prerequisite relationship between course prevCoursei and course nextCoursei:
course prevCoursei has to be taken before course nextCoursei.

In one semester, you can take any number of courses as long as you have taken
all the prerequisites in the previous semester for the courses you are taking.

Return the minimum number of semesters needed to take all courses.
If there is no way to take all the courses, return -1.
"""

"""
Idea: 
- To take all courses with the minimum number of semesters,
  try to take as much courses as possible in each semester.
  -> Takes all courses with no prerequisites in each semester.
  -> Use Kahn's algorithm (BFS).
     . courses are nodes.
     . prerequisites are directed edges.

Implementation:
- Add all nodes with in-degree 0 to queue.
- Process all nodes at each level before moving on.
  Decrement the in-degree of children for each processed node.
  If the in-degree of a child becomes 0, add it the queue.
- number or minimum semesters = number of levels.
"""

from collections import defaultdict, deque


def min_semesters(n: int, relations: list[list[int]]) -> int:
    in_degree = [0] * (n + 1)  # entry 0 is not used (nodes are 1-indexed)
    adj_list: defaultdict[int, list[int]] = defaultdict(list)
    for a, b in relations:  # a is prerequisite of b
        adj_list[a].append(b)
        in_degree[b] += 1

    queue: deque[int] = deque()
    for i in range(1, n + 1):  # nodes are 1-indexed
        if in_degree[i] == 0:
            queue.append(i)

    level = 0
    studied = 0
    while queue:
        level += 1
        curr_len = len(queue)
        for _ in range(curr_len):  # process all nodes at current level
            node = queue.popleft()
            studied += 1  # study 'node'

            for child in adj_list[node]:
                in_degree[child] -= 1  # completed prerequisite 'node'
                if in_degree[child] == 0:
                    queue.append(child)

    return level if studied == n else -1


"""
Complexity:
- Number of nodes: n
  Number of edges: E = len(relations)
  . worst case: E = O(n^2)

1. Time complexity: O(n + E)
- Init 'in_degree': O(n)
- Build adjacency list and fill 'in_degree': O(E)
- BFS: O(n + E)

2. Space complexity: O(n + E)
- 'in_degree': O(n)
- adjacency list: O(n + E)
- queue: O(n)
"""
