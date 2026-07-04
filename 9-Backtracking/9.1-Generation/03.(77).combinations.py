"""
https://leetcode.com/problems/combinations/

Given two integers n and k,
return all possible combinations of k numbers chosen from the range [1, n].
You may return the answer in any order.
"""

"""
Idea:
- The problems is asking for subsets of length k.
  -> Similar to '(78).subsets', but only add result when subset_length == k.

Details:
- Use backtracking to find all combinations. States needed:
  . curr: the combination being built
  . start: only add numbers in [start..n]
- We need 'start' to avoid duplicates. Because order doesn't matter in a combination,
  only combine in 1 direction (forward).
- When 'curr' reaches length k, add it to result.
"""


def get_combinations(n: int, k: int) -> list[list[int]]:
    ans: list[list[int]] = []

    def build(curr: list[int], start: int):
        if len(curr) == k:
            # Mutate 'curr' across 'build' calls -> clone when adding
            ans.append(curr[:])
            return

        for num in range(start, n + 1):
            curr.append(num)
            build(curr, num + 1)
            curr.pop()

    build(curr=[], start=0)
    return ans


"""
Complexity:
- Each 'build' call is a node in recursion tree.
- Recursion depth: O(k)

1. Time complexity: O(k * nCk)
- Number of distinct combinations (number of leaves): nCk
  . n options for 1st position
  . n - 1 options for 2nd position
  . ...
  . n - k + 1 options for kth position
  -> ways to choose k items: n * (n - 1) * ... * (n - k + 1) = n! / (n - k)!
  . the same subset has k! permutations
  -> number of distinct subsets: n! / (k! * (n - k)!)
- Work at leaves:
  . clone 'curr' list (per leaf node): O(k)
  -> clone 'curr' list (across leaves): O(k * nCk)

- Number of nodes: O(nCk)
  . level 0: empty combination, 1 root
  . level 1: size=1 combinations, nC1 nodes
  . level 2: size=2 combinations, nC2 nodes
  . ...
  . level k: reached results -> nCk leaves
  -> total nodes = sum(nCi for i in [0..k]) = O(nCk)
- Total loop work = number of branches spawn
                  = number of nodes - 1     (exclude root)
                  = O(nCk)
  (if being lax, total_node = O(k * nCk), 
   but that doesn't change overall time complexity)

=> Overall: O(k * nCk) + O(nCk) = O(k * nCk)

2. Space complexity: O(k)
- recursion stack: O(k)
- 'curr': O(k)
"""

# === Extra: Why sum(nCi for i in [0..k]) = O(nCk) ===
"""
- Growth rate between levels:
  . nCi / nC(i-1) = (n! / (i! * (n-i)!)) / (n! / ((i-1)! * (n-i+1)!))
    = (n - i + 1) / i = n/i - 1 + 1/i

1) Case 1: k <= n / 2
. i <= k <= n/2
  -> (n - i + 1) / i >= n/(n/2) - 1 + 1/(n/2) = 1 + 2/n > 1
  -> number of nodes grow exponentially level by level.

. total_nodes = sum(nCi for i in [0..k])
  = n! / k!*(n-k)! + n! / (k-1)!*(n - k + 1)! + n! / (k-2)!*(n-k+2)! + ...
  = nCk * (1 + k/(n-k+1) + k*(k-1) / (n-k+1)*(n-k+2) + ...)

. Let r = k/(n-k+1) = 1 / (n/k - 1 + 1/k)
  . k <= n/2 -> n/k - 1 + 1/k >= 1 + 2/n > 1
  . -> r = 1 / (n/k - 1 + 1/k) < 1

. Analyze some terms:
  . i = 0: 1
  . i = 1: k/(n-k+1) = r
  . i = 2: k/(n-k+1) * (k-1)/(n-k+2)
  . i = 3: k/(n-k+1) * (k-1)/(n-k+2) * (k-2)/(n-k+3)
  . i = i: k/(n-k+1) * ... * (k-i+1)/(n-k+i)

. Compare k/(n-k+1) and (k-i+1)/(n-k-i+1) when i > 1
  . i > 1 -> . k - i + 1 < k
             . n - k + i > n - k + 1
    -> (k-i+1)/(n-k+i) < k/(n-k+1) = r
    -> k/(n-k+1) * ... * (k-i+1)/(n-k+i) < r^i 
  
=> total_nodes < nCk * sum(r^i for i in [0..inf]) 
               = nCk * (1 / (1 - r))      (geometric series sum with r < 1)
               = nCk * constant
               = O(nCk)

2) Case 2: k > n/2
  . choosing k elements to keep <-> choosing n - k elements to skip
  . k > n/2 -> n - k < n/2 -> reduce to case 1
"""
