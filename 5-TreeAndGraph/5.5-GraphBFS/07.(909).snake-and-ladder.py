"""
https://leetcode.com/problems/snakes-and-ladders/

You are given an n x n integer matrix 'board'
where the cells are labeled from 1 to n^2 in a Boustrophedon style
starting from the bottom left of the board (i.e. board[n - 1][0]) and alternating direction each row.

You start on square 1 of the board.
In each move, starting from square 'curr', do the following:
- Choose a destination square next with a label in the range [curr + 1, min(curr + 6, n^2)].
  This choice simulates the result of a standard 6-sided die roll:
  i.e., there are always at most 6 destinations, regardless of the size of the board.
- If next has a snake or ladder, you must move to the destination of that snake or ladder.
  Otherwise, you move to next.
- The game ends when you reach the square n^2.

A board square on row r and column c has a snake or ladder if board[r][c] != -1.
The destination of that snake or ladder is board[r][c].
Squares 1 and n^2 are not the starting points of any snake or ladder.

Note that you only take a snake or ladder at most once per dice roll.
If the destination to a snake or ladder is the start of another snake or ladder,
you do not follow the subsequent snake or ladder.
- For example, suppose the board is [[-1,4],[-1,3]], and on the first move,
  your destination square is 2. You follow the ladder to square 3,
  but do not follow the subsequent ladder to 4.

Return the least number of dice rolls required to reach the square n^2.
If it is not possible to reach the square, return -1.
"""

"""
Idea:
- Perform BFS starting from label 1. Increment the number of dice rolls with each level.
- The first time we reach label n^2, that's the shortest possible path.
  If we cannot reach label n^2, return -1.
- Avoid visiting the same node again: use a set to track visited nodes.

- Map 1-indexed label to 0-indexed (row, col):
  + Row:
    . If labels are put from top to bottom: row = (label - 1) // n
      In this problem, labels are put from bottom to top
      -> row = n - 1 - (label - 1) // n
  + Col:
    . Group 1: Labels in rows [n-1, n-3, ...] are put from left to right
      -> col = (label - 1) % n
    . Group 2: Labels in rows [n-2, n-4, ...] are put from right to left
      -> col = n - 1 - (label - 1) % n
    . Decide group:
      . row % 2 = (n - 1) % 2 -> group 1
      . row % 2 != (n - 1) % 2 -> group 2
    
- Find neighbors of a node with label 'curr':
  . Candidates (next_label): [curr + 1, min(curr + 6, n^2)]
  . For each next_label, check corresponding cell content.
    If cell_content != -1, explore label=cell_content instead of next_label.
"""


from collections import deque


def snakes_and_ladders(board: list[list[int]]) -> int:
    n = len(board)
    n_square = n**2

    def label_to_cell(label: int) -> tuple[int, int]:
        """Map label to corresponding (row, col)."""
        row = n - 1 - (label - 1) // n
        if row % 2 == (n - 1) % 2:
            col = (label - 1) % n
        else:
            col = n - 1 - (label - 1) % n
        return row, col

    seen: set[int] = {1}  # track visited nodes by label
    queue: deque[tuple[int, int]] = deque([(1, 0)])  # (label, number of dice rolls)

    while queue:
        label, num_dice_rolls = queue.popleft()

        # Return number of dice rolls when destination is reached the first time
        if label == n_square:
            return num_dice_rolls

        # Visit the nodes in range [label + 1, min(label + 6, n^2)],
        # increment the number of dice rolls.
        for next_label in range(label + 1, min(label + 6, n_square) + 1):
            # next_label = board[row][col] if encounter a snake/ladder
            row, col = label_to_cell(next_label)
            if board[row][col] != -1:
                next_label = board[row][col]

            if next_label not in seen:
                seen.add(next_label)
                queue.append((next_label, num_dice_rolls + 1))

    return -1


"""
Complexity:
- Number of nodes: N = O(n^2)
- Number of edges: E = O(6 * N) = O(N)

1. Time complexity: O(N + E) = O(n^2)

2. Space complexity: O(N) = O(n^2)
- 'seen': O(N)
- queue: O(N') where N' < N (don't hold all nodes at once)
"""
