# You are given an n x n integer matrix board
# where the cells are labeled from 1 to n2 in a Boustrophedon style
# starting from the bottom left of the board (i.e. board[n - 1][0]) and alternating direction each row.
#
# You start on square 1 of the board.
# In each move, starting from square curr, do the following:
# - Choose a destination square next with a label in the range [curr + 1, min(curr + 6, n2)].
#   This choice simulates the result of a standard 6-sided die roll:
#   i.e., there are always at most 6 destinations, regardless of the size of the board.
# - If next has a snake or ladder, you must move to the destination of that snake or ladder.
#   Otherwise, you move to next.
# - The game ends when you reach the square n2.
#
# A board square on row r and column c has a snake or ladder if board[r][c] != -1.
# The destination of that snake or ladder is board[r][c].
# Squares 1 and n2 are not the starting points of any snake or ladder.
#
# Note that you only take a snake or ladder at most once per dice roll.
# If the destination to a snake or ladder is the start of another snake or ladder,
# you do not follow the subsequent snake or ladder.
# - For example, suppose the board is [[-1,4],[-1,3]], and on the first move,
#   your destination square is 2. You follow the ladder to square 3,
#   but do not follow the subsequent ladder to 4.
#
# Return the least number of dice rolls required to reach the square n2. If it is not possible to reach the square, return -1.

# Example 1:
# Input:
# board = [
#     [-1, -1, -1, -1, -1, -1],
#     [-1, -1, -1, -1, -1, -1],
#     [-1, -1, -1, -1, -1, -1],
#     [-1, 35, -1, -1, 13, -1],
#     [-1, -1, -1, -1, -1, -1],
#     [-1, 15, -1, -1, -1, -1],
# ]
# Output: 4
# Explanation:
# In the beginning, you start at square 1 (at row 5, column 0).
# You decide to move to square 2 and must take the ladder to square 15.
# You then decide to move to square 17 and must take the snake to square 13.
# You then decide to move to square 14 and must take the ladder to square 35.
# You then decide to move to square 36, ending the game.
# This is the lowest possible number of moves to reach the last square, so return 4.

# Example 2:
# Input: board = [[-1,-1],[-1,3]]
# Output: 1

# Constraints:
# n == board.length == board[i].length
# 2 <= n <= 20
# board[i][j] is either -1 or in the range [1, n^2].
# The squares labeled 1 and n^2 are not the starting points of any snake or ladder.

# ===== Strategy =====
# - Perform BFS starting from label 1. Increment the number of dice rolls with each level.
# - The first time we reach label n^2, that's the shortest possible path.
#   If we cannot reach label n^2, return -1.
# - To find the neighbors of a node with label 'curr' and (row, col):
#   + Add all nodes in the range [curr + 1, min(curr + 6, n^2)]
#     (This ensure there are at most 6 neighbors, and the labels don't exceed n^2)
#   + For each neighbor, check the content of the cell at that label.
#     If it is not -1, explore that label instead of the current node.
#     (We will need a way to map label to the corresponding (row, col), to get the content of that cell)

# - Avoid visiting the same node again (use a set to track visited nodes).
#
# - Logic to map label to (row, col) in board:
#   + Row:
#     . If label row is in the same order as board row (top to bottom)
#       -> row = (label - 1) // n
#     . The labels are put in reverse order (bottom to top)
#       -> row = n - 1 - (label - 1) // n
#   + Col:
#     . There are 2 groups of rows. Each will contain all even or all odd rows.
#       -> check divisibility by 2 to decide
#     . The group with bottom row has the same column order as board (left to right)
#       -> col = (label - 1) % n
#     . The other group has reverse column order (right to left)
#       -> col = n - 1 - (label - 1) % n


from collections import deque


def snakes_and_ladders(board: list[list[int]]) -> int:
    n = len(board)
    n_square = n**2

    def label_to_cell(label: int) -> tuple[int, int]:
        """Map label to corresponding (row, col)"""
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

        # Visit the nodes in range [label + 1, min(label + 6, n^2)], increment the number of dice rolls
        for next_label in range(label + 1, min(label + 6, n_square) + 1):
            # Follow the label if encounter a snake/ladder
            row, col = label_to_cell(next_label)
            if board[row][col] != -1:
                next_label = board[row][col]

            if next_label not in seen:
                seen.add(next_label)
                queue.append((next_label, num_dice_rolls + 1))

    return -1
