"""
https://leetcode.com/problems/find-the-longest-valid-obstacle-course-at-each-position

You want to build some obstacle courses.
You are given a 0-indexed integer array obstacles of length n,
where obstacles[i] describes the height of the ith obstacle.

For every index i between 0 and n - 1 (inclusive),
find the length of the longest obstacle course in obstacles such that:
- You choose any number of obstacles between 0 and i inclusive.
- You must include the ith obstacle in the course.
- You must put the chosen obstacles in the same order as they appear in obstacles.
- Every obstacle (except the first) is taller than or the same height as the obstacle immediately before it.

Return an array ans of length n,
where ans[i] is the length of the longest obstacle course for index i as described above.
"""

"""
=> Core problem:
Find the length of the longest increasing subsequence that ends at each index i.
"""

# ========== Approach 1: DP ==========
# ====================================
"""
- ans[i] is the length of the LIS that ends at i
- We can add obstacles[i] to subsequences that ends at j before i if obstacles[j] <= obstacles[i]
  -> ans[i] = max(ans[j] + 1) where j is in [0, i) and obstacles[j] <= obstacles[i]
- Base case: every element is a subsequence with length 1.
"""


# [!] This approach exceeds time limit
def longest_obstacle_course(obstacles: list[int]) -> list[int]:
    n = len(obstacles)
    ans: list[int] = [1] * n
    for i in range(n):
        for j in range(i):
            if obstacles[j] <= obstacles[i]:
                ans[i] = max(ans[i], ans[j] + 1)
    return ans


"""
Complexity:
- Let n = len(obstacles)

1. Time complexity: O(n^2)

2. Space Complexity: O(1) 
('ans' is output -> not counted)
"""


# ========== Approach 2: Binary search ==========
# ===============================================
"""
- In the range [0, i), let the range of subsequence length be [1, L].
  Since obstacles[i] can only be append to the subsequence if tail <= obstacles[i],
  pick the subsequence with the smallest tail for each length value.
  -> Use a list 'tails' where tails[L] is smallest tail for any subsequence with length L + 1.
     len(tails) is also the length of the current LIS.
- The smallest tail for length L + 1 >= the smallest tail for length L
  -> 'tails' is monotonically increasing: tails[0] <= tails[1] <= ...
- For a new element i, there are 2 possibilities:
  + obstacles[i] >= all previous tails (compare with tails[-1])
    -> . append obstacles[i] to 'tails'
       . ans[i] = len(tails)
  + Otherwise, obstacles[i] can be a better (smaller) tail for an existing subsequence length
    -> . find the first index j such that tails[j] > obstacles[i]
       . replace tails[j] = obstacles[i]
       . update ans[i] = j + 1
- Since 'tails' is monotonically increasing, we can perform binary search
  to find the first element > x (bisect_right/upper_bound operation)
"""

import bisect


def longest_obstacle_course(obstacles: list[int]) -> list[int]:
    ans: list[int] = []
    tails: list[int] = []

    for obstacle in obstacles:
        if len(tails) == 0 or tails[-1] <= obstacle:
            tails.append(obstacle)
            ans.append(len(tails))
        else:
            idx = bisect.bisect_right(tails, obstacle)
            tails[idx] = obstacle
            ans.append(idx + 1)

    return ans


"""
Complexity:

1. Time complexity: 
- n iterations
- binary search on 'tails' in each iteration: O(log(n))
=> Overall: O(n * log(n))

2. Space Complexity: O(n) for 'tails'
"""
