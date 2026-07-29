"""
https://leetcode.com/problems/counting-bits/

Given an integer n, return an array 'ans' of length n + 1
such that for each i (0 <= i <= n),
ans[i] is the number of 1's in the binary representation of i.
"""

"""
Idea:
- For each i > 0, i & (i - 1) clear the lowest set bit of n 
  -> Repeat until i becomes 0. Count number of steps.
- Perform for i in range [0..n] to produce answer.
"""


def count_set_bits(i: int) -> int:
    cnt = 0
    while i > 0:
        i &= i - 1
        cnt += 1
    return cnt


class Solution:
    def countBits(self, n: int) -> list[int]:
        ans: list[int] = []
        for i in range(n + 1):
            ans.append(count_set_bits(i))
        return ans


"""
Complexity:
- Let L = bit length

1. Time complexity: O(n * L)
2. Space complexity: O(1)
"""


# === Optimize ===
"""
- Range [2^k..2^(k+1)-1] has bit pattern: '1 <k low bits>'
  -> Each number corresponds to a number in range [0..2^k-1]
     (represented by k low bits)
  -> count_ones[i] = 1 + count_ones[i-2^k]
     for i in [2^k..2^(k+1)-1]      (if 2^(k+1)-1 > n, use n)
- Base cases: ans[0] = 0
"""


class Solution:
    def countBits(self, n: int) -> list[int]:
        ans: list[int] = [0]

        k = 0
        while (1 << k) <= n:
            mask = 1 << k
            for i in range(mask, min(n + 1, 1 << (k + 1))):  # [2^k..min(n, 2^(k+1)-1)]
                ans.append(1 + ans[i - mask])
            k += 1

        return ans


"""
Complexity:
1. Time complexity: O(n)
2. Space complexity: O(1)
"""
