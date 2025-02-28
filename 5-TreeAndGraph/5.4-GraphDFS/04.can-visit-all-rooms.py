# There are n rooms labeled from 0 to n - 1
# and all the rooms are locked except for room 0.
# Your goal is to visit all the rooms.
# When you visit a room, you may find a set of distinct keys in it.
# Each key has a number on it, denoting which room it unlocks,
# and you can take all of them with you to unlock the other rooms.
# Given an array rooms where rooms[i] is the set of keys
# that you can obtain if you visited room i,
# return true if you can visit all the rooms, or false otherwise.

# ===== Analyze =====
# - the graph is given as an adjacency list
#   (rooms[i] is an array of other reachable rooms)

# ===== Strategy =====
# - start a DFS from room 0 and see if we can visit every node
#   (use a set and check the length, or a boolean array)

def can_visit_all_rooms_recursive(rooms: list[list[int]]) -> bool:
    seen = {0}

    def dfs(node):
        for neighbor in rooms[node]:
            if neighbor not in seen:
                seen.add(neighbor)
                dfs(neighbor)

    dfs(0)

    return len(seen) == len(rooms)


def can_visit_all_rooms_iterative(rooms: list[list[int]]) -> bool:
    seen = {0}
    stack = [0]

    while len(stack) > 0:
        node = stack.pop()

        for neighbor in rooms[node]:
            if neighbor not in seen:
                seen.add(neighbor)
                stack.append(neighbor)

    return len(seen) == len(rooms)

# ===== Complexity =====
# 
# Time complexity: O(n + e)
# - each node is visited once: O(n)
# - each edge is processed at most twice: O(e)
#
# Space complexity: O(n)
# - seen: O(n)
# - recursion call stack: O(n)