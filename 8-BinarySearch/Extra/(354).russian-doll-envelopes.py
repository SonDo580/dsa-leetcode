"""
https://leetcode.com/problems/russian-doll-envelopes

You are given a 2D array of integers envelopes where
envelopes[i] = [wi, hi] represents the width and the height of an envelope.

One envelope can fit into another if and only if both the width and height
of one envelope are greater than the other envelope's width and height.

Return the maximum number of envelopes you can Russian doll
(i.e., put one inside the other).

Note: You cannot rotate an envelope.

Example 1:
Input: envelopes = [[5,4],[6,4],[6,7],[2,3]]
Output: 3
Explanation: The maximum number of envelopes you can Russian doll is 3 ([2,3] => [5,4] => [6,7]).

Example 2:
Input: envelopes = [[1,1],[1,1],[1,1]]
Output: 1

Constraints:
1 <= envelopes.length <= 10^5
envelopes[i].length == 2
1 <= wi, hi <= 10^5
"""

"""
Analysis:
- The envelopes can be nested if w1 < ... < wn and h1 < ... < hn
- If we sort by width ascending first, the problem reduce to finding the 
  longest strictly increasing subsequence on the height dimension
  (alternative: sort by height then find LIS on the width dimension)
- In any sequence, there should only be 1 envelope with a particular width,
  since envelopes with equal widths can not be nested.
  But the LIS finding algorithm may add both (w, h1) and (w, h2) if h1 < h2, 
  since it only operates on the height dimension.
  -> Sort by height descending for a group with the same width.
- To find length of LIS: see '(300).longest-increasing-subsequence' 
"""

import bisect


def max_envelopes(envelopes: list[tuple[int, int]]) -> int:
    def _length_of_LIS(nums: list[int]) -> int:
        tails: list[int] = []
        for num in nums:
            if len(tails) == 0 or tails[-1] < num:
                tails.append(num)
            else:
                idx = bisect.bisect_left(tails, num)
                tails[idx] = num
        return len(tails)

    envelopes.sort(key=lambda x: (x[0], -x[1]))  # width ASC, height DESC
    heights = [height for _, height in envelopes]
    return _length_of_LIS(heights)


"""
Complexity:
- Let n = envelopes.length

1. Time complexity:
- Sort 'envelopes': O(n * log(n))
- Build 'heights': O(n)
- Find LIS on 'heights': O(n * log(n))
=> Overall: O(n * log(n))

2. Space complexity:
- Sort 'envelopes': Python's timsort takes O(n)
- 'heights': O(n)
- 'tails': O(n)
=> Overall: O(n)
"""
