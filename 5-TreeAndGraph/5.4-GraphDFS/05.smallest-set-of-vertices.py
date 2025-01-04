# Given a directed acyclic graph, with n vertices numbered from 0 to n-1,
# and an array edges where edges[i] = [x, y] represents a directed edge
# from node x to node y. Find the smallest set of vertices
# from which all nodes in the graph are reachable.

# ===== Analyzed =====
# - Reframe: the smallest set of nodes from which all nodes can be reached
#            <=>
#            the smallest set of nodes that cannot be reached from another node
#   (if a node can be reached from another node,
#    we would include the parent rather the child)
#
# - A node cannot be reached from other nodes if it has an in-degree of 0
#   (no edges entering the node)
#
# - The graph is acyclic -> we don't have to handle cycles

# ===== Strategy =====
# - Find the in-degree of all nodes
# - Add the ones with in-degree of 0 to the result set

from typing import List


def find_smallest_set_of_vertices(n: int, edges: List[List[int]]) -> List[int]:
    # initialize the in-degrees of all nodes
    indegree = [0] * n

    # loop through the edges, increase the in-degree of the target node
    for _, y in edges:
        indegree[y] += 1

    # add the nodes with in-degree of 0 to the result
    result = []
    for node in range(n):
        if indegree[node] == 0:
            result.add(node)

    return result
