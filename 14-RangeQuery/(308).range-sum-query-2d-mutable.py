"""
https://leetcode.com/problems/range-sum-query-2d-mutable/

Given a 2D matrix 'matrix', handle multiple queries of the following types:
- Update the value of a cell in matrix.
- Calculate the sum of the elements of matrix inside the rectangle defined by
  its upper left corner (row1, col1) and lower right corner (row2, col2).

Implement the NumMatrix class:
- NumMatrix(int[][] matrix):
  . Initializes the object with the integer matrix matrix.
- void update(int row, int col, int val):
  . Updates the value of matrix[row][col] to be val.
- int sumRegion(int row1, int col1, int row2, int col2):
  . Returns the sum of the elements of matrix inside the rectangle defined by
    its upper left corner (row1, col1) and lower right corner (row2, col2).
"""


# === Approach 1: Iterate through region each time ===
class NumMatrix:
    def __init__(self, matrix: list[list[int]]):
        self.matrix = matrix

    def update(self, row: int, col: int, val: int) -> None:
        self.matrix[row][col] = val

    def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
        total = 0
        for r in range(row1, row2 + 1):
            for c in range(col1, col2 + 1):
                total += self.matrix[r][c]
        return total


"""
Complexity:
- Let m = number of rows, n = number of columns

1. Time complexity:
- init: O(1)
- update: O(1)
- sum_region: O(m*n)

2. Space complexity: O(1)
"""

# === Approach 2: 2D Prefix sum ===
# (doesn't work well for dynamic data, must rebuild with each update)
"""
- Let prefix[r][c] be sum of region defined by
  upper left corner (0, 0) and lower right corner (r-1, c-1)
  -> dimension: (m + 1) * (n + 1)
- Build 'prefix':
  Base case: 
  . prefix[0][0] = 0 (empty region)
  . prefix[0][c] and prefix[r][0]: calculate like 1D prefix sum 
  Recurrence: 
  . prefix[r][c] = matrix[r-1][c-1] 
                  + prefix[r-1][c] 
                  + prefix[r][c-1] 
                  - prefix[r-1][c-1]
- Answer query:
  sum_region(r1, c1, r2, c2) = prefix[r2+1][c2+1] 
                              - prefix[r2+1][c1] 
                              - prefix[r1][c2+1]
                              + prefix[r1][c1]
"""


class NumMatrix:
    def __init__(self, matrix: list[list[int]]):
        self.matrix = matrix
        self.prefix = self.__build_prefix_sum()

    def __build_prefix_sum(self) -> list[list[int]]:
        m = len(self.matrix)  # number of rows
        n = len(self.matrix[0])  # number of columns
        prefix = [[0] * (n + 1) for _ in range(m + 1)]

        for c in range(1, n + 1):
            prefix[0][c] = self.matrix[0][c - 1] + prefix[0][c - 1]
        for r in range(1, m + 1):
            prefix[r][0] = self.matrix[r - 1][0] + prefix[r - 1][0]

        for r in range(1, m + 1):
            for c in range(1, n + 1):
                prefix[r][c] = (
                    self.matrix[r - 1][c - 1]
                    + prefix[r - 1][c]
                    + prefix[r][c - 1]
                    - prefix[r - 1][c - 1]
                )

        return prefix

    def update(self, row: int, col: int, val: int) -> None:
        self.matrix[row][col] = val
        self.prefix = self.__build_prefix_sum()

    def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
        return (
            self.prefix[row2 + 1][col2 + 1]
            - self.prefix[row2 + 1][col1]
            - self.prefix[row1][col2 + 1]
            + self.prefix[row1][col1]
        )


"""
Complexity:
- Let m = number of rows, n = number of columns

1. Time complexity:
- init: O(m*n)
- update: O(m*n)
- sum_region: O(1)

2. Space complexity: O(m*n) for 'prefix'
"""


