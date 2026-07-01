"""
https://leetcode.com/problems/divide-chocolate

You have one chocolate bar that consists of some chunks.
Each chunk has its own sweetness given by the array 'sweetness'.

You want to share the chocolate with your k friends
so you start cutting the chocolate bar into k + 1 pieces using k cuts,
each piece consists of some consecutive chunks.

Being generous, you will eat the piece with the minimum total sweetness
and give the other pieces to your friends.

Find the maximum total sweetness of the piece you can get
by cutting the chocolate bar optimally.
"""

"""
Idea:
- Let S be our piece's sweetness.
  -> Check if we can cut the bar into k + 1 pieces
     where each piece's sweetness >= S
- Greedy check:
  . Iterate through the chunks and accumulate sweetness
    (reset to 0 for each new piece).
  . If adding a chunk makes sweetness >= S, make a cut after it.
  . Success if: make k cuts && final piece also satisfies condition.
- Why cut right when condition satisfies (greedy):
  . Delaying decreases total sweetness of remaining bar
    -> decreases the average sweetness of a piece
    -> increases the chance that a piece's sweetness < s.
- S's range:
  . min: min sweetness of a chunk.
  . max: total sweetness of the whole bar.
- We can binary search for optimal S (maximum valid).
"""


def divide_chocolate(sweetness: list[int], k: int) -> int:
    def can_divide(min_s: int) -> bool:
        """
        Return True if the bar can be divided into k + 1 pieces
        where each piece's sweetness >= min_s.
        """
        curr_s = 0  # sweetness of current piece
        num_pieces = 0

        for s in sweetness:
            curr_s += s
            if curr_s < min_s:
                continue

            # else: curr_s >= min_s
            num_pieces += 1
            if num_pieces == k + 1:
                return True
            curr_s = 0  # reset for next piece

        return False

    left = min(sweetness)  # min sweetness of a piece
    right = sum(sweetness)  # max sweetness of a piece
    while left <= right:
        mid = (left + right) // 2
        if can_divide(mid):
            # search better answer (greater s that is still valid)
            left = mid + 1
        else:
            # search valid answer (lower s)
            right = mid - 1
    return right


"""
Complexity:
- Let n = len(sweetness), min = min(sweetness), max = sum(sweetness)

1. Time complexity:
- Binary search: O(log(max - min)) = O(log(max))
- Check valid: O(n)
=> Overall: O(n * log(max))

2. Space complexity: O(1)
"""
