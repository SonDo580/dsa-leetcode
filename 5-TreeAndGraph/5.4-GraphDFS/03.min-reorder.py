# There are n cities numbered from 0 to n - 1 and n - 1 roads 
# such that there is only one way to travel between two different cities. 
# Roads are represented by connections where connections[i] = [x, y] 
# represents a road from city x to city y. The edges are directed. 
# Swap the direction of some edges so that every city can reach city 0. 
# Return the minimum number of swaps needed.

# ===== Analyze =====
# - this is a directed graph given as an array of edges
# - if every city can reach city 0, all roads must be directed towards 0

# ===== Strategy ===== 
# - start traversing from city 0, treat the graph as undirected
# - every time we see an edge pointing away, swap it and increment the count

from typing import List
from collections import defaultdict

def min_reorder_recursive(connections: List[List[int]]) -> int:
    roads = set() # to fast-check if an edge is in 'connections'
    graph = defaultdict(list) # represent as adjacency list
    seen = set() # track visited nodes

    for x, y in connections:
        graph[x].append(y)
        graph[y].append(x)
        roads.add((x, y))

    def dfs(node):
        swap_count = 0 # number of swaps needed
        
        # mark the node as visited
        seen.add(node) 

        # visit the neighbors
        for neighbor in graph[node]:
            if neighbor not in seen:
                # We are traversing away from city 0.
                # So if the edge is in 'connections', we need to swap it.
                if (node, neighbor) in roads:
                    swap_count += 1
                
                swap_count += dfs(neighbor)

        return swap_count

    return dfs(0) # start from 0

# ===== Complexity =====
# 
# Time complexity:
# - we visit each node once and do constant work -> O(n)
# - we visit each edge twice (including the virtual edges) -> O(2(n-1)) = O(n)
# => Overall: O(n)
#
# Space complexity:
# - seen: O(n)
# - roads: O(n-1) = O(n)
# - graph: O(n)
# => Overall: O(n)