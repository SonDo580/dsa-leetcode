# You are given an array of integers stones where stones[i] is the weight of the ith stone.
# We are playing a game with the stones. 
# On each turn, we choose the heaviest two stones and smash them together. 
# Suppose the heaviest two stones have weights x and y with x <= y. 
# The result of this smash is:
# If x == y, both stones are destroyed, and
# If x != y, the stone of weight x is destroyed, and the stone of weight y has new weight y - x.
# At the end of the game, there is at most one stone left.
# Return the weight of the last remaining stone. 
# If there are no stones left, return 0.

# Example 1:
# Input: stones = [2,7,4,1,8,1]
# Output: 1
# Explanation: 
# We combine 7 and 8 to get 1 so the array converts to [2,4,1,1,1] then,
# we combine 2 and 4 to get 2 so the array converts to [2,1,1,1] then,
# we combine 2 and 1 to get 1 so the array converts to [1,1,1] then,
# we combine 1 and 1 to get 0 so the array converts to [1] then that's the value of the last stone.

# Example 2:
# Input: stones = [1]
# Output: 1

# Constraints:
# 1 <= stones.length <= 30
# 1 <= stones[i] <= 1000

import heapq

def last_stone_weight(stones: list[int]) -> int:
    # Python's heapq only implement min heap
    # To simulate a max heap:
    # - negate the values put on the heap
    # - reverse the sign again when popping items
    stones = [-stone for stone in stones]
    heapq.heapify(stones)

    while len(stones) > 1:
        # Get the 2 heaviest stones
        first = abs(heapq.heappop(stones))
        second = abs(heapq.heappop(stones))

        # If both stones are not destroyed after the smash, 
        # re-add the new stone to the heap
        weight_diff = abs(first - second) 
        if weight_diff > 0:
            heapq.heappush(stones, -weight_diff)
    
    # Return the weight of the last remaining stone or 0
    return -stones[0] if stones else 0 

# ===== Complexity =====
# 1. Time complexity:
# - Heap initialization -> O(n)
# - In each iteration, at least 1 stone is destroyed -> at most n - 1 iterations -> O(n)
# - In each iteration, perform 2 pop possibly a push on the heap -> O(log(n))
# => overall: O(n*log(n)) 
# 
# 2. Space complexity: O(n) for the heap
# (we're mutating the input 'stones')

# ===== Time complexity (in more details) =====:
# - There are at most n - 1 iterations (1 stone is destroyed each time).
#   In that case the heap start at size n, and reduced by 1 each time until it reaches 1
# - The total cost of heap operations:
#   O(log(n)) + O(log(n-1)) + O(log(n-2)) + ... + O(log(2)) + O(log(1))
#   = O(log(n * (n-1) * (n-2) * ... * 2 * 1))
#   = O(log(n!))  
#   ~= O(log(sqrt(2*pi*n)) + n*log(n/e))
#   ~= O(0.5*log(2*pi) + 0.5*log(n) + n*log(n) - n*log(e))
#   ~= O(n*log(n))
# Note: n! ~= sqrt(2*pi*n) * (n/e)^n    (Stirling approximation)