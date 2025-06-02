# You are given an array of non-negative integers nums and an integer k. 
# In one operation, you may choose any element from nums and increment it by 1. 
# Return the maximum product of nums after at most k operations, modulo 
# 10^9 + 7

# ===== Analyze =====
# - Consider any 2 element x and y such that x > y
# - If we increment x: (x + 1) * y = xy + y
# - If we increment y: (y + 1) * x = xy + x
# - Since x > y, the later product is greater
# => We should greedily increment the smallest element at every operation
# => Convert nums to a min heap, pop from it, increment, then push back
#    Do this k times, multiply the numbers, then apply modulo operation
# 
# - The number can get very large at the end
# => We should take the modulus at every operation

# Formula (see note.md):
# a1.a2...an mod n = ((a1 mod n).a2 mod n ...).an mod n

import heapq

def max_product(nums: list[int], k: int) -> int:
    heapq.heapify(nums)

    for _ in range(k):
        heapq.heappush(nums, heapq.heappop(nums) + 1)

    MOD = 1_000_000_007
    
    result = 1
    for num in nums:
        result = (result * num) % MOD

    return result