# === Approach 3: Segment tree per row ===
"""
- Maintain a segment tree for range sum query for each row.
  . node's value = sum of elements in managed range.
- Answer sum_region query:
  . Sum query results on segment trees of [row1..row2].
"""


class SegmentTree:
    """Segment tree for range sum query."""

    def __init__(self, nums: list[int]):
        n = len(nums)
        self.tree = [0] * 4 * n
        self.__build_tree(nums, 0, n - 1, 0)

    def __lci(self, i: int) -> int:
        return 2 * i + 1

    def __rci(self, i: int) -> int:
        return 2 * i + 2

    def __build_tree(self, nums: list[int], left: int, right: int, i: int) -> None:
        if left == right:
            # reached tree node -> record node's value
            self.tree[i] = nums[left]
            return

        mid = (left + right) // 2
        lci = self.__lci(i)
        rci = self.__rci(i)

        self.__build_tree(nums, left, mid, lci)  # build left subtree
        self.__build_tree(nums, mid + 1, right, rci)  # build right subtree
        self.tree[i] = self.tree[lci] + self.tree[rci]  # aggregate result

    def update(self, pos: int, val: int, left: int, right: int, i: int) -> None:
        """Update segment tree after updating nums[pos] = val"""
        if left == right:
            # reached leaf node -> update node's value
            self.tree[i] = val
            return

        mid = (left + right) // 2
        lci = self.__lci(i)
        rci = self.__rci(i)
        if pos <= mid:
            # target managed by left child
            self.update(pos, val, left, mid, lci)
        else:
            # target managed by right child
            self.update(pos, val, mid + 1, right, rci)

        # update current node's value after updating children
        self.tree[i] = self.tree[lci] + self.tree[rci]

    def query_range(
        self, qleft: int, qright: int, left: int, right: int, i: int
    ) -> int:
        if qright < left or right < qleft:
            # node's range is completely outside query range
            return 0

        if qleft <= left and right <= qright:
            # node's range is completely inside query range -> return precomputed value
            return self.tree[i]

        # partially overlap -> query both halves and combine
        mid = (left + right) // 2
        left_res = self.query_range(qleft, qright, left, mid, self.__lci(i))
        right_res = self.query_range(qleft, qright, mid + 1, right, self.__rci(i))
        return left_res + right_res


class NumMatrix:
    def __init__(self, matrix: list[list[int]]):
        self.matrix = matrix
        m = len(matrix)  # number of rows
        self.n = len(matrix[0])  # number of cols
        self.st_list = [SegmentTree(matrix[i]) for i in range(m)]

    def update(self, row: int, col: int, val: int) -> None:
        self.matrix[row][col] = val
        self.st_list[row].update(col, val, 0, self.n - 1, 0)

    def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
        total = 0
        for r in range(row1, row2 + 1):
            total += self.st_list[r].query_range(col1, col2, 0, self.n - 1, 0)
        return total


"""
Complexity:
- Let m = number of rows, n = number of columns
- segment tree for 1 row:
  . number of nodes: O(4*n)
  . height: h = O(log(n)) (since the tree is balanced) 

1. Time complexity:
- init: O(m*n)
  . build 1 segment tree: O(4*n)
    -> build m segment trees: O(m*4*n)
- update: O(h) = O(log(n))
  . only 1 segment tree is updated
  . update follows exactly 1 path from root to a leaf
- sumRegion: O(m*log(n))
  . each query_range costs O(h)
    . at most 2 nodes per level (2 bounds) can overlap partially with query range,
      each spawns 2 extra recursive calls.
      -> at most 4 nodes are processed at each level
      -> across level: O(4*h)
  -> over row2-row1+1 rows: O(m*h) = O(m*log(n))

2. Space complexity: O(4*m*n + m) = O(m*n)
- segment tree list (pointers): O(m)
- each segment tree: O(4*n)
  -> m segment trees: O(4*m*n)
"""
