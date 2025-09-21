# Given a directed acyclic graph (DAG) of n nodes labeled from 0 to n - 1,
# find all possible paths from node 0 to node n - 1 and return them in any order.
#
# The graph is given as follows:
# graph[i] is a list of all nodes you can visit from node i
# (i.e., there is a directed edge from node i to node graph[i][j]).

# Example 1:
# Input: graph = [[1,2],[3],[3],[]]
# Output: [[0,1,3],[0,2,3]]
# Explanation: There are two paths: 0 -> 1 -> 3 and 0 -> 2 -> 3.

# Example 2:
# Input: graph = [[4,3,1],[3,2,4],[3],[4],[]]
# Output: [[0,4],[0,3,4],[0,1,3,4],[0,1,2,3,4],[0,1,4]]

# Constraints:
# n == graph.length
# 2 <= n <= 15
# 0 <= graph[i][j] < n
# graph[i][j] != i (i.e., there will be no self-loops).
# All the elements of graph[i] are unique.
# The input graph is guaranteed to be a DAG.


# ===== Analysis =====
# - The graph format is an adjacency list
# - We need to find all paths from source to target
#   -> use backtracking, not just DFS/BFS
# - The input graph is a DAG
#   -> don't need to worry about cycles
#   -> don't need to track visited nodes for a path

# ===== Strategy =====
# - Use a function backtrack(path, i) to build each path, where:
#   . path is the current path being built.
#   . i represents the ith node.
# - Recurse on all nodes reachable from i.
# - For a path: start from source, stop when destination is reached.


def all_paths_from_source_to_target(graph: list[list[int]]) -> list[list[int]]:
    all_paths: list[list[int]] = []
    source = 0
    destination = len(graph) - 1

    def backtrack(path: list[int], i: int):
        if i == destination:
            # - We mutate 'path' across 'backtrack' calls,
            #   -> create a copy of 'path' when adding
            all_paths.append(path[:])
            return

        for neighbor in graph[i]:
            path.append(neighbor)
            backtrack(path, neighbor)
            path.pop()

    backtrack(path=[source], i=source)
    return all_paths
