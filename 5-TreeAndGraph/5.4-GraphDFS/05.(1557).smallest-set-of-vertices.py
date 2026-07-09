"""
https://leetcode.com/problems/minimum-number-of-vertices-to-reach-all-nodes/

Given a directed acyclic graph, with n vertices numbered from 0 to n-1,
and an array edges where edges[i] = [x, y] represents a directed edge
from node x to node y.

Find the smallest set of vertices from which all nodes in the graph are reachable.
"""

"""
Analysis:
- Reframe problem: 
  . the smallest set of nodes from which all nodes can be reached
    <-> the set of nodes that cannot be reached from another node
  . If a node can be reached from another node,
    we should have include the parent rather than the child.
- A node cannot be reached from other nodes if it has an in-degree of 0
  (no edges entering the node).
- The graph is acyclic -> we don't have to handle cycles.

Idea:
- Find the in-degree of all nodes
- Add the ones with in-degree of 0 to the result set
"""


def find_smallest_set_of_vertices(n: int, edges: list[list[int]]) -> list[int]:
    indegree = [0] * n

    # iterate through directed edges, increase in-degree of target node
    for _, y in edges:
        indegree[y] += 1

    # return the nodes with in-degree of 0
    return [node for node in range(n) if indegree[node] == 0]


"""
Complexity:
- Number of nodes: n
  Number of edges: E = len(edges)

1. Time complexity: O(n + E)
- Init 'indegree': O(n)
- Iterate through edges: O(E)
- Collect nodes with in-degree of 0: O(n)

2. Space complexity: O(n) for 'indegree'
"""
