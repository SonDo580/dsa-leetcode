# You are given a string s and an integer k. 
# Find the length of the longest substring 
# that contains at most k distinct characters.

# For example, given s = "eceba" and k = 2, return 3. 
# The longest substring with at most 2 distinct characters is "ece".

def longest_substring(s: str, k: int) -> int:
    counts = {}
    left = 0
    max_length = 0

    for right in range(len(s)):
        right_char = s[right]
        if right_char not in counts:
            counts[right_char] = 0
        counts[right_char] += 1

        while len(counts) > k:
            left_char = s[left]
            counts[left_char] -= 1
            if counts[left_char] == 0:
                del counts[left_char]
            left += 1
        
        max_length = max(max_length, right - left + 1)

    return max_length

# Time complexity: O(n)
# (the work inside the while loop is amortized O(1))

# The hash map use O(k) space
# (the algorithm deletes elements when it goes beyond k)