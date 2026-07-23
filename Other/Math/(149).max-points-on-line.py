"""
https://leetcode.com/problems/max-points-on-a-line/

Given an array of points where points[i] = [xi, yi]
represents a point on the X-Y plane,
return the maximum number of points that lie on the same straight line.
"""

"""
Idea:
- A, B, C is on a straight line if:
  . DyAB / DxAB = DyBC / DxBC (same slope and have a common point)
    where Dx(i,j) = yi - yj, Dy(i,j) = xi - xj
  -> Use a hash map to group points, with key=Dy/Dx between any 2 points in group.
- Using floating-point value as hashmap key is not ideal (rounding issue).
  -> Reduce Dy/Dx then use tuple (reduced_Dy, reduced_Dx) as key. 
- For each point i:
  . Start a new hashmap 'slopes'. 
    . key = slope of a line through i
    . value = number of points (other than i) on the line.
  . Try grouping i with each point j that comes after i.
    (group i with j that comes before i <-> group previous i with current i, 
     which was handled by previous iterations)
  . If Dy/Dx match, put the point in the bucket.
  . Max number of points on a line through i: 1 + max(slopes.values())

- Normalize fraction (fully reduce a/b):
  . Find GCD(a, b): use Euclidean algorithm
  . a = a // gcd
  . b = b // gcd
"""


from collections import defaultdict


def get_gcd(a: int, b: int) -> int:
    while b != 0:
        a, b = b, a % b
    return a


def get_slope(p1: tuple[int, int], p2: tuple[int, int]) -> tuple[int, int]:
    """
    Slope of a line go through both points is Dy / Dx.
    Return tuple (Dy, Dx) in normalized form.
    """
    x1, y1 = p1
    x2, y2 = p2
    dy = y1 - y2
    dx = x1 - x2
    assert not (dx == 0 and dy == 0)  # all points are unique (constraint)

    if dy == 0:  # 2 points are on the same horizontal line
        return (0, 1)

    if dx == 0:  # 2 points are on the same vertical line
        return (1, 0)

    # normalize to (positive/positive) or (negative/positive)
    if (dy < 0 and dx < 0) or (dy > 0 and dx < 0):
        dy, dx = -dy, -dx

    # reduce
    gcd = get_gcd(abs(dy), abs(dx))
    dy //= gcd
    dx //= gcd

    return (dy, dx)


class Solution:
    def maxPoints(self, points: list[list[int]]) -> int:
        ans = 1  # if there's a single point

        n = len(points)
        for i in range(n - 1):
            # number of points except i on the line with a given slope
            points_per_slope: defaultdict[int, int] = defaultdict(int)

            for j in range(i + 1, n):
                slope = get_slope(points[i], points[j])
                points_per_slope[slope] += 1
                ans = max(ans, 1 + points_per_slope[slope])

        return ans


"""
Complexity:

1. Time complexity: O(n^2)
- get_gcd: O(log(min(a, b)))
- get_slope: O(get_gcd(abs(dy), abs(dx))) = O(log(min(max_dy, max_dx)))
  . max_dy = max_y - min_y = max(points[i][1]) - min(points[i][1])
  . max_dx = max_x - min_x = max(points[i][0]) - min(points[i][0])
- . i = 0: n - 1 get_slope calls
  . i = 1: n - 2 get_slope calls
  . ...
  . i = n - 2: 1 get_slop calls
  -> T = n-1 + n-2 + ... + 2 = n*(n-1)/2 - 1 = O(n^2)

2. Space complexity: O(n-1) = O(n) for 'points_per_slope' dict.
"""
