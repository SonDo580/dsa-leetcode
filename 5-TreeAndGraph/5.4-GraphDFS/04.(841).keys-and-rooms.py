"""
https://leetcode.com/problems/keys-and-rooms/

There are n rooms labeled from 0 to n - 1
and all the rooms are locked except for room 0.
Your goal is to visit all the rooms.

When you visit a room, you may find a set of distinct keys in it.
Each key has a number on it, denoting which room it unlocks,
and you can take all of them with you to unlock the other rooms.

Given an array 'rooms' where rooms[i] is the set of keys
that you can obtain if you visited room i,
return true if you can visit all the rooms, or false otherwise.
"""

"""
Analyze:
- This is a directed graph given as an adjacency list
  . rooms[i] is an array of other reachable rooms

Idea:
- Start DFS/BFS from room 0 and see if we can visit every node.
  . Check final size of the set of visited nodes.
"""


def can_visit_all_rooms_recursive(rooms: list[list[int]]) -> bool:
    seen: set[int] = {0}

    def dfs(node: int) -> None:
        for neighbor in rooms[node]:
            if neighbor not in seen:
                seen.add(neighbor)
                dfs(neighbor)

    dfs(0)
    return len(seen) == len(rooms)


def can_visit_all_rooms_iterative(rooms: list[list[int]]) -> bool:
    seen: set[int] = {0}
    stack: list[int] = [0]
    while stack:
        node = stack.pop()
        for neighbor in rooms[node]:
            if neighbor not in seen:
                seen.add(neighbor)
                stack.append(neighbor)

    return len(seen) == len(rooms)


"""
Complexity:
- Number of nodes: n
  Number of edges: E
  Max depth: h
  . worst case: h = O(n)

1. Time complexity: O(n + E)
- visit each node/edge once

2. Space complexity: O(n)
- 'seen': O(n)
- stack:
  . recursive approach: O(h)
  . iterative approach: O(n)
"""
