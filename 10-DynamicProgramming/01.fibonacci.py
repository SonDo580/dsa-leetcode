def fibonacci(n: int) -> int:
    if n == 0:
        return 0
    if n == 1:
        return 1
    
    return fibonacci(n - 1) + fibonacci(n - 2)

# Time complexity: O(2^n)
# (because every call creates 2 more calls)


# ===== Optimize =====
# Memoize the results

def fibonacci(n: int) -> int:
    memo = {} # store the results

    def recur(x: int) -> int:
        if x == 0:
            return 0
        if x == 1:
            return 1
        
        # Return the memoized result if it exists
        if x in memo:
            return memo[x]
        
        # Memoize the result
        memo[x] = recur(x - 1) + recur(x - 2)
        return memo[x]
    
    return recur(n)

# Time complexity: O(n)
# (extremely fast compared to O(2^n))

# Using recursion and memoization -> "top-down" algorithm
 

# ===== Another approach =====
# "bottom-up" algorithm
# - also known as tabulation 
# - done iteratively 

def fibonacci(n: int) -> int:
    arr = [0] * (n + 1)
    arr[1] = 1

    for i in range(2, n + 1):
        arr[i] = arr[i - 1] + arr[i - 2]
    
    return arr[n]