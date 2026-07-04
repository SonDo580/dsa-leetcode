"""
https://leetcode.com/problems/all-paths-from-source-to-target/

Given a directed acyclic graph (DAG) of n nodes labeled from 0 to n - 1,
find all possible paths from node 0 to node n - 1 and return them in any order.

The graph is given as follows:
graph[i] is a list of all nodes you can visit from node i
(i.e., there is a directed edge from node i to node graph[i][j]).
"""

"""
Analysis:
- The graph format is an adjacency list
- We need to find all paths from source to target
  -> use backtracking, not just DFS/BFS
- The input graph is a DAG
  -> don't need to worry about cycles

Idea:
- Use backtracking to find all paths. States needed:
  . path: the current path being built.
  . i: current node to explore.
- For each node, explore all of its neighbor.
- A valid path starts from source and stops at destination.
"""


def all_paths_from_source_to_target(graph: list[list[int]]) -> list[list[int]]:
    all_paths: list[list[int]] = []
    source = 0
    destination = len(graph) - 1

    def backtrack(path: list[int], i: int):
        if i == destination:
            # Clone 'path' when adding since we mutate 'path' across 'backtrack' calls
            all_paths.append(path[:])
            return

        # Explore all neighbors
        for neighbor in graph[i]:
            path.append(neighbor)
            backtrack(path, neighbor)
            path.pop()

    backtrack(path=[source], i=source)
    return all_paths


"""
Complexity:
- Let N = number of nodes in graph

1. Space complexity: O(N)
- recursion stack: O(N)
- 'path': O(N)
  - A path with no cycles cannot contains more nodes than N

2. Time complexity: O(N * 2^N)
- Clone 'path' for each valid path: O(N)
- Number of valid paths: O(2^(N-2)) = O(2^N)
  . Worst case when the DAG is full connected
    (every node has a directed edge to every node after it)
    . node 0 connects to [1, 2, ... N-1]
    . node 1 connects to [2, ... N-1]
    . ...
  . Every valid path starts at 0 and ends at N-1.
    Each intermediate nodes [1, 2, ..., N-2] has 2 choices
    (included in path OR excluded from path).
    -> num_valid_paths = 2^(N-2)
=> Total work: O(N) * O(2^N) = O(N * 2^N)
"""
