"""
https://leetcode.com/problems/detonate-the-maximum-bombs/

You are given a list of bombs.
The range of a bomb is defined as the area where its effect can be felt.
This area is in the shape of a circle with the center as the location of the bomb.

The bombs are represented by a 0-indexed 2D integer array bombs where bombs[i] = [xi, yi, ri].
xi and yi denote the X-coordinate and Y-coordinate of the location of the ith bomb,
whereas ri denotes the radius of its range.

You may choose to detonate a single bomb.
When a bomb is detonated, it will detonate all bombs that lie in its range.
These bombs will further detonate the bombs that lie in their ranges.

Given the list of bombs, return the maximum number of bombs that can be detonated
if you are allowed to detonate only one bomb.
"""

"""
Analysis:
- The bombs network is a graph.
  The bombs are nodes (distinguished by index in 'bombs').
  Neighbors are bombs that have centers in current bomb's radius range.
- Detonating 1 bomb will eventually detonate all bombs reachable from it.
  -> The problem is finding the maximum number of nodes in a connected component.
- Note that the edges are directed.
  . If detonating bomb x detonates bomb y, the reverse may not be true.
  . Example: x = (y, 0, 3), y = (y, 2, 1)
    . 0 + 3 = 3 > 2 -> y is in x's radius range
    . 2 - 1 = 1 > 0 -> x is not in y's radius range

Implementation:
- To find neighbors of a node (bomb):
  . Calculate the distance between current center and all other centers,
    then take the ones with distance <= radius.
  . We can do this in advance and build a hashmap to lookup neighbors.
- To count number of items in a connected component:
  . Perform DFS/BFS starting from each node.
  . [Optimize] Skip traversal if a start node has been visited.
    . If we still do it, the resulting component belongs to 
      a larger or equally large component (equal if there's a cycle).
    . Equal example: A <--> B --> ... 
      (Traversing from A and from B visit the same set of nodes)
    -> Need a set to track visited nodes across traversal.
  . Because the edges are directed, a node may belongs to multiple components.
    . Example: A --> B <-- C 
      (B belongs to 2 components: {A, B} and {C, B}) 
    -> Do not skip a node visited from previous traversals
       (except for start node, in which case we should skip the whole traversal)
  . But must skip if node is visited in the current traversal,
    to prevent going in cycles.
    -> Need separate set to track visited nodes in a single traversal.
"""


from collections import defaultdict
import math


def max_detonation(bombs: list[list[int]]) -> int:
    # Build adjacency list to lookup neighbor of a node
    graph: defaultdict[int, list[int]] = defaultdict(list)
    for i in range(len(bombs) - 1):
        xi, yi, ri = bombs[i]
        for j in range(i + 1, len(bombs)):
            xj, yj, rj = bombs[j]

            # Calculate distance between centers of bomb_i and bomb_j
            distance = math.sqrt((xi - xj) ** 2 + (yi - yj) ** 2)

            # Add a directed edge if the other center is in radius range
            if distance <= ri:
                graph[i].append(j)
            if distance <= rj:
                graph[j].append(i)

    seen: set[int] = set()  # track visited nodes across traversals
    max_node_count = -1  # max number nodes in a connected components

    def dfs(start: int) -> int:
        """Returns number of nodes reachable from 'start'."""
        round_seen: set[int] = {start}  # track visited nodes in the current traversal
        stack: list[int] = [start]
        node_count = 0

        while stack:
            node = stack.pop()
            node_count += 1

            for neighbor in graph[node]:
                seen.add(neighbor)
                if neighbor not in round_seen:
                    round_seen.add(neighbor)
                    stack.append(neighbor)

        return node_count

    for i in range(len(bombs)):
        # Start traversing a new component if start node has not been visited
        if i not in seen:
            seen.add(i)
            max_node_count = max(max_node_count, dfs(i))

    return max_node_count


"""
Complexity:
- Number of nodes: N = len(bombs)
- Number of edges: E
  . worst case: every node is connected to every other nodes -> E = O(N^2)

1. Time complexity: O(N*(N + E)) = O(N^2 + N*E)
- Perform O(N) traversals.
- Each DFS: O(N + E).

2. Space complexity: O(N + E)
- 'graph': O(N + E)
- 'seen': O(N)
- 'round_seen': O(N)
- stack: O(N)
"""
