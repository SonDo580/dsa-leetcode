# LeetCode would like to work on some projects to increase its capital before IPO.
# You are given n projects where the ith project has a profit of profits[i]
# and a minimum capital of capital[i] is needed to start it.
# Initially, you have w capital.
# When you finish a project, the profit will be added to your total capital.
# Return the max capital possible if you are allowed to do up to k projects.

# ===== Strategy =====
# - Always choose the most profitable project we can afford at each step.
#   This also opens the door to more projects in the next step.
# - Use a heap to keep track of the most profitable project.
#   Add projects to the heap as we gain capital.
# - Note: With heapq, simulate a max heap by negating the value

import heapq


def max_capital(k: int, w: int, profits: list[int], capital: list[int]) -> int:
    # Sort the projects by capital required,
    # to easily push affordable ones onto the heap as capital increases
    projects = sorted(zip(capital, profits))

    n = len(projects)
    heap = []
    i = 0

    # Do k projects
    for _ in range(k):
        # Push profits of affordable projects to the max heap
        # We can stop when capital > w since the projects are already sorted
        while i < n and projects[i][0] <= w:
            heapq.heappush(heap, -projects[i][1])
            i += 1

        # Not enough money to do any more projects
        if len(heap) == 0:
            return w

        # Do the most profitable project and accumulate capital
        w -= heapq.heappop(heap)

    return w


# ===== Complexity =====
# - Let n the number of projects given
# - The heap's max size is n -> its operation is O(log(n))
#
# 1. Time complexity:
# - Sorting the input: O(n*log(n))
# - n heap pushes: O(n*log(n))
# - k heap pop: O(k*log(n))
# => Overall: O((n + k)*log(n))
#
# 2. Space complexity: O(n) - for the heap
