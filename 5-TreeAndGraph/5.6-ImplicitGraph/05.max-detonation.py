# You are given a list of bombs.
# The range of a bomb is defined as the area where its effect can be felt.
# This area is in the shape of a circle with the center as the location of the bomb.
#
# The bombs are represented by a 0-indexed 2D integer array bombs where bombs[i] = [xi, yi, ri].
# xi and yi denote the X-coordinate and Y-coordinate of the location of the ith bomb,
# whereas ri denotes the radius of its range.
#
# You may choose to detonate a single bomb.
# When a bomb is detonated, it will detonate all bombs that lie in its range.
# These bombs will further detonate the bombs that lie in their ranges.
#
# Given the list of bombs, return the maximum number of bombs that can be detonated
# if you are allowed to detonate only one bomb.

# Example 1:
# Input: bombs = [[2,1,3],[6,1,4]]
# Output: 2
# Explanation:
# If we detonate the left bomb, the right bomb will not be affected.
# But if we detonate the right bomb, both bombs will be detonated.
# So the maximum bombs that can be detonated is max(1, 2) = 2.

# Example 2:
# Input: bombs = [[1,1,5],[10,10,5]]
# Output: 1
# Explanation:
# Detonating either bomb will not detonate the other bomb,
# so the maximum number of bombs that can be detonated is 1.

# Example 3:
# Input: bombs = [[1,2,3],[2,3,1],[3,4,2],[4,5,3],[5,6,4]]
# Output: 5
# Explanation:
# The best bomb to detonate is bomb 0 because:
# - Bomb 0 detonates bombs 1 and 2. The red circle denotes the range of bomb 0.
# - Bomb 2 detonates bomb 3. The blue circle denotes the range of bomb 2.
# - Bomb 3 detonates bomb 4. The green circle denotes the range of bomb 3.
# Thus all 5 bombs are detonated.

# Constraints:
# 1 <= bombs.length <= 100
# bombs[i].length == 3
# 1 <= xi, yi, ri <= 10^5


# ===== Analyze =====
# - Consider the bombs "network" as a graph, the bombs are nodes (distinguished by index in 'bombs').
# - Detonating 1 bomb will directly detonate all bombs that have centers in the current radius range.
# - Detonating 1 bomb will eventually detonate all bombs reachable from it.
#   => The problem is finding the maximum number of nodes in a connected component.
# - Note that the edges are directed. Like in example 1, detonating the right bomb will detonate the left bomb,
#   but detonating the left bomb will not detonate the right bomb.

# ===== Implementation notes =====
# - To find neighbors of a bomb node:
#   + Calculate the distance between current center and all other centers,
#     then take the ones with distance <= radius.
#   + We can do this in advance and build a hashmap to lookup neighbors.
# - To count number of items in a connected component:
#   + Loop through all nodes and perform a traversal (DFS or BFS) from each one.
#   + For a start node, skip if it is already visited
#     (the resulting component belongs to a larger, or equally large component)
#   + Do not skip a node if it is visited from previous traversals,
#     only skip if it is visited in the current trarversal.
#     (Because the edges are directed, starting from a node may only visit 1 part of the component)
#     -> Besides the global set to track all visited nodes,
#        use a separate set to track visited nodes in a single traversal.

from collections import defaultdict
import math


def max_detonation(bombs: list[list[int]]) -> int:
    # Build hashmap to lookup neighbor of a node
    graph: defaultdict[int, list[int]] = defaultdict(list)
    for i in range(len(bombs) - 1):
        xi, yi, ri = bombs[i]
        for j in range(i + 1, len(bombs)):
            xj, yj, rj = bombs[j]

            # Calculate distance between centers of bomb_i and bomb_j
            distance = math.sqrt((xi - xj) ** 2 + (yi - yj) ** 2)

            # Add an edge if the other center is in radius range
            if distance <= ri:
                graph[i].append(j)
            if distance <= rj:
                graph[j].append(i)

    seen: set[int] = set()  # track visited nodes across traversals
    max_node_count = -1  # max number nodes in a connected components

    def dfs(start: int) -> int:
        """Returns number of nodes in the (partial) connected component starting from 'start'"""
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
        # Start traversing a new component if current node has not been visited
        if i not in seen:
            seen.add(i)
            max_node_count = max(max_node_count, dfs(i))

    return max_node_count
